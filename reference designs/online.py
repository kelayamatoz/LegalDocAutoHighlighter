import logging
import re
import os.path
import sys
import multiprocessing
import gensim
import nltk

reload(sys)
sys.setdefaultencoding('utf8')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("sampleEULA.txt")
data = fp.read()
sentences = tokenizer.tokenize(data)
tokenList = list()

for sentence in sentences:
    tokenList.append(re.compile('\w+').findall(sentence))

vocabTxt = open('vocabulary', 'a')
for sen in tokenList:
    for token in sen:
        vocabTxt.write(token + " ")
vocabTxt.close()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = gensim.models.Word2Vec()
trainSentences = gensim.models.word2vec.LineSentence("vocabulary")
model.build_vocab(trainSentences)
model.train(sentences)

model.save('EULAmodel')
