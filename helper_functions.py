from turtle import distance
import nltk
import json
import re
import numpy as np
from collections import Counter
import Levenshtein
from nltk.tokenize import sent_tokenize, word_tokenize



nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def compare_str(s1,s2, threshold = 0.3):
    #Comparing different strings in order to not differentiate between two very similar strings.
    distance = Levenshtein.distance(s1,s2)
    base_length = len(s1)
    if(distance <= base_length * threshold ):
        return 1
    else:
        return 0

example_string = "Neil Armstrong went to the moon."

s1 = word_tokenize(example_string)

print(s1)

def extract_ne(quote):
    words = word_tokenize(quote)
    tags = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tags, binary=True)
    return set(
        " ".join(i[0] for i in t)
        for t in tree
        if hasattr(t, "label") and t.label() == "NE"
    )

    # tree.draw()

ne_set = extract_ne(example_string)

print(ne_set)