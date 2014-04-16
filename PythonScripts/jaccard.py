def jaccard_similarity(doc1, doc2):
	a=set(doc1.split());
	b=set(doc2.split());
	similarity=float(len(a.intersection(b))*1.0/len(a.union(b)))
	return similarity
with open('1.txt', 'r') as content_file:
	a=content_file.read()
with open('1.txt', 'r') as content_file2:
	b=content_file2.read()
print jaccard_similarity(a,b);
