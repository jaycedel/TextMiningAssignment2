import os
import xml.etree.ElementTree as ET

from cleaner import clean_post
from xml_tags_cleaner import clean_xml_tags
from lda_topic_modelling import lda_parse_post
from lda_gensim_topic_modelling import lda_gensim_parse_post
from parse_file_name import parse_filename


# START OF MAIN PROGRAM

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
                cleanPost = str(clean_post(elem.text))
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
        print("Unexpected error on " + fullname + ":", e)
        # pass

# lda_parse_post(blogs)

#USING TF-IDF AND GENSIM TOPIC MODELING
lda_gensim_parse_post("male", blog_male_list)
lda_gensim_parse_post("female", blog_female_list)
lda_gensim_parse_post("Below 21", blog_below21_list)
lda_gensim_parse_post("Above 20", blog_above20_list)
lda_gensim_parse_post("ALL ", blogs)