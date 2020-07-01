from gensim.corpora import Dictionary
from nltk import word_tokenize
from nltk.corpus import stopwords
import os
import xml.etree.ElementTree as ET
import html.parser
from collections import defaultdict
import itertools
import numpy as np


# CLEAN TEXT CONTENTS REMOVING SPECIAL CHARACTERS WHICH CAUSE SOME XML PARSING, AND STOP WORDS


def clean_xml_tags(text):
    decodedContent = html.unescape(text)
    decodedContent = decodedContent.replace(" & ", " ")
    decodedContent = decodedContent.replace("&", "")
    decodedContent = decodedContent.replace("<>", " ")
    decodedContent = decodedContent.replace("&lt;", " ")
    decodedContent = decodedContent.replace("&gt;", " ")

    return decodedContent


# REPLACE NON TOPIC WORDS
def remove_non_topic_word(text):
    decodedContent = text.replace(" i ", " ")
    decodedContent = text.replace(".I ", " ")
    decodedContent = decodedContent.replace(" MR ", " ")
    decodedContent = decodedContent.replace(" the ", " ")
    decodedContent = decodedContent.replace(".The ", " ")
    decodedContent = decodedContent.replace("The", " ")
    decodedContent = decodedContent.replace(" it ", " ")
    decodedContent = decodedContent.replace("'s", " ")
    decodedContent = decodedContent.replace("one", " ")
    decodedContent = decodedContent.replace("'m", " ")
    decodedContent = decodedContent.replace("via", " ")
    decodedContent = decodedContent.replace("like", " ")
    decodedContent = decodedContent.replace("urlLink", " ")
    # REMOVE STOP WORDS  https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
    for sw in stop_words:
        decodedContent = decodedContent.replace(' ' + sw + ' ', " ")

    return decodedContent


# SPLIT FILENAME AND RETURNS {'GENDER': 'FEMALE', 'AGE': 26, 'INTEREST': 'INTERNET'}
def parse_filename(filename):
    splittedFilename = filename.split(".")
    return {'GENDER': splittedFilename[1].upper(), 'AGE': int(splittedFilename[2]),
            'INTEREST': splittedFilename[3].upper()}


# https://www.tutorialspoint.com/gensim/gensim_creating_tf_idf_matrix.htm
# https://honingds.com/blog/natural-language-processing-with-python/
def ner_post_parsing(classification, blogs):
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


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data


# START OF MAIN PROGRAM
stop_words = set(stopwords.words('english'))
path = "../blogs2"  # FOLDER OF WHERE THE FILES ARE

blogs_male = ""
blogs_female = ""
blogs_below21 = ""
blogs_above20 = ""
blog_text = ""

blogs = []
blog_male_list = []
blog_female_list = []
blog_below21_list = []
blog_above20_list = []

for filename in os.listdir(path):
    if not filename.endswith('.xml'):
        continue

    currentBlogger = parse_filename(filename)
    # GET THE FULLNAME
    fullname = os.path.join(path, filename)
    try:
        # GET CONTENT OF THE XML FILE
        # https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in/42340744
        with open(fullname, encoding="utf8", errors='ignore') as f:
            text = f.read()

        cleanText = clean_xml_tags(text)
        tree = ET.fromstring(cleanText)

        # GET ALL POST ELEMENT TAGS
        for elem in tree.iter():
            if elem.tag == 'post':
                cleanPost = str(remove_punctuation(elem.text))
                cleanPost = remove_non_topic_word(cleanPost)
                blogs.append(cleanPost)
                if currentBlogger['GENDER'] == 'MALE':
                    blog_male_list.append(cleanPost)
                if currentBlogger['GENDER'] == 'FEMALE':
                    blog_female_list.append(cleanPost)
                # Less Than 20 Counter
                if currentBlogger['AGE'] <= 20:
                    blog_below21_list.append(cleanPost)
                # More Than 20 Counter
                if currentBlogger['AGE'] > 20:
                    blog_above20_list.append(cleanPost)

    except Exception as e:
        # print("Unexpected error on " + fullname + ":", e)
        pass

ner_post_parsing("Everyone", blogs)
ner_post_parsing("Male", blog_male_list)
ner_post_parsing("Female", blog_male_list)
ner_post_parsing("Below 21", blog_below21_list)
ner_post_parsing("Above 20", blog_above20_list)
