#https://medium.com/@pemagrg/magic-of-tf-idf-202649d39c2f

import pandas as pd
import sklearn as sk
import math
import nltk
from nltk.corpus import stopwords

set(stopwords.words('english'))

def computeTF(wordDict, doc):
    tfDict = {}
    corpusCount = len(doc)
    for word, count in wordDict.items():
        tfDict[word] = count / float(corpusCount)
    return (tfDict)


def computeIDF(docList):
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / (float(val) + 1))

    return (idfDict)


def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return (tfidf)

def create_word_dict(total, sentence):
    wordDict = dict.fromkeys(total, 0)
    for word in sentence:
        wordDict[word] += 1
    return wordDict

sentence1 = "Go until jurong point, crazy.. Available only in bugis n great world la e buffet... Cine there got amore wat..."
sentence2 = "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's"

sentence1_list = nltk.word_tokenize(sentence1)
sentence2_list = nltk.word_tokenize(sentence2)
total = set(sentence1_list).union(set(sentence2_list))
print('sentence 1 list')
print(sentence1_list)
print('sentence 2 list')
print(sentence2_list)
print("Total")
print(total)


wordDictA = create_word_dict(total, sentence1_list)
wordDictB = create_word_dict(total, sentence2_list)

print(wordDictA)
print()
print(wordDictB)

tfFirst = computeTF(wordDictA, sentence1_list)
tfSecond = computeTF(wordDictB, sentence2_list)
print("TERM FREQUENCY OF SENTENCE1:\n", tfFirst)
print()
print("TERM FREQUENCY OF SENTENCE2:\n", tfSecond)

idfs = computeIDF([wordDictA, wordDictB])

idfFirst = computeTFIDF(tfFirst, idfs)
idfSecond = computeTFIDF(tfSecond, idfs)
print(idfFirst)
print()
print(idfSecond)

# putting it in a dataframe
idf = pd.DataFrame([idfFirst, idfSecond])
idf.head()
