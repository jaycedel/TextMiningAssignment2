import os
import sys
import xml.etree.ElementTree as ET
from htmlentitydefs import name2codepoint

maleCount = 0
femaleCount = 0

path = "/Users/junedc/Desktop/JoanSchool/blogs"

demographics = {}

gender = {}
age = {}
interest = {}
zodiac = {}



for filename in os.listdir(path):
    if not filename.endswith('.xml'):
        continue
    fullname = os.path.join(path, filename)
    try:
        parser = ET.XMLParser()
        parser.parser.UseForeignDTD(True)
        parser.entity.update((x, unichr(i)) for x, i in name2codepoint.iteritems())
        etree = ET.ElementTree()
        tree = etree.parse(fullname, parser=parser)
        #tree = ET.parse(fullname, ET.XMLParser(encoding='utf-8'))
    except Exception as e:
        print(e)
        print "Unexpected error on " + fullname + ":", sys.exc_info()[0]
        #raise
        #pass

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

print(gender)
print(age)
print(interest)
print(zodiac)