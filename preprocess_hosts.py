import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.tokens import DocBin

from tqdm import tqdm

import string
import re
import json


nlp = spacy.load('en_core_web_sm', disable=["parser"])
nlp.add_pipe('sentencizer')


def clean(tweet):
    nums_and_puncs = r"[0-9{}<>\-,:_\.=+#|\/@]"
    for_removal = (string.punctuation+'\"'+'\n' +
                   "“"+"…"+"RT"+"”"+"'s")
    flag = re.MULTILINE

    # remove urls
    clean_tweet = re.sub(r"(\S*https?:\S*)", '', tweet, flags=flag)
    # remove punctuation from words
    clean_tweet = re.sub(nums_and_puncs, '', tweet, flags=flag)
    # remove stop words, lone punctuation, and retweet tag
    clean_tweet = " ".join([
        word for word in clean_tweet.split(' ') if word not in for_removal and word not in STOP_WORDS])
    return clean_tweet


def save(docs, year):
    doc_bin = DocBin(docs=docs)
    doc_bin.to_disk(f"{year}.spacy")


def preprocess(year):
    with open(f"gg{year}.json") as f:
        print(f"starting preprocessing for gg{year}...")
        print("reading json...")
        data = json.load(f)
        print("finished reading json...")

        tweets = [tweet_data['text'] for tweet_data in data]
        print("cleaning tweets...")
        cleaned_tweets = [clean(tweet)
                          for tweet in tqdm(tweets, total=len(tweets))]
        print("finished cleaning...")

        print("processing tweets...")
        docs = [doc for doc in tqdm(
            nlp.pipe(cleaned_tweets, n_process=8), total=len(cleaned_tweets))]
        print("saving processed data...")
        save(docs, year)
        print(f"saved as {year}.spacy")

