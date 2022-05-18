import nltk
import json
import re
import numpy as np
from collections import Counter, OrderedDict
import helper_functions

def award_winners(year):
    OFFICIAL_AWARDS_1315 = ['cecil b. demille award',
    'best motion picture - drama',
    'best performance by an actress in a motion picture - drama', 
    'best performance by an actor in a motion picture - drama',
    'best motion picture - comedy or musical',
    'best performance by an actress in a motion picture - comedy or musical',
    'best performance by an actor in a motion picture - comedy or musical',
    'best animated feature film',
    'best foreign language film',
    'best performance by an actress in a supporting role in a motion picture',
    'best performance by an actor in a supporting role in a motion picture',
    'best director - motion picture',
    'best screenplay - motion picture',
    'best original score - motion picture',
    'best original song - motion picture',
    'best television series - drama',
    'best performance by an actress in a television series - drama',
    'best performance by an actor in a television series - drama',
    'best television series - comedy or musical',
    'best performance by an actress in a television series - comedy or musical',
    'best performance by an actor in a television series - comedy or musical',
    'best mini-series or motion picture made for television',
    'best performance by an actress in a mini-series or motion picture made for television',
    'best performance by an actor in a mini-series or motion picture made for television',
    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
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
    name_matching['best performance by an actress in a television series - comedy or musical'] = ['best actress TV', 'best actress television']
    name_matching['best performance by an actor in a television series - comedy or musical'] = ['best actor TV', 'best actor television']
    name_matching['best mini-series or motion picture made for television'] = ['best TV show', 'best television show', 'best show']
    name_matching['best performance by an actress in a mini-series or motion picture made for television'] = ['best actress TV', 'best actress television']
    name_matching['best performance by an actor in a mini-series or motion picture made for television'] = ['best actor TV', 'best actor television']
    name_matching['best performance by an actress in a supporting role in a series, mini-series or motion picture made for television'] = ['best supporting actress']
    name_matching['best performance by an actor in a supporting role in a series, mini-series or motion picture made for television'] = ['best supporting actor']

    candidates = {"won": []}
    namedentities = {"won":[]}

    with open("pre_process_winners_" + str(year) + ".json", "r") as file:
    #with open("pre_process_winners_2013.json", "r") as file:
        content = json.load(file)
        for tweet in content:
            text = tweet[0]['text']
            # parse expressions in tweet, add possible award names to candidates
            words = text.lower().split()
            upperwords = text.split()
            try:
                won_idx = words.index("won")
                candidates["won"].append((" ".join(words[0: won_idx]), tweet[1], " ".join(upperwords[0: won_idx])))
                #candidates["won"].append((" ".join(words), tweet[1], " ".join(upperwords)))
            except:
                pass


    for i in range(0, len(candidates["won"])):
        ne = helper_functions.extract_ne(candidates["won"][i][2])
        ne_lst = list(ne)
        for j in range(len(ne_lst)):
            if ne_lst[j] != "RT" and ne_lst[j] != "Golden Globes" and ne_lst[j] != "Golden Globe":
                namedentities["won"].append((ne_lst[j], candidates["won"][i][1]))

    ne_counts = Counter(val[0] for val in namedentities["won"])
    most_frequent = sorted(namedentities["won"], key = lambda ele: ne_counts[ele[0]], reverse = True)
    res = list(OrderedDict.fromkeys(most_frequent))

    winners = {key: [] for key in OFFICIAL_AWARDS_1315}
    for i in range (len(res)):
        if year == 2013:
            if not winners[res[i][1]]: #and res[i][0] in nominees_2013[res[i][1]]:
                winners[res[i][1]] = res[i][0]
        else:
            if not winners[res[i][1]]:
                winners[res[i][1]] = res[i][0]

    #print(winners)
    return winners
