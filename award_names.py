import nltk
import json
import re
import numpy as np
from collections import Counter

candidates = {"best": []}

stop_punctuation = ['.','!','?',',','@','#']
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
                    stop_idx = i
                    found_idx = True
                    break
            if found_idx:
                break

        #for i in range(idx+1, stop_idx+1):
            #candidates["best"].append(words[idx+1: i+1])
        candidates["best"].append(words[idx+1: stop_idx+1])

# now, to compare the candidates and find the most likely ones
flattened = [word for candidate in candidates["best"] for word in candidate]
print(flattened[:10])
monster_str = ' '.join(flattened)
print("monster str: ", monster_str[:100])
text = nltk.Text(monster_str)
collocations = text.collocations()
print("\ncollocations: ", collocations[:100])

print(candidates["best"][:10])
print(len(candidates["best"]))
unique = np.unique(candidates["best"])
print(zip(unique[:10]))


