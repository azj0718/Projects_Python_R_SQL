# Import modules to be used in program

import sys
from wordscore import *

import time
start = time.time()

# Open Dictionary

with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    sowpods = [datum.strip('\n').lower() for datum in raw_input]

# Illegal characters and scoring dictionary

illegal_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '+', ',', '-', '.', '/', ':', ';', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']

scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}

# Initial input from command line

o = sys.argv

# Input validity Checking

class Error(Exception):
    """Base class for other exceptions"""
    pass

class SysLenError1(Error):
    """If no rack entered during initial input."""
    pass

class SysLenError2(Error):
    """If space used in initial input."""
    pass

class LenError1(Error):
    """If space used in initial input."""
    pass


illegal_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '+', ',', '-', '.', '/', ':', ';', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' ']

try:
    o = sys.argv
    if len(o) == 1:
        raise SysLenError1
    if len(o) > 2:
        raise SysLenError2
except SysLenError1:
    print("You didn't enter a rack, please re-run and enter a rack of valid characters.")
    sys.exit()
except SysLenError2:
    print("No spaces permitted, please re-run and enter a rack without spaces and valid characters.")
    sys.exit()
else:
    a = (sys.argv[1]).strip('""')

try:
    if len(a) < 2 or len(a) > 7:
        raise LenError1
    else:
        pass
except LenError1:
    print("You must only enter between 2-7 legal characters. Please re-run program.")
    sys.exit()
else:
    pass

try:
    for letter in a:
        if letter in illegal_characters:
            raise ValueError
except ValueError:
    print("You entered an invalid character, only letters, '*', and '?' are allowed. Please re-run program.")
    sys.exit()
else:
    pass

try:
    for letter in a:
        if a.count('*') > 1:
            raise ValueError
except ValueError:
    print("Only one of each wildcard character is allowed. Please re-run program.")
    sys.exit()
else:
    pass

try:
    for letter in a:
        if a.count('?') > 1:
            raise ValueError
except ValueError:
    print("Only one of each wildcard character is allowed. Please re-run program.")
    sys.exit()
else:
    pass


def input_sorter(arguments):
    '''
    This takes the input rack as a string, and returns a sorted list.
    This is important as the sort function moves "*" and "?" to the front, in that order.
    '''
    input_rack = []
    for x in arguments.lower():
        input_rack.append(x)
        input_rack.sort()
    return input_rack

def data_cutter(dataset, input_rack):
    '''
    Cut down dataset to only items <= length of input rack.
    '''
    data = []
    for item in dataset:
        if len(item) <= len(input_rack):
            data.append(item)
    return data

def wildcard_checker(words):
    '''
    Checks if wildcards are present.
    If single wildcard is present, creates 26 new lists of character permutations.
    If 2 wildcards are present it creates 276 new lists using itertools, representing every possible permutations of 2 letters.
    If no wildcards are present, it just outputs the original sorted input list.
    '''
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    new_list = []
    if words[0] == '*' and not "?" in words:
        for item in alphabet:
            temp_list = words[1:]
            temp_list.insert(0,item)
            new_list.append(temp_list)
    elif words[0] == '?' and not "*" in words:
        for item in alphabet:
            temp_list = words[1:]
            temp_list.insert(0,item)
            new_list.append(temp_list)
    elif words[0] == '*' and words[1] == '?':
        from itertools import combinations_with_replacement
        combos = combinations_with_replacement(alphabet, 2)
        combos = list(combos)
        for item in combos:
            a, b = item
            temp_list = words[2::]
            temp_list.insert(0,a)
            temp_list.insert(1,b)
            new_list.append(temp_list)
    else:
        new_list = words
    return new_list

def character_dict(master):
    '''
    Convert a word into a dictionary (used for both match_words and wildcard_match functions).
    '''
    char_dict = {}
    for word in master:
        char_dict[word] = char_dict.get(word, 0) + 1
    return char_dict

def match_words(master_list, characters):
    '''
    For racks with no wildcards.
    Iterates through SOWPODS creating a dictionary for each word and compare letters in rack with it.
    Returns a single list of possible words.
    '''
    final_list = []
    for word in master_list:
        positive = 1
        word_dict = character_dict(word)
        for item in word_dict:
            if item not in characters:
                positive = 0
            elif word_dict[item] > characters.count(item):
                positive = 0
        if positive == 1:
            final_list.append(word)
            continue
    return final_list

def wildcard_match(master_list, wildcard_chars):
    '''
    If the racks contains wildcards, this function iterates through all of the lists of possible letter combinations and in order     for the word to be correctly scored, it creates a dictionary with the word:list pair that it was generated from.
    '''
    final_list = []
    used_sublists = []
    for sublist in wildcard_chars:
        for word in master_list:
            word_dict = character_dict(word)
            positive = 1
            for item in word_dict:
                if item not in sublist:
                    positive = 0
                elif word_dict[item] > sublist.count(item):
                    positive = 0
            if positive == 1:
                final_list.append(word)
                used_sublists.append(sublist)
                continue
    final_dict = {final_list[i] : used_sublists[i] for i in range(len(final_list))}
    return final_dict

# Matching processes

b = input_sorter(a)

data = data_cutter(sowpods, b)

c = wildcard_checker(b)

if '*' in b and not '?' in b:
    d = wildcard_match(data, c)
elif '?' in b and not '*' in b:
    d = wildcard_match(data, c)
elif '*' and '?' in b:
    d = wildcard_match(data, c)
else:
    d = match_words(data, c)

# Scoring Processes

if '*' in b and not '?' in b:
    e = wildcard_scorer(d, b)
elif '?' in b and not '*' in b:
    e = wildcard_scorer(d, b)
elif '*' and '?' in b:
    e = wildcard_scorer(d, b)
else:
    e = score_word(d)

# Print outputs

for item in sorted(e,key=lambda x:(-x[0],x[1])):
    print('({0}, {1})'.format(item[0],item[1]))
print("Total number of words:",len(e))

tot_time = time.time() - start
print('Total time was {} seconds'.format(tot_time))