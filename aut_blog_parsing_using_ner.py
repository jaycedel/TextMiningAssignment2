# https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089
# https://github.com/susanli2016/NLP-with-Python/blob/master/NER_NLTK_Spacy.ipynb

import os
import xml.etree.ElementTree as ET
import html.parser
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist


# GET THE OBJECT OR THING ON THE BLOG POST AND RETURN THE OBJECT
def parseBlog(txt):
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if chunk.label() in topics:
                    keyValue = topics[chunk.label()]
                    if keyValue is not None:
                        # ADD THE VALUE LIST TO A PREVIOUSLY CREATED TOPIC WITH KEY chunk.label()
                        keyValue.append(' '.join(c[0] for c in chunk))
                        topics[chunk.label()] = keyValue
                else:
                    # CREATE A NEW TOPIC KEY chunk.label() WITH VALUE COMING FROM chunk
                    topics[chunk.label()] = [' '.join(c[0] for c in chunk)]


# CLEAN TEXT CONTENTS REMOVING SPECIAL CHARACTERS WHICH CAUSE SOME XML PARSING, AND STOP WORDS
def preProcessContent(text):
    decodedContent = html.unescape(text)
    # print(decodedContent)
    decodedContent = decodedContent.replace(" & ", " ")
    decodedContent = decodedContent.replace("&", "")
    decodedContent = decodedContent.replace("<>", " ")
    decodedContent = decodedContent.replace("&lt;", " ")
    decodedContent = decodedContent.replace("&gt;", " ")
    decodedContent = decodedContent.replace("urlLink", "")
    decodedContent = decodedContent.replace(" I ", " ")
    decodedContent = decodedContent.replace(" MR ", " ")
    # REMOVE STOP WORDS  https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
    for sw in stop_words:
        # print(sw)
        decodedContent = decodedContent.replace(' ' + sw + ' ', " ")

    return decodedContent


# SPLIT FILENAME AND RETURNS {'GENDER': 'FEMALE', 'AGE': 26, 'INTEREST': 'INTERNET'}
def parseFileName(filename):
    splittedFilename = filename.split(".")
    if splittedFilename[1] in gender:
        gender[splittedFilename[1]] += 1
    else:
        gender[splittedFilename[1]] = 1

    if splittedFilename[2] in age:
        age[splittedFilename[2]] += 1
    else:
        age[splittedFilename[2]] = 1

    if splittedFilename[3] in interest:
        interest[splittedFilename[3]] += 1
    else:
        interest[splittedFilename[3]] = 1

    if splittedFilename[4] in zodiac:
        zodiac[splittedFilename[4]] += 1
    else:
        zodiac[splittedFilename[4]] = 1

    # currentBlogger = {'GENDER': splittedFilename[1].upper(), 'AGE': int(splittedFilename[2]),
    #                   'INTEREST': splittedFilename[3].upper()}

    return {'GENDER': splittedFilename[1].upper(), 'AGE': int(splittedFilename[2]),
            'INTEREST': splittedFilename[3].upper()}


# MAIN CODE
# REMOVE NOISE IN THE TEXT
stop_words = set(stopwords.words("english"))

maleCount = 0
femaleCount = 0

path = "../blogs2"  # FOLDER OF WHERE THE FILES ARE
demographics = {}
gender = {}
age = {}
interest = {}
zodiac = {}
topics = {}

# VARIABLES USED FOR MALE COUNTER
male_key_person = []
male_key_gpe = []
male_key_gsp = []
male_key_facility = []
male_key_organization = []

# VARIABLES USED FOR FEMALE COUNTER
female_key_person = []
female_key_gpe = []
female_key_gsp = []
female_key_facility = []
female_key_organization = []

# VARIABLES USED FOR BELOW 20 COUNTER
below20_key_person = []
below20_key_gpe = []
below20_key_gsp = []
below20_key_facility = []
below20_key_organization = []

# VARIABLES USED FOR ABOVE 20 COUNTER
above20_key_person = []
above20_key_gpe = []
above20_key_gsp = []
above20_key_facility = []
above20_key_organization = []

# VARIABLES USED FOR ALL
key_person = []
key_gpe = []
key_gsp = []
key_facility = []
key_organization = []


for filename in os.listdir(path):
    if not filename.endswith('.xml'):
        continue

    topics.clear()
    currentBlogger = parseFileName(filename)

    # GET THE FULLNAME
    fullname = os.path.join(path, filename)

    try:
        # GET CONTENT OF THE XML FILE
        # https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in/42340744
        with open(fullname, encoding="utf8", errors='ignore') as f:
            text = f.read()

        cleanText = preProcessContent(text)
        tree = ET.fromstring(cleanText)

        # GET ALL POST ELEMENT TAGS
        for elem in tree.iter():
            if elem.tag == 'post':
                parseBlog(elem.text.upper())  # MAKE TEXT UPPER

        # CHECK THE TOPIC AND SUBJECT ENTERED IN THE BLOG POST
        # DEBUGGIN PURPOSES
        # for keyTopic in topics:
        #     print(keyTopic, '->', topics[keyTopic])

        # Male Counter
        if currentBlogger['GENDER'] == 'MALE':
            if 'PERSON' in topics:
                male_key_person += topics['PERSON']
            if 'GPE' in topics:
                male_key_gpe += topics['GPE']
            if 'GSP' in topics:
                male_key_gsp += topics['GSP']
            if 'FACILITY' in topics:
                male_key_facility += topics['FACILITY']
            if 'ORGANIZATION' in topics:
                male_key_organization += topics['ORGANIZATION']
        # Female Counter
        if currentBlogger['GENDER'] == 'FEMALE':
            if 'PERSON' in topics:
                female_key_person += topics['PERSON']
            if 'GPE' in topics:
                female_key_gpe += topics['GPE']
            if 'GSP' in topics:
                female_key_gsp += topics['GSP']
            if 'FACILITY' in topics:
                female_key_facility += topics['FACILITY']
            if 'ORGANIZATION' in topics:
                female_key_organization += topics['ORGANIZATION']
        # Less Than 20 Counter
        if currentBlogger['AGE'] <= 20:
            if 'PERSON' in topics:
                below20_key_person += topics['PERSON']
            if 'GPE' in topics:
                below20_key_gpe += topics['GPE']
            if 'GSP' in topics:
                below20_key_gsp += topics['GSP']
            if 'FACILITY' in topics:
                below20_key_facility += topics['FACILITY']
            if 'ORGANIZATION' in topics:
                below20_key_organization += topics['ORGANIZATION']
        # More Than 20 Counter
        if currentBlogger['AGE'] > 20:
            if 'PERSON' in topics:
                above20_key_person += topics['PERSON']
            if 'GPE' in topics:
                above20_key_gpe += topics['GPE']
            if 'GSP' in topics:
                above20_key_gsp += topics['GSP']
            if 'FACILITY' in topics:
                above20_key_facility += topics['FACILITY']
            if 'ORGANIZATION' in topics:
                above20_key_organization += topics['ORGANIZATION']


        # Everyone Counter
        if 'PERSON' in topics:
            key_person += topics['PERSON']
        if 'GPE' in topics:
            key_gpe += topics['GPE']
        if 'GSP' in topics:
            key_gsp += topics['GSP']
        if 'FACILITY' in topics:
            key_facility += topics['FACILITY']
        if 'ORGANIZATION' in topics:
            key_organization += topics['ORGANIZATION']

    except Exception as e:
        #print("Unexpected error on " + fullname + ":", e)
        pass

print('Most males are talking about')
if male_key_person:
    print('People ' + str(FreqDist(male_key_person).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(male_key_person).most_common(1).pop(0)[1]) + ' mention')
if male_key_gsp:
    print('Location ' + str(FreqDist(male_key_gsp).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(male_key_gsp).most_common(1).pop(0)[1]) + ' mention')
if male_key_facility:
    print('Facility ' + str(FreqDist(male_key_facility).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(male_key_facility).most_common(1).pop(0)[1]) + ' mention')
if male_key_organization:
    print('Unknown 1 ' + str(FreqDist(male_key_organization).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(male_key_organization).most_common(1).pop(0)[1]) + ' mention')
if male_key_gpe:
    print('Unknown 2 ' + str(FreqDist(male_key_gpe).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(male_key_gpe).most_common(1).pop(0)[1]) + ' mention')

print()
print('Most females are talking about')

if female_key_person:
    print('People ' + str(FreqDist(female_key_person).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(female_key_person).most_common(1).pop(0)[1]) + ' mention')

if female_key_gsp:
    print('Location ' + str(FreqDist(female_key_gsp).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(female_key_gsp).most_common(1).pop(0)[1]) + ' mention')

if female_key_facility:
    print('Facility ' + str(FreqDist(female_key_facility).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(female_key_facility).most_common(1).pop(0)[1]) + ' mention')

if female_key_organization:
    print('Unknown 1 ' + str(FreqDist(female_key_organization).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(female_key_organization).most_common(1).pop(0)[1]) + ' mention')

if female_key_gpe:
    print('Unknown 2 ' + str(FreqDist(female_key_gpe).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(female_key_gpe).most_common(1).pop(0)[1]) + ' mention')

print()
print('Most Below 20 are talking about')

if below20_key_person:
    print('People ' + str(FreqDist(below20_key_person).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(below20_key_person).most_common(1).pop(0)[1]) + ' mention')

if below20_key_gsp:
    print('Location ' + str(FreqDist(below20_key_gsp).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(below20_key_gsp).most_common(1).pop(0)[1]) + ' mention')

if below20_key_facility:
    print('Facility ' + str(FreqDist(below20_key_facility).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(below20_key_facility).most_common(1).pop(0)[1]) + ' mention')

if below20_key_organization:
    print('Unknown 1 ' + str(FreqDist(below20_key_organization).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(below20_key_organization).most_common(1).pop(0)[1]) + ' mention')

if below20_key_gpe:
    print('Unknown 2 ' + str(FreqDist(below20_key_gpe).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(below20_key_gpe).most_common(1).pop(0)[1]) + ' mention')

print()
print('Most Above 20 are talking about')

if above20_key_person:
    print('People ' + str(FreqDist(above20_key_person).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(above20_key_person).most_common(1).pop(0)[1]) + ' mention')

if above20_key_gsp:
    print('Location ' + str(FreqDist(above20_key_gsp).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(above20_key_gsp).most_common(1).pop(0)[1]) + ' mention')

if above20_key_facility:
    print('Facility ' + str(FreqDist(above20_key_facility).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(above20_key_facility).most_common(1).pop(0)[1]) + ' mention')

if above20_key_organization:
    print('Unknown 1 ' + str(FreqDist(above20_key_organization).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(above20_key_organization).most_common(1).pop(0)[1]) + ' mention')

if above20_key_gpe:
    print('Unknown 2 ' + str(FreqDist(above20_key_gpe).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(above20_key_gpe).most_common(1).pop(0)[1]) + ' mention')

print()
print('People are talking about')

if key_person:
    print('People ' + str(FreqDist(key_person).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(key_person).most_common(1).pop(0)[1]) + ' mention')

if key_gsp:
    print('Location ' + str(FreqDist(key_gsp).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(key_gsp).most_common(1).pop(0)[1]) + ' mention')

if key_facility:
    print('Facility ' + str(FreqDist(key_facility).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(key_facility).most_common(1).pop(0)[1]) + ' mention')

if key_organization:
    print('Unknown 1 ' + str(FreqDist(key_organization).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(key_organization).most_common(1).pop(0)[1]) + ' mention')

if key_gpe:
    print('Unknown 2 ' + str(FreqDist(key_gpe).most_common(1).pop(0)[0]) + ' with '
          + str(FreqDist(key_gpe).most_common(1).pop(0)[1]) + ' mention')
