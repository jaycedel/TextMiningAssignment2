import os
import xml.etree.ElementTree as ET
import html.parser
import nltk

maleCount = 0
femaleCount = 0

path = "../blogs2"  # FOLDER OF WHERE THE FILES ARE
demographics = {}
gender = {}
age = {}
interest = {}
zodiac = {}
topics = {}


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

    currentBlogger = {}
    currentBlogger['GENDER'] = splittedFilename[1]
    currentBlogger['AGE'] = splittedFilename[2]
    currentBlogger['INTEREST'] = splittedFilename[3]
    return currentBlogger


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

        decodedContent = html.unescape(text)
        decodedContent = decodedContent.replace(" & ", " and ")
        decodedContent = decodedContent.replace("&", "")
        decodedContent = decodedContent.replace("<>", " ")
        decodedContent = decodedContent.replace("&lt;", " ")
        decodedContent = decodedContent.replace("&gt;", " ")
        decodedContent = decodedContent.replace("urlLink", "")
        tree = ET.fromstring(decodedContent)

        # GET ALL POST ELEMENT TAGS
        for elem in tree.iter():
            if elem.tag == 'post':
                parseBlog(elem.text)

        # DISPLAY THE CURRENT GENDER, AGE AND INTEREST
        print(currentBlogger)

        # CHECK THE TOPIC AND SUBJECT ENTERED IN THE BLOG POST
        for keyTopic in topics:
            print(keyTopic, '->', topics[keyTopic])

    except Exception as e:
        print("Unexpected error on " + fullname + ":", e)
        pass

# print(gender)
# print(age)
# print(interest)
# print(zodiac)
