import nltk
import json
import re
import numpy as np
from collections import Counter

candidates = {"won": []}
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

stop_punctuation_include = ['.','!','?',',']
stop_punctuation_uninclude = ['@','#']
stop_punctuation = stop_punctuation_include + stop_punctuation_uninclude
with open("pre_process_winners_2013.json", "r") as file:
    content = json.load(file)
    for tweet in content:
        text = tweet['text']
        # parse expressions in tweet, add possible award names to candidates
        words = text.lower().split()
        #re.split(r' |,|!|;|?|.', text.lower())
        try:
            idx = words.index("won")
        except:
            pass
        else:
            for i in range(1, idx):
                candidates["won"].append(" ".join(words[0: i]))

        #candidates["best"].append(words[idx+1: stop_idx+1])

print(candidates["won"])
occurence_count = Counter(candidates["won"])
most_frequent, temp = zip(*(occurence_count.most_common(100)))
#most_frequent = occurence_count.most_common(125)
#print(most_frequent)

eliminated = []
for i in range (len(most_frequent)):
    for j in range(i+1, len(most_frequent)):
        if most_frequent[i] in most_frequent[j]:
            eliminated.append(i)
        elif most_frequent[j] in most_frequent[i]:
            eliminated.append(j)
awards = []
for i in range (len(most_frequent)):
    if i not in eliminated:
        awards.append(most_frequent[i])

print(awards)
