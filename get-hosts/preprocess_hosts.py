import spacy
from spacy.lang.en.stop_words import STOP_WORDS

import string
import re
import json


nlp = spacy.load('en_core_web_sm', disable=["parser"])
nlp.add_pipe('sentencizer')


def clean(tweet):
    nums_and_puncs = r"[0-9{}<>\-,:_\.=+#|\/@]"
    for_removal = (string.punctuation+'\"'+'\n' +
                   "“"+"…"+"RT"+"”")
    flag = re.MULTILINE

    # remove urls
    clean_tweet = re.sub(r"(\S*https?:\S*)", '', tweet, flags=flag)
    # remove punctuation from words
    clean_tweet = re.sub(nums_and_puncs, '', tweet, flags=flag)
    # remove stop words, lone punctuation, and retweet tag
    clean_tweet = " ".join([
        word for word in clean_tweet.split(' ') if word not in for_removal and word not in STOP_WORDS])

    return clean_tweet

def preprocess(path: str):
    with open(path) as f:
        print("reading json...")
        data = json.load(f)
        print("finished reading json...")
        tweets = [tweet_data['text'] for tweet_data in data]
        print("cleaning tweets...")
        cleaned_tweets = [clean(tweet) for tweet in tweets]
        print("finished cleaning...")
        print("piping tweets")
        return nlp.pipe(cleaned_tweets)
        
if __name__ == '__main__':
    preprocess('gg2015.json')
