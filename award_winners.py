import nltk
import json
import re
import numpy as np
from collections import Counter
import helper_functions

def award_winners(): 
    OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    name_matching = {}
    name_matching['cecil b. demille award'] = ['demille award']
    name_matching['best motion picture - drama'] = ['best picture', 'best drama']
    name_matching['best performance by an actress in a motion picture - drama'] = ['best actress drama']
    name_matching['best performance by an actor in a motion picture - drama'] = ['best actor drama']
    name_matching['best motion picture - comedy or musical'] = ['best picture', 'best comedy', 'best musical']
    name_matching['best performance by an actress in a motion picture - comedy or musical'] = ['best actress comedy', 'best actress musical', 'best comedy actress', 'best musical actress']
    name_matching['best performance by an actor in a motion picture - comedy or musical'] = ['best actor comedy', 'best actor musical', 'best comedy actor', 'best musical actor']
    name_matching['best animated feature film'] = ['best animated']
    name_matching['best foreign language film'] = ['best foreign']
    name_matching['best performance by an actress in a supporting role in a motion picture'] = ['best supporting actress']
    name_matching['best performance by an actor in a supporting role in a motion picture'] = ['best supporting actor']
    name_matching['best director - motion picture'] = ['best director']
    name_matching['best screenplay - motion picture'] = ['best screenplay']
    name_matching['best original score - motion picture'] = ['best score', 'best original score']
    name_matching['best original song - motion picture'] = ['best song', 'best original song']
    name_matching['best television series - drama'] = ['best television series', 'best TV drama']
    name_matching['best performance by an actress in a television series - drama'] = ['best actress TV drama']
    name_matching['best performance by an actor in a television series - drama'] = ['best actor TV drama']
    name_matching['best television series - comedy or musical'] = ['best television series', 'best TV comedy', 'best TV musical']
    name_matching['best director - motion picture'] = ['best director']
    name_matching['best television series - comedy or musical'] = ['best director']
    name_matching['best performance by an actress in a television series - comedy or musical'] = ['best actress TV', 'best actress television']
    name_matching['best performance by an actor in a television series - comedy or musical'] = ['best actor TV', 'best actor television']
    name_matching['best mini-series or motion picture made for television'] = ['best TV show', 'best television show', 'best show']
    name_matching['best performance by an actress in a mini-series or motion picture made for television'] = ['best actress TV', 'best actress television']
    name_matching['best performance by an actor in a mini-series or motion picture made for television'] = ['best actor TV', 'best actor television']
    name_matching['best performance by an actress in a supporting role in a series, mini-series or motion picture made for television'] = ['best supporting actress']
    name_matching['best performance by an actor in a supporting role in a series, mini-series or motion picture made for television'] = ['best supporting actor']

    candidates = {"won": []}

    stop_punctuation_include = ['.','!','?',',']
    stop_punctuation_uninclude = ['@','#']
    stop_punctuation = stop_punctuation_include + stop_punctuation_uninclude
    with open("pre_process_winners_2013.json", "r") as file:
        content = json.load(file)
        for tweet in content:
            text = tweet[0]['text']
            # parse expressions in tweet, add possible award names to candidates
            words = text.lower().split()
            #re.split(r' |,|!|;|?|.', text.lower())
            try:
                idx = words.index("won")
            except:
                pass
            else:
                for i in range(1, idx):
                    candidates["won"].append((" ".join(words[0: i]), tweet[1]))


    # find the most common candidates
    #print(candidates["won"])
    #print(len(candidates["won"]))
    occurence_count = Counter(candidates["won"])
    most_frequent, temp = zip(*(occurence_count.most_common(100)))
    #most_frequent = occurence_count.most_common(100)
    print(most_frequent)

    # substring elimination
    eliminated = []
    for i in range (len(most_frequent)):
        for j in range(i+1, len(most_frequent)):
            if most_frequent[i][0] in most_frequent[j][0]:
                eliminated.append(i)
            elif most_frequent[j][0] in most_frequent[i][0]:
                eliminated.append(j)

    winners = {key: [] for key in OFFICIAL_AWARDS_1315}
    for i in range (len(most_frequent)):
        if i not in eliminated:
            ne = helper_functions.extract_ne(most_frequent[i][0])
            #print(ne)
            ne_lst = list(ne)
            if len(ne_lst) > 0:
               winners[most_frequent[i][1]] = ne_lst[0]
            else:
                winners[most_frequent[i][1]] = most_frequent[i][0]

    print(winners)
    return winners
