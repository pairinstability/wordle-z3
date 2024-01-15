#!/usr/bin/env python3

import z3
from os.path import exists

DICTIONARY_FILE = "dictionary"
WORD_LENGTH = 5
LETTER_TO_INDEX = {letter: index for index, letter in enumerate("abcdefghijklmnopqrstuvwxyz")}
INDEX_TO_LETTER = {index: letter for letter, index in LETTER_TO_INDEX.items()}


# defines a word as consisting of 5 z3 Int char indexes
def define_letter_variables():
    return [z3.Int(f"letter_{index}")for index in range(WORD_LENGTH)]

# each guess is a z3 Int constrained by the length of the alphabet
def add_alphabet_constraint(solver, letter_vars):
    for letter_var in letter_vars:
        solver.add(letter_var >= 0, letter_var <= 25)

    return solver

def add_legal_words_constraint(solver, words, letter_vars):
    all_words_disjunction = []
    # maps any letter to an index value 0-25

    for word in words:
        word_conjunction = z3.And([letter_vars[index] == LETTER_TO_INDEX[letter] for index, letter in enumerate(word)])
        all_words_disjunction.append(word_conjunction)

    solver.add(z3.Or(all_words_disjunction))

    return solver

# letters that are excluded
def add_gray_constraint(solver, letter_vars, letter):
    for letter_var in letter_vars:
        solver.add(letter_var != LETTER_TO_INDEX[letter])

    return solver

# letters that are correct but in wrong position
def add_gold_constraint(solver, letter_vars, letter, position):
    # bad position
    solver.add(letter_vars[position] != LETTER_TO_INDEX[letter])
    # contains letter
    solver.add(z3.Or([letter_var == LETTER_TO_INDEX[letter] for letter_var in letter_vars]))

    return solver

# letters that are correct and in right position
def add_green_constraint(solver, letter_vars, letter, position, occurrence):
    # exact position
    solver.add(letter_vars[position] == LETTER_TO_INDEX[letter])
    
    if occurrence == "T":
        unique_letter_disjunction = []

        # occurrence
        for letter_var in letter_vars:
            this_letter_conjunction = [letter_var == LETTER_TO_INDEX[letter]]
            for other_letter_var in letter_vars:
                if letter_var == other_letter_var:
                    continue
                this_letter_conjunction.append(other_letter_var != LETTER_TO_INDEX[letter])
            unique_letter_disjunction.append(z3.And(this_letter_conjunction))

        solver.add(z3.Or(unique_letter_disjunction))

    return solver

def prompt_input(solver, letter_vars):
    constraints = input("enter letter constraints\n").split(",")

    gray = constraints[0]
    gold = constraints[1]
    green = constraints[2]
    
    # letters that are excluded 
    if gray:
        for letter in gray:
            solver = add_gray_constraint(solver, letter_vars, letter)  

    # letters that are in the wrong position
    if gold:
        for letter, position in gold.split("."):
            solver = add_gold_constraint(solver, letter_vars, letter, int(position)) 

    # fully correct letters
    if green:
        for letter, position, occurrence in green.split("."):
            solver = add_green_constraint(solver, letter_vars, letter, int(position), occurrence)

    return solver

if __name__ == "__main__":
    # check if dictionary exists
    if not exists(DICTIONARY_FILE):
        print("dictionary not present. use `get_dict.py` first.")
        exit()

    words = []

    with open(DICTIONARY_FILE) as f:
        while (line := f.readline().rstrip()):
            words.append(line)

    print("setting up solver")
    # z3 setup
    solver = z3.Solver()

    # initial constraints
    letter_vars = define_letter_variables()
    solver = add_alphabet_constraint(solver, letter_vars)
    solver = add_legal_words_constraint(solver, words, letter_vars)

    # prompt for constraints
    solver = prompt_input(solver, letter_vars)

    print("solving given constraints")
    result = solver.check()
    print(result)
    assert result == z3.sat

    model = solver.model()

    word = []
    for index, letter_var in enumerate(letter_vars):
        word.append(INDEX_TO_LETTER[model[letter_var].as_long()])

    print(''.join(word))

