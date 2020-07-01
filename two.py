# https://medium.com/@yanlinc/how-to-build-a-lda-topic-model-using-from-text-601cdcbfd3a6

import matplotlib
import numpy as np
import pandas as pd
import re, nltk, spacy, gensim

# Sklearn
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from pprint import pprint

import spacy

# nlp = spacy.load('en_core_web_sm')
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Plotting tools
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt


# %matplotlib inline

def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):  # 'NOUN', 'ADJ', 'VERB', 'ADV'
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append(" ".join(
            [token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))
    return texts_out

# Show top n keywords for each topic
def show_topics(vectorizer, lda_model, n_words=20):
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))
    return topic_keywords

def color_green(val):
    color = "green" if val > .1 else "black"
    return "color: {col}".format(col=color)

def make_bold(val):
    weight = 700 if val > .1 else 400
    return "font-weight: {weight}".format(weight=weight)

def predict_topic(text, nlp=nlp):
    global sent_to_words
    global lemmatization

def apply_predict_topic(text):
     text = [text]
     infer_topic, topic, prob_scores = predict_topic(text = text)
     return(infer_topic)

df = pd.read_csv("googleplaystore_user_reviews.csv", error_bad_lines=False)
df = df.dropna(subset=["Translated_Review"])

# Convert to list
data = df.Translated_Review.values.tolist()
# Remove Emails
data = [re.sub(r'\S*@\S*\s?', '', sent) for sent in data]
# Remove new line characters
data = [re.sub(r'\s+', ' ', sent) for sent in data]
# Remove distracting single quotes
data = [re.sub(r"\'", "", sent) for sent in data]
pprint(data[:1])

data_words = list(sent_to_words(data))
print(data_words[:1])

data_lemmatized = lemmatization(data_words, allowed_postags=["NOUN", "VERB"])  # select noun and verb

print(data_lemmatized[:2])

vectorizer = CountVectorizer(analyzer='word',
                             min_df=10,
                             # minimum reqd occurences of a word
                             stop_words='english',
                             # remove stop words
                             lowercase=True,
                             # convert all words to lowercase
                             token_pattern='[a-zA-Z0-9]{3,}',
                             # num chars > 3
                             max_features=50000,
                             # max number of uniq words
                             )
data_vectorized = vectorizer.fit_transform(data_lemmatized)

# Build LDA Model
lda_model = LatentDirichletAllocation(n_components=20,  # Number of topics
                                      max_iter=10,
                                      # Max learning iterations
                                      learning_method='online',
                                      random_state=100,
                                      # Random state
                                      batch_size=128,
                                      # n docs in each learning iter
                                      evaluate_every=-1,
                                      # compute perplexity every n iters, default: Don't
                                      n_jobs=-1,
                                      # Use all available CPUs
                                      )
lda_output = lda_model.fit_transform(data_vectorized)
print(lda_model)  # Model attributes

# LatentDirichletAllocation(batch_size=128, doc_topic_prior=None,
#                           evaluate_every=-1, learning_decay=0.7,
#                           learning_method="online", learning_offset=10.0,
#                           max_doc_update_iter=100, max_iter=10, mean_change_tol=0.001,
#                           n_components=10, n_jobs=-1, n_topics=20, perp_tol=0.1,
#                           random_state=100, topic_word_prior=None,
#                           total_samples=1000000.0, verbose=0)

# Log Likelyhood: Higher the better
print("Log Likelihood: ", lda_model.score(data_vectorized))
# Perplexity: Lower the better. Perplexity = exp(-1. * log-likelihood per word)
print("Perplexity: ", lda_model.perplexity(data_vectorized))
# See model parameters
pprint(lda_model.get_params())

# Define Search Param
search_params = {'n_components': [10, 15, 20, 25, 30], 'learning_decay': [.5, .7, .9]}
# Init the Model
lda = LatentDirichletAllocation(max_iter=5, learning_method='online', learning_offset=50., random_state=0)
# Init Grid Search Class
model = GridSearchCV(lda, param_grid=search_params)
# Do the Grid Search
model.fit(data_vectorized)
GridSearchCV(cv=None, error_score='raise',
             estimator=LatentDirichletAllocation(batch_size=128, doc_topic_prior=None,
                                                 evaluate_every=-1, learning_decay=0.7, learning_method=None,
                                                 learning_offset=10.0, max_doc_update_iter=100, max_iter=10,
                                                 mean_change_tol=0.001, n_components=10, n_jobs=1,
                                                 n_topics=None, perp_tol=0.1, random_state=None,
                                                 topic_word_prior=None, total_samples=1000000.0, verbose=0),
             fit_params=None, iid=True, n_jobs=1,
             param_grid={'n_topics': [10, 15, 20, 25, 30], 'learning_decay': [0.5, 0.7, 0.9]},
             pre_dispatch='2*n_jobs', refit=True, return_train_score='warn',
             scoring=None, verbose=0)


# Best Model
best_lda_model = model.best_estimator_
# Model Parameters
print("Best Model's Params: ", model.best_params_)
# Log Likelihood Score
print("Best Log Likelihood Score: ", model.best_score_)
# Perplexity
print("Model Perplexity: ", best_lda_model.perplexity(data_vectorized))



# Create Document — Topic Matrix
lda_output = best_lda_model.transform(data_vectorized)
# column names
topicnames = ["Topic" + str(i) for i in range(best_lda_model.n_components)]
# index names
docnames = ["Doc" + str(i) for i in range(len(data))]
# Make the pandas dataframe
df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)
# Get dominant topic for each document
dominant_topic = np.argmax(df_document_topic.values, axis=1)
df_document_topic["dominant_topic"] = dominant_topic
# Styling


# Apply Style
df_document_topics = df_document_topic.head(15).style.applymap(color_green).applymap(make_bold)


# Topic-Keyword Matrix
df_topic_keywords = pd.DataFrame(best_lda_model.components_)
# Assign Column and Index
df_topic_keywords.columns = vectorizer.get_feature_names()
df_topic_keywords.index = topicnames
# View
df_topic_keywords.head()


topic_keywords = show_topics(vectorizer=vectorizer, lda_model=best_lda_model, n_words=15)
# Topic - Keywords Dataframe
df_topic_keywords = pd.DataFrame(topic_keywords)
df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]


Topics = ["Update Version/Fix Crash Problem","Download/Internet Access","Learn and Share","Card Payment","Notification/Support",
          "Account Problem", "Device/Design/Password", "Language/Recommend/Screen Size", "Graphic/ Game Design/ Level and Coin", "Photo/Search"]
df_topic_keywords["Topics"]=Topics
