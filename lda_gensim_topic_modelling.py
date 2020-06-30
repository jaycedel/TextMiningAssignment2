# https://www.tutorialspoint.com/gensim/gensim_creating_tf_idf_matrix.htm
# https://honingds.com/blog/natural-language-processing-with-python/

import itertools
from collections import defaultdict

from gensim.corpora import Dictionary
from nltk import word_tokenize


def lda_gensim_parse_post(classification, blogs):
    tokenized_docs = [word_tokenize(doc) for doc in blogs]
    dictionary = Dictionary(tokenized_docs)
    bag_of_words_corpus = [dictionary.doc2bow(tokenized_doc) for tokenized_doc in tokenized_docs]

    total_word_count = defaultdict(int)
    for word_id, word_count in itertools.chain.from_iterable(bag_of_words_corpus):
        total_word_count[word_id] += word_count

    # Create a sorted list from the defaultdict: sorted_word_count
    sorted_word_count = sorted(total_word_count.items(), key=lambda w: w[1], reverse=True)

    # Print the top 1 words across all documents alongside the count
    for word_id, word_count in sorted_word_count[:1]:
        print(classification + " is talking about '" + str(dictionary.get(word_id)) + "', with " + str(
            word_count) + " occurence")
