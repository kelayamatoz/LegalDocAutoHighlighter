'''
This script prepares vocabulary model of gensim using doc2vec.
'''

import logging
import htmlParser
# import txtParser
import os.path
import sys
import gensim
import re
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import nltk
from gensim import corpora, models
import gensim.models.doc2vec as doc2vec


reload(sys)
sys.setdefaultencoding('utf8')
tokenizer_old = nltk.data.load('tokenizers/punkt/english.pickle')
tokenizer = RegexpTokenizer(r'\w+')

def updateModel(model, fileNameList):
    # note: online version of gensim is not working stably...
    # right now if we want to update the model, we need to retrain the whole thing.
    for trainingTxt in fileNameList:
        newSentence = gensim.models.word2vec.LineSentence(trainingTxt)
        model.build_vocab(newSentence, update=True)
        model.train(newSentence)


# This function cleans up a document to the desired format
extraStopWords = ['bitbucket', 'atlassian', 'github']

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


def cleanupDoc(fileString):
    raw = fileString.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from token
    stoppedTokens = [i for i in tokens if i not in en_stop]
    # stemmedTokens = [p_stemmer.stem(i) for i in stoppedTokens]
    return ' '.join(stoppedTokens) + '\n'


def initVocabModel():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    doc2vecCorporaFiles = os.listdir('./doc2vecCorpora')
    labeledSenList = list()
    uid = 0
    for filename in doc2vecCorporaFiles:
        print filename
        with open('./doc2vecCorpora/'+filename, 'rb') as infile:
            for l in infile:
                tokens = tokenizer.tokenize(l.lower())
                stoppedTokens = [i for i in tokens if i not in en_stop]
                sentence = doc2vec.TaggedDocument(stoppedTokens, ['SENT_%s' % uid])
                labeledSenList.append(sentence)
                uid += 1

    model = gensim.models.Doc2Vec(alpha=0.025, min_alpha=0.025)
    model.build_vocab(iter(labeledSenList))
    for epoch in range(10):
        model.train(iter(labeledSenList))
        model.alpha -= 0.002
        model.min_alpha = model.alpha

    model.save('./doc2vecModel.doc2vec')
    # generateVocabulary('./doc2vecCorpora/vocabulary.txt')
    print 'here'


if __name__ == '__main__':
    # file2CorpusTxt('atlassian')
    # file2CorpusTxt('github')
    # file2CorpusTxt('apple')
    initVocabModel()


