import nltk
import json
import re
import numpy as np
import spacy
from collections import Counter, OrderedDict
import helper_functions
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load('en_core_web_sm')

def best_dressed(year):
    candidates = {"outfit": []}
    namedentities = {"outfit":[]}

    with open(f"gg{year}.json", "r") as file:
    #with open("pre_process_winners_2013.json", "r") as file:
        content = json.load(file)
        for tweet in content:
            text = tweet['text']
            # parse expressions in tweet, add possible award names to candidates
            words = text.lower().split()
            upperwords = text.split()
            try:
                outfit_idx = words.index("outfit")
                #candidates["won"].append((" ".join(words[0: won_idx]), tweet[1], " ".join(upperwords[0: won_idx])))
                candidates["outfit"].append((" ".join(words), " ".join(upperwords)))
            except:
                pass

    for i in range(0, len(candidates["outfit"])):
        docs = nlp.pipe(candidates["outfit"][i])
        names = [str(ent) for doc in docs for ent in doc.ents if ent.label_ == 'PERSON']
        unique = np.unique(names)
        for j in range(len(unique)):
            namedentities["outfit"].append((unique[j], candidates["outfit"][i][0]))

    print(namedentities["outfit"])

    cumulative_sentiment = {}
    analyzer = SentimentIntensityAnalyzer()
    for ne in namedentities["outfit"]:
        vs = analyzer.polarity_scores(ne[1])
        if ne[0] not in cumulative_sentiment.keys():
            cumulative_sentiment[ne[0]] = vs["compound"]
        else:
            cumulative_sentiment[ne[0]] += vs["compound"]
        
    print(cumulative_sentiment)

    best_dressed = max(cumulative_sentiment, key=cumulative_sentiment.get)
    worst_dressed = min(cumulative_sentiment, key=cumulative_sentiment.get)
    result = {"Best Dressed": best_dressed, "Worst Dressed": worst_dressed}
    print(result)

    return result
