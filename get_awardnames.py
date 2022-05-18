from xxlimited import new
import nltk
import json
import re
import numpy as np
from collections import Counter
import helper_functions as hp

def get_awardnames(year):
    if year == '2013':
        filename = "pre_process_2013.json"
    if year == '2015':
        filename = "pre_process_2015.json"
    candidates = {"best": []}

    stop_punctuation_include = ['.','!','?',',',':']
    stop_punctuation_uninclude = ['@','#']
    stop_punctuation = stop_punctuation_include + stop_punctuation_uninclude
    with open(filename, "r") as file:
        content = json.load(file)
        for tweet in content:
            text = tweet['text']
            # parse expressions in tweet, add possible award names to candidates
            words = text.lower().split()
            #re.split(r' |,|!|;|?|.', text.lower())
            if "won" in words:
                idx = words.index("won")
            

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
                    # if "rt" in words:
                    #     continue
                    candidates["best"].append(" ".join(words[idx+1: i+1]))

            if "wins" in words:
                idx = words.index("wins")
            

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
                    # if "rt" in words:
                    #     continue
                    candidates["best"].append(" ".join(words[idx+1: i+1]))
            elif "goes" in words:
                
                idx = words.index("goes")

                stop_idx = idx -1 # index of the last word we include
                found_idx = False
                for i in range(0, idx-1):
                    for mark in stop_punctuation:
                        if mark in words[idx - 1-i]:
                            if mark in stop_punctuation_include:
                                stop_idx = idx-1-i
                                words[i] = words[i].replace(mark, "")
                            else:
                                stop_idx = 0
                            found_idx = True
                            break
                    if found_idx:
                        break
                for i in range(stop_idx, idx):
                    if "rt" in words:
                        continue
                    candidates["best"].append(" ".join(words[stop_idx : stop_idx+i]))

    occurence_count = Counter(candidates["best"])
    most_frequent, temp = zip(*(occurence_count.most_common(100)))


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

    unique_marker = [1 for i in range(len(awards)) ]
    new_awards = []
            


    for i in range(len(awards)):
        for j in range(i+1, len(awards)):
            
            if(hp.compare_str(awards[i],awards[j],threshold=0.4) == 1):

                unique_marker[j] = 0


    for i in range(len(awards)):
        if unique_marker[i] == 1:
            if("for" not in awards[i]):
                # if("goes" not in awards[i]):
                    new_awards.append(awards[i])




    print(new_awards)
    
    """
    flattened = [word for candidate in candidates["best"] for word in candidate]
    print(flattened[:10])
    monster_str = ' '.join(flattened)
    print("monster str: ", monster_str[:100])
    text = nltk.Text(monster_str)
    collocations = text.collocations()
    print("\ncollocations: ", collocations[:100])
    """
    return(awards)

