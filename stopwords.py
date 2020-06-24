import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

text = ".The quick brown fox jumps over the lazy dog"

for sw in stop_words:
    print(sw)
    text = text.upper().replace(' ' + sw.upper() + ' ', " ")
    text = text.replace('.' + sw.upper() + ' ', " ")

print(text)
