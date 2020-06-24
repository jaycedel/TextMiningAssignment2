#https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math

# %load_ext autotime

title = "stories"
alpha = 0.3


folders = [x[0] for x in os.walk(str(os.getcwd())+'/'+title+'/')]
print(folders)
folders[0] = folders[0][:len(folders[0])-1]

dataset = []

c = False

for i in folders:
    file = open(i + "/index.html", 'r')
    text = file.read().strip()
    file.close()

    file_name = re.findall('><A HREF="(.*)">', text)
    file_title = re.findall('<BR><TD> (.*)\n', text)

    if c == False:
        file_name = file_name[2:]
        c = True

    print(len(file_name), len(file_title))

    for j in range(len(file_name)):
        dataset.append((str(i) + "/" + str(file_name[j]), file_title[j]))

N = len (dataset)
def print_doc(id):
    print(dataset[id])
    file = open(dataset[id][0], 'r', encoding='cp1250')
    text = file.read().strip()
    file.close()
    print(text)

def convert_lower_case(data):
    return np.char.lower(data)

def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text

def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data

def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


def stemming(data):
    stemmer = PorterStemmer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text



def convert_numbers(data):
    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        try:
            w = num2words(int(w))
        except:
            a = 0
        new_text = new_text + " " + w
    new_text = np.char.replace(new_text, "-", " ")
    return new_text



def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data) #remove comma seperately
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = convert_numbers(data)
    data = stemming(data)
    data = remove_punctuation(data)
    data = convert_numbers(data)
    data = stemming(data) #needed again as we need to stem the words
    data = remove_punctuation(data) #needed again as num2word is giving few hypens and commas fourty-one
    data = remove_stop_words(data) #needed again as num2word is giving stop words 101 - one hundred and one
    return data



processed_text = []
processed_title = []

for i in dataset[:N]:
    file = open(i[0], 'r', encoding="utf8", errors='ignore')
    text = file.read().strip()
    file.close()

    processed_text.append(word_tokenize(str(preprocess(text))))
    processed_title.append(word_tokenize(str(preprocess(i[1]))))


#Calculating DF for all words
DF = {}

for i in range(N):
    tokens = processed_text[i]
    for w in tokens:
        try:
            DF[w].add(i)
        except:
            DF[w] = {i}

    tokens = processed_title[i]
    for w in tokens:
        try:
            DF[w].add(i)
        except:
            DF[w] = {i}
for i in DF:
    DF[i] = len(DF[i])



total_vocab_size = len(DF)

total_vocab = [x for x in DF]


def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c


#Calculating TF-IDF for body, we will consider this as the actual tf-idf as we will add the title weight to this.


doc = 0

tf_idf = {}

for i in range(N):

    tokens = processed_text[i]

    counter = Counter(tokens + processed_title[i])
    words_count = len(tokens + processed_title[i])

    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = np.log((N + 1) / (df + 1))

        tf_idf[doc, token] = tf * idf

    doc += 1


#Calculating TF-IDF for Title
doc = 0

tf_idf_title = {}

for i in range(N):

    tokens = processed_title[i]
    counter = Counter(tokens + processed_text[i])
    words_count = len(tokens + processed_text[i])

    for token in np.unique(tokens):
        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = np.log((N + 1) / (df + 1))  # numerator is added 1 to avoid negative values

        tf_idf_title[doc, token] = tf * idf

    doc += 1

#Merging the TF-IDF according to weights
for i in tf_idf:
    tf_idf[i] *= alpha

for i in tf_idf_title:
    tf_idf[i] = tf_idf_title[i]


#TF-IDF Matching Score Ranking
def matching_score(k, query):
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))

    print("Matching Score")
    print("\nQuery:", query)
    print("")
    print(tokens)

    query_weights = {}

    for key in tf_idf:

        if key[1] in tokens:
            try:
                query_weights[key[0]] += tf_idf[key]
            except:
                query_weights[key[0]] = tf_idf[key]

    query_weights = sorted(query_weights.items(), key=lambda x: x[1], reverse=True)

    print("")

    l = []

    for i in query_weights[:10]:
        l.append(i[0])

    print(l)

#TF-IDF Cosine Similarity Ranking
def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

#Vectorising tf-idf
D = np.zeros((N, total_vocab_size))
for i in tf_idf:
    try:
        ind = total_vocab.index(i[1])
        D[i[0]][ind] = tf_idf[i]
    except:
        pass


def gen_vector(tokens):
    Q = np.zeros((len(total_vocab)))

    counter = Counter(tokens)
    words_count = len(tokens)

    query_weights = {}

    for token in np.unique(tokens):

        tf = counter[token] / words_count
        df = doc_freq(token)
        idf = math.log((N + 1) / (df + 1))

        try:
            ind = total_vocab.index(token)
            Q[ind] = tf * idf
        except:
            pass
    return Q


def cosine_similarity(k, query):
    print("Cosine Similarity")
    preprocessed_query = preprocess(query)
    tokens = word_tokenize(str(preprocessed_query))

    print("\nQuery:", query)
    print("")
    print(tokens)

    d_cosines = []

    query_vector = gen_vector(tokens)

    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))

    out = np.array(d_cosines).argsort()[-k:][::-1]

    print("")

    print(out)
