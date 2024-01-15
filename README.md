note the `get_dict.py` doesn't work anymore since wordle moved to the NYT. I wrote this whenever wordle was popular

# wordle solver

wordle is cool. I also want to learn Z3 and be better at wordle.

its basically hangman+. you get 5 guesses for a 5 letter word, and with each word guess it states whether a letter either doesnt exist in the answer, exists but you entered it at the wrong position, or it exists and you entered it in the right position.


## requirements

- requests
- z3

## usage

run the `get_dict.py` to download the dictionary of words scraped from the website.

run the `solve.py` and enter constraints to determine the word to enter into the wordle website. The first should be 'slate'  because it seems to work reliably. run the script when wanting to find the next word. its pretty hacky but makes solving it easier and its how a human would do it.

the gray constraints are just the excluded letters.

the gold constraints are the letter and position pairs separated by a .

the green constraints are the letter, position, and occurrence pairs separated by a . T for occurrence means it occurs only once, F means multiple times or unknown. 

the constraints need not be strictly appended, as if letters are found to be green and occur once, having the same letter as a gold constraint is not necessary but it works either way.

for example, for 2022-01-16:
1. entering 'slate' reveals 's' green, 'la' gold, 'te' gray
	- constraints are 'te,l1.a2,s0F'. this produces 'salad'
2. entering 'salad' now reveals 'la' as green, 'ad' as gray
	- constraint are now 'ted,l1.a2,s0F.l2F.a3T'. this produces 'solar' which is correct.

```
Wordle 211 3/6

🟩🟨🟨⬛⬛
🟩⬛🟩🟩⬛
🟩🟩🟩🟩🟩
```
