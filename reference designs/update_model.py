
import logging
import re
import os
import sys
import multiprocessing
import gensim
import nltk

reload(sys)
sys.setdefaultencoding('utf8')
model = gensim.models.Word2Vec.load('EULAmodel')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
for f in os.listdir(os.getcwd()+"/new_training_texts"):
    fp = open(os.getcwd()+"/new_training_texts/"+f)
    data = fp.read()
    sentences = tokenizer.tokenize(data)
    tokenList = list()

    for sentence in sentences:
        tokenList.append(re.compile('[A-Za-z]+').findall(sentence))

    vocabTxt = open('vocabulary'+'_'+f, 'a')
    for sen in tokenList:
        for token in sen:
            vocabTxt.write(token + " ")

    vocabTxt.close()

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    trainSentences = gensim.models.word2vec.LineSentence("vocabulary")
    model.build_vocab(trainSentences)
    model.train(sentences)

model.save('EULAmodel')
