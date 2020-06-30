# https://ourcodingclub.github.io/tutorials/topic-modelling-python/

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# the vectorizer object will be used to transform text to vector form
vectorizer = CountVectorizer(max_df=0.9, min_df=25, token_pattern='\w+|\$[\d\.]+|\S+')


# apply transformation
def lda_parse_post(posts):

    tf = vectorizer.fit_transform(posts).toarray()

    # tf_feature_names tells us what word each column in the matric represents
    tf_feature_names = vectorizer.get_feature_names()

    number_of_topics = 10

    model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)

    model.fit(tf)
    no_top_words = 10

    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict["Topic %d words" % (topic_idx)] = ['{}'.format(tf_feature_names[i])
                                                      for i in topic.argsort()[:-no_top_words - 1:-1]]
        topic_dict["Topic %d weights" % (topic_idx)] = ['{:.1f}'.format(topic[i])
                                                        for i in topic.argsort()[:-no_top_words - 1:-1]]
