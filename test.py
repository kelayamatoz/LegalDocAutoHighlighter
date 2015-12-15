import gensim

model = gensim.models.Doc2Vec.load('./doc2vecModel.doc2vec')
testModel = gensim.models.Word2Vec.load('./word2vecModel')
print 'here'