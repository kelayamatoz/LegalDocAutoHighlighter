'''
This script prepares vocabulary model of gensim using word2vec.
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
    return ' '.join(stoppedTokens)


def generateVocabulary(fname):
    f = open(fname, 'w+')
    f.write(' ')
    corporaFiles = os.listdir('./corpora')
    for filename in corporaFiles:
        with open('./corpora/'+filename, 'rb') as infile:
            infileContent = infile.read()
            f.write(cleanupDoc(infileContent))
            # clean and tokenize document string
    f.close()


def initVocabModel():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corporaFiles = os.listdir('./corpora')
    # hacky way of reformating the vocabulary to plain text...

    # f = open('./corpora/vocabulary.txt', 'w+')
    # f.write(' ')
    # for filename in corporaFiles:
    #     with open('./corpora/'+filename, 'rb') as infile:
    #         for line in infile.read():
    #             f.write(line)
    # f.close()
    generateVocabulary('./corpora/vocabulary.txt')

    # gensim seems missing words... here is a possible fix by removing all the empty lines for training
    # with open('./corpora/vocabulary.txt', 'r+') as fname:
    #     for line in fname:
    #         if line.strip():
    #             fname.write(line)

    model = gensim.models.Word2Vec()
    trainSentences = gensim.models.word2vec.LineSentence('./corpora/vocabulary.txt')
    model.build_vocab(trainSentences)
    model.train(trainSentences)
    # updateModel(model, updateModelFile)
    model.save('word2vecModel')

r = re.compile('[A-Za-z]+')
deleteSet = set(['a', 'an', 'and', 'or', 'the'])


def tokenize(ct):
    # modify this function for different strategies of tokenizing
    # remove greek numbers, preps,
    # all words should be small case.
    resultSentences = list()
    sentences = tokenizer_old.tokenize(ct)
    for sentence in sentences:
        tokens = r.findall(sentence.lower())
        resultSentences.append(" ".join([token for token in tokens if token not in deleteSet]))

    return resultSentences


def file2CorpusTxt(txtPrefix):
    fileDirs = [t for t in os.listdir('.') if txtPrefix in t and 'Parsed' not in t]
    for fileDir in fileDirs:
        # these sub dir should contain only html files
        if 'atlassian' in fileDir or 'github' in fileDir :
            for fname in os.listdir('./'+fileDir):
                print fname
                if 'html' not in fname:
                    continue
                # if 'privacy'  in fname: continue
                textList = htmlParser.extractTextInfo(fileDir, './'+fileDir+'/'+fname)[3]
                print ">>>> translated file name = ", './corpora/vocab-'+txtPrefix+"-"+fname[:-5] + '.txt'
                with open('./corpora/vocab-'+txtPrefix+"-"+fname[:-5] + '.txt', 'w+') as fVocab:
                    for div in textList:
                        for content in div:
                            sentences = tokenize(content)
                            for sentence in sentences:
                                fVocab.write(sentence + '\n')
        elif 'apple' in fileDir:
            # apple legal docs are stored in txt format (copy-pasted from pdf)
            for fname in os.listdir('./'+fileDir):

                with open('./'+fileDir+'/'+fname) as f:
                    with open('./corpora/vocab-'+txtPrefix+'-'+fname[:-4], 'w+') as fVocab:
                        # resultSentences = tokenize(f.read())
                        # for sentence in resultSentences:
                        #     fVocab.write(sentence + '\n')
                        fVocab.write(f.read())


def loadModel():
    return gensim.models.Word2Vec.load('word2vecModel')

if __name__ == '__main__':
    # file2CorpusTxt('atlassian')
    # file2CorpusTxt('github')
    file2CorpusTxt('apple')
    initVocabModel()
