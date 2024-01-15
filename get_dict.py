#!/usr/bin/env python3

import requests

URL = "https://www.powerlanguage.co.uk/wordle/main.c1506a22.js"

r = requests.get(URL)

content = bytes.decode(r.content)

solution_begin = "La=["
solution_end = "],Ta="

dict_subset_begin = "Ta=["
dict_subset_end = "],Ia="

# all ordered solutions
# +1 and -1 to get rid of leading and trailing "
solutions = content[content.find(solution_begin)+len(solution_begin)+1:content.find(solution_end)-1].split('","')

# rest of possible words
dict_subset = content[content.find(dict_subset_begin)+len(dict_subset_begin)+1:content.find(dict_subset_end)-1].split('","')

dictionary = solutions + dict_subset
dictionary.sort()

with open("dictionary", "w") as f:
    for words in dictionary:
        f.writelines(words+"\n")
