import nltk
######################Simple Tagging###############################################################################################
# text = nltk.word_tokenize("The city of Auckland is in New Zeland which is in the Pacific")
# print(nltk.pos_tag(text))
#
# # Many words can function in different roles, such as run,live and talk.
# text = nltk.word_tokenize("The talk was boring")
# print(nltk.pos_tag(text))
#
# text = nltk.word_tokenize("You should talk more in class")
# print(nltk.pos_tag(text))

# ####################################Misc operations on tagging##############################################################

# Representing tagged tokens
# tagged_token = nltk.tag.str2tuple('fly/NN')
# tagged_token
# ('fly', 'NN')
# print(tagged_token[0])
# print(tagged_token[1])
#
# #Reading tagged corpora
# print(nltk.corpus.nps_chat.tagged_words())
# print(nltk.corpus.conll2000.tagged_words())
# print(nltk.corpus.treebank.tagged_words())
#
# #Taggged corpora for several ther languages are also available
# print(nltk.corpus.sinica_treebank.tagged_words())
# print(nltk.corpus.indian.tagged_words())
# print(nltk.corpus.mac_morpho.tagged_words())
# print(nltk.corpus.conll2002.tagged_words())
# print(nltk.corpus.cess_cat.tagged_words())

# ##########################################################################################################################f

# from nltk.corpus import brown
# brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
# tag_fd = nltk.FreqDist(tag for (word, tag) in brown_news_tagged)
# print(tag_fd.most_common())
# tag_fd.plot(cumulative=False)

# #################################Exploring corpora#########################################################################################f
# Lets see what parts of speech frequently occur before a noun
from nltk.corpus import brown
brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
word_tag_pairs = nltk.bigrams(brown_news_tagged)
noun_preceders = [a[1] for (a, b) in word_tag_pairs if b[1] == 'NOUN']
print(noun_preceders)
print("\n",noun_preceders.__sizeof__())
fdist = nltk.FreqDist(noun_preceders)
print([tag for (tag, _) in fdist.most_common()])

# #####################################Exploreing corpora#####################################################################################
#
# #Explore the corpora
# #Lets see which word most often follows the word "often". Verb is the highest and nouns never even appear.
# from nltk.corpus import brown
# brown_learned_text = brown.words(categories='learned')
# print(sorted(set(b for (a, b) in nltk.bigrams(brown_learned_text) if a == 'often')))
# #Probably better to see the POS that follows the word "often"
# brown_lrnd_tagged = brown.tagged_words(categories='learned', tagset='universal')
# tags = [b[1] for (a, b) in nltk.bigrams(brown_lrnd_tagged) if a[0] == 'often']
# fd = nltk.FreqDist(tags)
# fd.tabulate()

# ################################Exploring Corpora##########################################################################################
# #Look at trigram contexts, lets explore verb TO verb in a big corpus.
# from nltk.corpus import brown
# def process(sentence):
#     for (w1,t1), (w2,t2), (w3,t3) in nltk.trigrams(sentence):
#         if (t1.startswith('V') and t2 == 'TO' and t3.startswith('V')):
#             print(w1, w2, w3)
#
# for tagged_sent in brown.tagged_sents():
#     process(tagged_sent)

# ##########################################################################################################################
#
# #Lets look at words that are hardest to tag, ie, they are most ambiguous.
# from nltk.corpus import brown
# brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
# data = nltk.ConditionalFreqDist((word.lower(), tag) for (word, tag) in brown_news_tagged)
#
# for word in sorted(data.conditions()):
#      if len(data[word]) > 2:
#         tags = [tag for (tag, _) in data[word].most_common()]
#         print(word, ' '.join(tags))
#
# ############################################Useful data structures in python##############################################################################

# # Indexed lists versus dictionaries
# # Indexed list - is a lookup table with index numbers and and an entry which is a string. Eg. a document is represented as a list
# #Dictionary - is again a table but this time the lookup is done using a string and you get back a value which can be a number or another string. Eg. a frequency dist. table.
#
# #Eg of a dictionary
# pos = {}
# pos['ideas'] = 'N'
# pos['sleep'] = 'V'
# pos['furiously'] = 'ADV'
# print(pos)
# print('ideas')
# print("\nUseful calls to konw for dictionary iterations")
# print(list(pos))
# print(sorted(pos))
# for word in sorted(pos):
#     print(word + ":" + pos[word])
#
# print(list(pos.keys()))
# print(list(pos.values()))
# print(list(pos.items()))
# for key, val in sorted(pos.items()):
#     print(key + ":", val)

# ##########################################################################################################################
# # Lets use some datasets from NLTK
# from collections import defaultdict
#
# counts = defaultdict(int)
# from nltk.corpus import brown
#
# for (word, tag) in brown.tagged_words(categories='news', tagset='universal'):
#     counts[tag] += 1
# print(counts['NOUN'])
# print(sorted(counts))
# from operator import itemgetter
#
# print(sorted(counts.items(), key=itemgetter(1), reverse=True))

# ##########################################################################################################################
#
#A handy trick to extract an element from a tuple
# from nltk.corpus import brown
# tags = [tag for (word, tag) in brown.tagged_words(categories='news')]
# print(tags)
#
# ##########################################################################################################################
# ##Lets use some POS taggers and see how they perform.
# ##Regualar expression tagger
#
# from nltk.corpus import brown
# brown_tagged_sents = brown.tagged_sents(categories='news')
# brown_sents = brown.sents(categories='news')
# patterns = [
#      (r'.*ing$', 'VBG'),               # gerunds
#      (r'.*ed$', 'VBD'),                # simple past
#      (r'.*es$', 'VBZ'),                # 3rd singular present
#      (r'.*ould$', 'MD'),               # modals
#      (r'.*\'s$', 'NN$'),               # possessive nouns
#      (r'.*s$', 'NNS'),                 # plural nouns
#      (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
#      (r'.*', 'NN')                     # nouns (default)
#  ]
# regexp_tagger = nltk.RegexpTagger(patterns)
# print(regexp_tagger.tag(brown_sents[3]))
# print("Accuracy: ",  regexp_tagger.evaluate((brown_tagged_sents)))

# ##########################################################################################################################
# #Unigram tagging - assigns the tag that is most frequently used with a given token in the training data.
# from nltk.corpus import brown
# brown_tagged_sents = brown.tagged_sents(categories='news')
# brown_sents = brown.sents(categories='news')
# unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
# print(unigram_tagger.tag(brown_sents[2007]))

# # ##########################################################################################################################
#Separating the training and the test data
import nltk
from nltk.corpus import brown
brown_tagged_sents = brown.tagged_sents(categories='news')
size = int(len(brown_tagged_sents) * 0.9)
print(size)
train_sents = brown_tagged_sents[:size]
test_sents = brown_tagged_sents[size:]
unigram_tagger = nltk.UnigramTagger(train_sents)
print(unigram_tagger.evaluate(test_sents))
#
# #Storing a trained model, retrieving it and using it.
#
# #Store it.
# from pickle import dump
# output = open('ugTagger.pkl', 'wb')
# dump(unigram_tagger, output, -1)
# output.close()
#
# #Retrieve it from a file
# from pickle import load
# input = open('ugTagger.pkl', 'rb')
# tagger = load(input)
# input.close()
# #Use it.
# text = "The board's action shows what free enterprise is up against in our complex maze of regulatory laws ."
# tokens = text.split()
# print(tagger.tag(tokens))
##########################################################################################################################
# #Using confusion matrix for evaluation.
# from nltk.metrics import *
# ref    = 'DET NN VB DET JJ NN NN IN DET NN'.split()
# tagged = 'DET VB VB DET NN NN NN IN DET NN'.split()
# cm = ConfusionMatrix(ref, tagged)
# print(cm)
# print("Precision: ",precision(set(ref),set(tagged)))
# print("Recall: ",recall(set(ref),set(tagged)))
# print("F measure: ",f_measure(set(ref),set(tagged)))
# print("Accuracy: ",accuracy(ref,tagged))
#
# #another way, library, whats the difference?
# from sklearn import metrics
# print(metrics.classification_report(ref, tagged))
#


##########################################################################################################################

# #Distance metrices
# from nltk.metrics import *
# s1 = "John went to town on a bike"
# s2 = "Peter went to town in a bus"
# print("Edit Distnance same string: ",edit_distance(s1,s1))
# print("Edit Distnance: ",edit_distance(s1,s2))
# print("Binary Distnance: ",binary_distance(set(s1),set(s2)))
# print("Jaccard Distnance: ",jaccard_distance(set(s1),set(s2)))
# print("Masi Distnance: ",masi_distance(set(s1),set(s2)))
##########################################################################################################################
