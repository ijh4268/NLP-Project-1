'''Version 0.35'''
import nltk
import json
import re
import spacy
import numpy as np
from collections import Counter
import difflib
import pre_process_winners
import award_winners
import award_nominees
import award_presenters
import pre_process
import best_dressed
import get_hosts as gh
import preprocess_hosts

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = gh.get_hosts(year)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = []
    candidates = {"best": []}

    stop_punctuation_include = ['.','!','?',',']
    stop_punctuation_uninclude = ['@','#']
    stop_punctuation = stop_punctuation_include + stop_punctuation_uninclude
    with open("pre_process_" +str(year) + ".json", "r") as file:
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
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    #nominees = {key: [] for key in OFFICIAL_AWARDS_1315}
    return award_nominees.award_nominees(year)

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    #winners = {key: [] for key in OFFICIAL_AWARDS_1315}
    return award_winners.award_winners(year)

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    #presenters = {key: [] for key in OFFICIAL_AWARDS_1315}
    return award_presenters.award_presenters(year)

def get_best_dressed(year):
    return best_dressed.best_dressed(year)

def pre_ceremony(year):
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    """
    with open("gg2013.json", "r") as file:
        s = json.load(file)
        for i in range(len(s)):
            s[i].pop('id')
            s[i].pop('user')
        json_str = json.dumps(s)
        out = open("pre_process_2013.json", "w")
        out.write(json_str)
        out.close()

    with open("gg2015.json", "r") as file:
        s = json.load(file)
        for i in range(len(s)):
            s[i].pop('id')
            s[i].pop('user')
        json_str = json.dumps(s)
        out = open("pre_process_2015.json", "w")
        out.write(json_str)
        out.close()
    """
    spacy.download('en_web_core_sm')
    pre_process.pre_process(year)
    pre_process_winners.pre_process_winners(year)
    preprocess_hosts.preprocess(year)

    print("Pre-ceremony processing complete.")
    return

def main(year):
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    hosts = get_hosts(year)
    awards = get_awards(year)
    winners = get_winner(year)
    nominees = get_nominees(year)
    presenters = get_presenters(year)
    best_dress = get_best_dressed(year)

    print("Year: "+ str(year) + "Golden Globes")
    print("\nHosts: " + (" ".join(hosts)))
    print("\nAwards: " + (" ".join(awards)))

    for i in winners.keys():
        print("\nAward: " + i)
        print("Presenters: " + ("".join(presenters[i])))
        print("Nominees: " + ("".join(nominees[i])))
        print("Winners: " + ("".join(winners[i])))

    print("\nBest Dressed: " + best_dress["Best Dressed"])
    print("Worst Dressed: " + best_dress["Worst Dressed"])

    return

if __name__ == '__main__':
    pre_ceremony(2013)
    pre_ceremony(2015)
    main(2013)
    main(2015)
