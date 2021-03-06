import nltk

# library for cleaning text
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

my_stopwords = nltk.corpus.stopwords.words('english')
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem
my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'


def clean_post(post, bigrams=True):

    post = post.lower()  # lower case

    # remove unwanted words
    post = post.replace("urllink", "")
    post = post.replace("time", "")
    post = post.replace("like", "")
    post = post.replace("make", "")
    post = post.replace("would", "")

    post = re.sub('[' + my_punctuation + ']+', ' ', post)  # strip punctuation
    post = re.sub('\s+', ' ', post)  # remove double spacing
    post = re.sub('([0-9]+)', '', post)  # remove numbers

    post_token_list = [word for word in post.split(' ')
                       if word not in my_stopwords]  # remove stopwords

    post_token_list = [word_rooter(word) if '#' not in word else word
                       for word in post_token_list]  # apply word rooter

    tokenized_posts = []
    for token in post_token_list:
        if len(token) > 3:
            tokenized_posts.append(token)

    if bigrams:
        post_token_list = post_token_list + [post_token_list[i] + '_' + post_token_list[i + 1]
                                             for i in range(len(post_token_list) - 1)]
    post = ' '.join(tokenized_posts)
    return post
