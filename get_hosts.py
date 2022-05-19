import spacy
import nltk
from spacy.tokens import DocBin
from difflib import get_close_matches
from tqdm import tqdm

nlp = spacy.load('en_core_web_sm')


def load(year):
    doc_bin = DocBin().from_disk(f"{year}.spacy")
    return list(doc_bin.get_docs(nlp.vocab))


def get_hosts(year):
    print("loading data...")
    tweets = load(year)
    print('finished loading...')
    print('searching for hosts...')
    result = find_hosts(tweets)
    print(result)
    return result


def find_hosts(tweets):
    # get tweets that only mention the word host
    only_host = [
        tweet for tweet in tweets for token in tweet if token.text.startswith('host')]
    # get all the PERSON entities that appear in those tweets
    people = [ent for doc in only_host for ent in doc.ents if ent.label_ == 'PERSON']
    # get frequency distribution
    most_common_people = nltk.FreqDist(
        person.text.lower() for person in people)
    # find most similar words in list of most common people
    similarities = [get_close_matches(
        word, most_common_people, cutoff=0.8) for word in most_common_people]
    # find the longest lists of similarities
    names_longest_similarities = [lst[0] for lst in similarities if len(
        lst) == len(max(similarities, key=len))]
    similarities = [get_close_matches(
        word, most_common_people, n=3, cutoff=0.8) for word in most_common_people]
    # find the longest lists of similarities
    names_longest_similarities = [lst[0] for lst in similarities if len(
        lst) == len(max(similarities, key=len))]
    # widdle down the similarities to just one item
    similarities = [get_close_matches(
        word, names_longest_similarities, n=1, cutoff=0.8) for word in names_longest_similarities]
    # get individual words
    to_words = [word.split(' ')
                for similarity in similarities for word in similarity]
    # get the first names in those words
    first_names = [words[0] for words in to_words if len(words) == 2]
    # get most common occurences
    most_common_first_names = nltk.FreqDist(name for name in first_names)
    top_10 = [name[0] for name in most_common_first_names.most_common(10)]
    occurences = {name: [occurence for occurence in to_words for word in occurence if name in occurence or word.startswith(
        name)] for name in top_10}
    # rank most common occurences
    ranked = sorted(occurences, key=lambda i: len(occurences[i]), reverse=True)
    host1, host2 = tuple(ranked[:2])
    # find potential last names based on the first names found
    potential_last_names = {host1: [words[words.index(host1)+1] for words in to_words if host1 in words
                                    and words.index(host1)+1 < len(words)
                                    and words[words.index(host1)+1] != host2
                                    and len(words) >= 2],
                            host2: [words[words.index(host2)+1] for words in to_words if host2 in words
                                    and words.index(host2)+1 < len(words)
                                    and words[words.index(host2)+1] != host1
                                    and len(words) >= 2]}
    # get the most common last names
    most_common_last_names = {host1: nltk.FreqDist(potential_last_names[host1]).most_common(1)[0][0],
                              host2: nltk.FreqDist(potential_last_names[host2]).most_common(1)[0][0]}
    print("done")
    # put together first names and last names and return
    return [" ".join([key, value]) for key, value in most_common_last_names.items()]
