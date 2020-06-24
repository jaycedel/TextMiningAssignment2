#https://stackoverflow.com/questions/34232190/scikit-learn-tfidfvectorizer-how-to-get-top-n-terms-with-highest-tf-idf-score

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')

t = """Two Travellers, walking in the noonday sun, sought the shade of a widespreading tree to rest. As they lay looking up among the pleasant leaves, they saw that it was a Plane Tree.

"How useless is the Plane!" said one of them. "It bears no fruit whatever, and only serves to litter the ground with leaves."

"Ungrateful creatures!" said a voice from the Plane Tree. "You lie here in my cooling shade, and yet you say I am useless! Thus ungratefully, O Jupiter, do men receive their blessings!"

Our best blessings are often the least appreciated."""

tfs = tfidf.fit_transform(t.split(" "))
str = 'tree cat travellers fruit jupiter'
response = tfidf.transform([str])
feature_names = tfidf.get_feature_names()

for col in response.nonzero()[1]:
    print(feature_names[col], ' - ', response[0, col])