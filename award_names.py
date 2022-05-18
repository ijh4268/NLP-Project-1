import nltk
import json
import re
import numpy as np
from collections import Counter

# sequence matcher similarity
# https://stackoverflow.com/questions/4802137/how-to-use-sequencematcher-to-find-similarity-between-two-strings


awards = []
candidates = {"best": []}

stop_punctuation_include = ['.','!','?',',']
stop_punctuation_uninclude = ['@','#']
stop_punctuation = stop_punctuation_include + stop_punctuation_uninclude
with open("pre_process_2013.json", "r") as file:
    content = json.load(file)
    for tweet in content:
        text = tweet['text']
        # parse expressions in tweet, add possible award names to candidates
        words = text.lower().split()
        #re.split(r' |,|!|;|?|.', text.lower())
        idx = words.index("best")
        #candidates["won"].append(words[idx+1:len(words)])
        stop_idx = len(words)-1 # index of the last word we include
        found_idx = False
        for i in range(idx+1, len(words)):
            for mark in stop_punctuation:
                if mark in words[i]:
                    if mark in stop_punctuation_include:
                        stop_idx = i
                        words[i] = words[i].replace(mark, "")
                    else:
                        stop_idx = i-1
                    found_idx = True
                    break
            if found_idx:
                break

        for i in range(idx+1, stop_idx+1):
            candidates["best"].append(" ".join(words[idx+1: i+1]))
        #candidates["best"].append(words[idx+1: stop_idx+1])

#print(candidates["best"][0:100])
occurence_count = Counter(candidates["best"])
most_frequent, temp = zip(*(occurence_count.most_common(100)))
#most_frequent = occurence_count.most_common(125)

eliminated = []
for i in range (len(most_frequent)):
    for j in range(i+1, len(most_frequent)):
        if most_frequent[i] in most_frequent[j]:
            eliminated.append(i)
        elif most_frequent[j] in most_frequent[i]:
            eliminated.append(j)
temp_awards = []
for i in range (len(most_frequent)):
    if i not in eliminated:
        temp_awards.append(most_frequent[i])


eliminated = set()
for i in range(len(temp_awards)):
    for j in range(i+1, len(temp_awards)):
        diff = difflib.SequenceMatcher(None, temp_awards[i], temp_awards[j])
        if diff.ratio() > 0.8: # similar
            eliminated.add(j)
awards = []
for i in range(len(temp_awards)):
    if i not in eliminated:
        awards.append(temp_awards[i])



