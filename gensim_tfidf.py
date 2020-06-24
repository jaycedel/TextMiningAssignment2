# https://www.tutorialspoint.com/gensim/gensim_creating_tf_idf_matrix.htm

import gensim
import pprint
from gensim import corpora, models
from gensim.utils import simple_preprocess
import numpy as np

doc_list = [
    "Hello, how are you?" "How do you do? Hey what are you doing? yes you What are you doing?"
]

mytext = "Hello, how are you?" "How do you do? Hey what are you doing? yes you What are you doing?"
doc_tokenized = [simple_preprocess(mytext)]
dictionary = corpora.Dictionary()
BoW_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in doc_tokenized]

tfidf = models.TfidfModel(BoW_corpus, smartirs='ntc')
for doc in tfidf[BoW_corpus]:
    for id,freq in doc:
        print(dictionary[id])
        print(np.around(freq,5))

    # Sort the doc for frequency: bow_doc
    #https://honingds.com/blog/natural-language-processing-with-python/
    bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)

    # Print the top 5 words of the document alongside the count
    for word_id, word_count in bow_doc[:1]:
        print(dictionary.get(word_id), word_count)