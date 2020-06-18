import os
import sys
import xml.etree.ElementTree as ET
import html.parser

maleCount = 0
femaleCount = 0

path = "../blogs"
demographics = {}
gender = {}
age = {}
interest = {}
zodiac = {}

for filename in os.listdir(path):
    if not filename.endswith('.xml'):
        continue

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

    # GET THE FULLNAME
    fullname = os.path.join(path, filename)
    print(fullname)

    # GET CONTENT OF THE XML FILE
    # https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in/42340744

    try:
        with open(fullname, encoding="utf8", errors='ignore') as f:
            text = f.read()

        decodedContent = html.unescape(text)
        decodedContent = decodedContent.replace(" & ", " and ")
        decodedContent = decodedContent.replace("&", "")
        decodedContent = decodedContent.replace("<>", " ")
        decodedContent = decodedContent.replace("&lt;", " ")
        decodedContent = decodedContent.replace("&gt;", " ")
        tree = ET.fromstring(decodedContent)
        # for elem in tree.iter():
        #     if elem.tag == 'post':
        #         print(elem.text)

    except Exception as e:
            print("Unexpected error on " + fullname + ":", e)
    #         raise
            pass

print(gender)
print(age)
print(interest)
print(zodiac)
