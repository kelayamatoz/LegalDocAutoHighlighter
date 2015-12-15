import sys
from numpy import array
import LDA
import vocabBuilder
import gensim
import LOF
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

reload(sys)
sys.setdefaultencoding('utf8')

# inputSrc = './sampleTest.txt'
inputSrc = './appleLegalDocDir/apple-osx-test.txt'
minTokenNum = 4
tokenList = list()
sentenceList = list()

with open(inputSrc) as f:
    text = f.read()

# Task 0: use LDA to filter out common topics. This way the main popular topic words won't affect
# calculation of similarities.

ldaModel = LDA.loadModel()
topics, topicCoherencePair = LDA.getTopicsWithNormalizedWeight(ldaModel)

sentences = vocabBuilder.tokenize(text)
for sentence in sentences:
    tokens = list()
    tmpTokens = sentence.split()
    for token in tmpTokens:
        if token not in topics:
            tokens.append(token)

    if len(tokens) >= minTokenNum:
        tokenList.append(tokens)
        sentenceList.append(sentence)
print 'There are ', len(sentenceList), ' sentences in the input sample.'


word2vecModel = vocabBuilder.loadModel()
sentenceVecModelList = list()
for tokenSen in tokenList:
    v1 = []
    for word in tokenSen:
        if word not in word2vecModel.vocab:
            v1.append([-1.0]*100)
        else:
            v1.append(word2vecModel[word])
    # normalize v1 with mean 0.
    sentenceVecModelList.append(gensim.matutils.unitvec(array(v1).mean(axis=0)))

## Task 1: Try AgglomerativeClustering:

aggModelList = list()
silhouette_avg_list = list()
for n_cluster in range(2, 40):
    aggModel = AgglomerativeClustering(n_clusters=n_cluster, n_components=len(sentenceVecModelList), \
                                   linkage='average', affinity='cosine')
    aggModel.fit(sentenceVecModelList)
    aggModelList.append(aggModel)
    silhouette_avg = silhouette_score(array(sentenceVecModelList), aggModel.labels_)
    silhouette_avg_list.append(silhouette_avg)

print silhouette_avg_list

n_clusters = 3
# Task 1 reports that three clusters give the best division...
testAggModel = AgglomerativeClustering(n_clusters=n_clusters, n_components=len(sentenceVecModelList), \
                                   linkage='average', affinity='cosine')
testAggModel.fit(sentenceVecModelList)
labels = testAggModel.labels_.tolist()
print labels

# find labels with the farthest distances...
clusterList = [list() for _ in range(n_clusters)]
for senVecId in range(len(sentenceVecModelList)):
    clusterList[labels[senVecId]].append(senVecId)

# filter out sentences that reside in one cluster. If such a sentence is found, then this sentence is an anormaly.
clusterAnormalySentences = list()
removeInds = list()
for ptsInd in range(len(clusterList)):
    print ptsInd
    pts = clusterList[ptsInd]
    if len(pts) == 1:
        print sentences[pts[0]]
        clusterAnormalySentences.append(sentences[pts[0]])
        removeInds.append(ptsInd)
#
# for i in removeInds:
#     pts = clusterList[i]
#     clusterList.remove(pts)
#     labels.remove(i)


# use LOF on the rest of the cluster
mus = list()
for cluster in clusterList:
    # get the centroid value
    numOfPts = len(cluster)
    mu = sum([sentenceVecModelList[pt] for pt in cluster]) / numOfPts
    mus.append(mu)

lof = LOF.LOF(mus, labels, sentenceVecModelList, 6)
lofList = list()
for ptIndex in range(len(labels)):
    lofPt = lof.calcLOF(ptIndex)
    lofList.append(lofPt)
    print ptIndex, lofPt

lofIdList = list();
anormalySentences = list()
for lofId in range(len(lofList)):
    if lofList[lofId] > 1.0: # now try to find inliners
        # print sentenceList[lofId]
        lofIdList.append(lofId)
        anormalySentences.append((sentenceList[lofId], lofList[lofId], sentenceVecModelList[lofId], lofId))

anormalySentencesReversed = sorted(anormalySentences, key=lambda x: x[1], reverse=True)
for sentence in anormalySentencesReversed:
    print sentence[0], sentence[1]