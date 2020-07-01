from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
print(stop_words)

filtered_sent=[]
for w in tokenized_sent:
    if w not in stop_words:
        filtered_sent.append(w)
print("Tokenized Sentence:",tokenized_sent)
print("Filterd Sentence:",filtered_sent)