from preprocess_hosts import preprocess
import nltk
from difflib import get_close_matches

tweets = list(preprocess('gg2013.json'))
print('finished piping...')
print('searching for hosts...')
# get tweets that only mention the word host
only_host = [
    tweet for tweet in tweets for token in tweet if token.text == 'host']
# get all the PERSON entities that appear in those tweets
people = [ent for doc in only_host for ent in doc.ents if ent.label_ == 'PERSON']
# get frequency distribution
most_common_people = nltk.FreqDist(person.text.lower() for person in people)
# find most similar words in list of most common people
similarities = [get_close_matches(word, most_common_people, cutoff=0.8) for word in most_common_people]
# find the longest lists of similarities
longest_similarities = [lst for lst in similarities if len(lst) == len(max(similarities, key=len))]
print(longest_similarities)


