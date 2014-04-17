import sys
def jaccard_similarity(doc1, doc2):
	a=set(doc1.split());
	b=set(doc2.split());
	similarity=float(len(a.intersection(b))*1.0/len(a.union(b)))
	return similarity
influencers = ['813286','14224719','15131310','31567254','16409683']#,'14075928','7040932','12687952,'5380672,'26784273']
score = {}
content_file = open(sys.argv[1]+"_tweets", 'r')
a=content_file.read()
print "Considering Top-5 Influencers for UserSimilarity"
for influencerId in influencers:
	content_file2=open(influencerId+"_tweets", 'r')
	b=content_file2.read()
	score[influencerId]=jaccard_similarity(a,b)
	content_file2.close()

#print score
print "maximum jaccard index is for :"
print max(score, key=score.get)
