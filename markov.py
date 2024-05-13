"""Bare-bones Markov text generator."""

import nltk
import random

"""Implement a function of the form finish_sentence(sentence, n, corpus, randomize=False) that takes four arguments:
 1. a sentence [list of tokens] that we're trying to build on, .
 2. n [int], the length of n-grams to use for prediction, and . 
 3. a source corpus [list of tokens] . 
 4. a flag indicating whether the process should be randomize [bool]
   and returns an extended sentence until the first . , ? , or ! is found OR until it has 10 total tokens. 
If the input flag randomize is false, choose at each step the single most probable next token. 
When two tokens are equally probable, choose the one that occurs first in the corpus. 
This is called a deterministic process. If randomize is true, draw the next word randomly from the appropriate distribution. 
Use stupid backoff ( α = 1 ) and no smoothing."""

corpus = nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())


def count_ngrams(lst):
    """function to count repeated elements in list."""
    element_count = {}
    for item in lst:
        if item in element_count:
            element_count[item] += 1
        else:
            element_count[item] = 1
    return element_count


def new_dic(old_dic, sentence, n):
    """fun to  build new dictionary with matching ngrams to sentence"""
    n_d = {}
    for key, value in old_dic.items():
        # print(key[:-1])
        if key[:-1] == tuple(sentence[-(n - 1) :]):
            n_d[key] = value
    return n_d


"""Function to build next_word.
Selects next_word from highest count using new dictionary, if no max count, keeps first element
DETERMINISTIC NEXT WORD
if randomize is false, select highest prob; if repeated keep first match
1. creat ngrams of n-1 size plus one word(next word)
caveat:
2. create dictionary of previuous ngrams and their frequency: n_dict key(ngram+next word):value(frequency of ngram)
3. use this dictionary to find the next word, the highest value is selected, if two high values exist, keep the first
 caveat: use recursive function if first ngram bears no matches
"""


def next_word_d(corpus, sentence, n):
    if n == 1:
        n_grams_d = count_ngrams([(item) for item in corpus])
        max_val = max(n_grams_d.values())
        keys_max_val = [key for key, value in n_grams_d.items() if value == max_val]
        return keys_max_val[0]
    # create ngrams list according to sentence and n an adding next word
    n_grams = [tuple(corpus[i : i + (n - 1) + 1]) for i in range(len(corpus) - (n - 1))]
    # create dict with previous count ofngrams
    n_dict = new_dic(count_ngrams(n_grams), sentence, n)
    if not n_dict:
        return next_word_d(corpus, sentence, n - 1)
    max_val = max(n_dict.values())  # Find the highest value in the dictionary
    keys_max_val = [key for key, value in n_dict.items() if value == max_val]
    return keys_max_val[0][
        -1
    ]  # Return last value from key with the highest value, which is the nextword


def next_word_s(corpus, sentence, n):
    if n == 1:
        n_grams_d = count_ngrams([(item) for item in corpus])
        max_val = max(n_grams_d.values())
        keys_max_val = [key for key, value in n_grams_d.items() if value == max_val]
        return keys_max_val[0]
    # create ngrams list according to sentence and n an adding next word
    n_grams = [tuple(corpus[i : i + (n - 1) + 1]) for i in range(len(corpus) - (n - 1))]
    # create dict with previous count ofngrams
    n_dict = new_dic(count_ngrams(n_grams), sentence, n)
    if not n_dict:
        return next_word_d(corpus, sentence, n - 1)
    # create new dictionary of only possible next word (last element of key tuple) and value
    weighted_dic = {key[-1]: value for key, value in n_dict.items()}
    # create list of weighted next_words using previous dict
    weighted_list = [
        item for item, weight in weighted_dic.items() for _ in range(weight)
    ]
    # use random choice to select one word from weighted list
    random_word = random.choice(weighted_list)
    return random_word


def finish_sentence(sentence, n, corpus, randomize):
    lst_enpo = [".", "?", "!"]
    while (len(sentence) < 10) and (sentence[-1] not in lst_enpo):
        # use next_word determenistic when randomize=FALSE and next_word stochastic when randomize=TRUE
        if randomize == False:
            la_nueva = next_word_d(corpus, sentence, n)
        else:
            la_nueva = next_word_s(corpus, sentence, n)
        sentence.append(la_nueva)
    return sentence


if __name__ == "__main__":
    """Test Cases."""

    corpus_j = nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())

    # finish_sentence(["I", "like","cakes"], 2, corpus_j, False)

    ["was", "not", "in"]
    ["not", "in", "the"]

    next_word_d(corpus_j, ["she", "was", "not"], 1)

    finish_sentence(["Dani", "is", "in"], 2, corpus_j, False)

    finish_sentence(["she", "was", "not"], 1, corpus_j, False)

    finish_sentence(["she", "was", "not"], 3, corpus_j, True)

    finish_sentence(["Robot"], 3, corpus_j, False)

    finish_sentence(["Robot"], 2, corpus_j, False)
