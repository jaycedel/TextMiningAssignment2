import spacy
# import displacy
from spacy import displacy
from collections import Counter

nlp = spacy.load('en_core_web_sm')
complete_text = ('Gus Proto is a Python developer currently'
                 'working for a London-based Fintech company. He is'
                 ' interested in learning Natural Language Processing.'
                 ' There is a developer conference happening on 21 July'
                 ' 2019 in London. It is titled "Applications of Natural'
                 ' Language Processing". There is a helpline number '
                 ' available at +1-1234567891. Gus is helping organize it.'
                 ' He keeps organizing local Python meetups and several'
                 ' internal talks at his workplace. Gus is also presenting'
                 ' a talk. The talk will introduce the reader about "Use'
                 ' cases of Natural Language Processing in Fintech".'
                 ' Apart from his work, he is very passionate about music.'
                 ' Gus is learning to play the Piano. He has enrolled '
                 ' himself in the weekend batch of Great Piano Academy.'
                 ' Great Piano Academy is situated in Mayfair or the City'
                 ' of London and has world-class piano instructors.')

complete_doc = nlp(complete_text)
# Remove stop words and punctuation symbols
words = [token.text for token in complete_doc
         if not token.is_stop and not token.is_punct]
word_freq = Counter(words)
# 5 commonly occurring words with their frequencies
common_words = word_freq.most_common(5)
print('common words')
print(common_words)

# Iterate over the tokens
for token in complete_doc:
    # Print the token and its part-of-speech tag
    print(token.text, "-->", token.pos_)

displacy.serve(complete_doc, style="ent")
