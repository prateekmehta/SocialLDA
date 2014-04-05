__author__ = 'prateek'

import sys
import json
import nltk
import numpy
import urllib2
import re
from goose import Goose
from nltk.corpus import stopwords
from BeautifulSoup import BeautifulStoneSoup

Tr = open("obama-url-summary.txt",'a')

#==============#
stop = stopwords.words('english')

#URL = sys.argv[1]
# Some parameters you can use to tune the core algorithm.
N = 1000 # Number of words to consider
CLUSTER_THRESHOLD = 5 # Distance between words to consider
TOP_SENTENCES = 10# Number of sentences to return for a "top n" summary
# Approach taken from "The Automatic Creation of Literature Abstracts" by H.P. Luhn.

def _score_sentences(sentences, important_words):
    scores = []
    sentence_idx = -1
    for s in [nltk.tokenize.word_tokenize(s) for s in sentences]:
        sentence_idx += 1
        word_idx = []
        # For each word in the word list...
        for w in important_words:
            try:
            # Compute an index for where any important words occur in the sentence.
                word_idx.append(s.index(w))
            except ValueError: # w not in this particular sentence
                pass
        word_idx.sort()
        # It is possible that some sentences may not contain any important words at all.
        if len(word_idx)== 0: continue
        # Using the word index, compute clusters by using a max distance threshold
        # for any two consecutive words.
        clusters = []
        cluster = [word_idx[0]]
        i = 1
        while i < len(word_idx):
            if word_idx[i] - word_idx[i - 1] < CLUSTER_THRESHOLD:
                cluster.append(word_idx[i])

            else:
                clusters.append(cluster[:])
                cluster = [word_idx[i]]
            i += 1

        clusters.append(cluster)
        # Score each cluster. The max score for any given cluster is the score
        # for the sentence.
        max_cluster_score = 0
        for c in clusters:
            significant_words_in_cluster = len(c)
            total_words_in_cluster = c[-1] - c[0] + 1
            score = 1.0 * significant_words_in_cluster \
                * significant_words_in_cluster / total_words_in_cluster
            if score > max_cluster_score:
                max_cluster_score = score
        scores.append((sentence_idx, score))
    return scores

#========================================================================================#
def summarize(txt):
    sentences = [s for s in nltk.tokenize.sent_tokenize(txt)]
    normalized_sentences = [s.lower() for s in sentences]
    words = [w.lower() for sentence in normalized_sentences for w in
            nltk.tokenize.word_tokenize(sentence)]

    fdist = nltk.FreqDist(words)

    top_n_words = [w[0] for w in fdist.items()
        if w[0] not in nltk.corpus.stopwords.words('english')][:N]

    scored_sentences = _score_sentences(normalized_sentences, top_n_words)

    # Summarization Approach 1:
    # Filter out non-significant sentences by using the average score plus a
    # fraction of the std dev as a filter.

    avg = numpy.mean([s[1] for s in scored_sentences])
    std = numpy.std([s[1] for s in scored_sentences])
    mean_scored = [(sent_idx, score) for (sent_idx, score) in scored_sentences
                    if score > avg + 0.5 * std]

    # Summarization Approach 2:
    # Another approach would be to return only the top N ranked sentences.
    top_n_scored = sorted(scored_sentences, key=lambda s: s[1])[-TOP_SENTENCES:]
    top_n_scored = sorted(top_n_scored, key=lambda s: s[0])

    # Decorate the post object with summaries


    return dict(top_n_summary=[sentences[idx] for (idx, score) in top_n_scored],
                mean_scored_summary=[sentences[idx] for (idx, score) in mean_scored])

# A minimalist approach or scraping the text out of a web page. Lots of time could
# be spent here trying to extract the core content, detecting headers, footers, margins,
# navigation, etc.

def clean_html(html):
    return BeautifulStoneSoup(nltk.clean_html(html),
                             convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]



#=============UNICODE WRITE===========================================#

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

def writeToFile(outputFile, unicode_text):
    """
    Write unicode_text to filename in UTF-8 encoding.
    Parameter is expected to be unicode. But it will also tolerate byte string.
    """
    fp = outputFile
    # workaround problem if caller gives byte string instead
    unicode_text = safe_unicode(unicode_text)
    utf8_text = unicode_text.encode('utf-8')
    fp.write(utf8_text)
    #fp.close()
#-------------UNICODE WRITE FINISH-----------------------------------#

def __unicode__(self):
   return unicode(self.some_field) or u''

def finalsum(a,m,t,url):
    try:
        a= " " + str(m).strip() + " "+ a
    except:
        print("no meta")
    try:
        a = " " + str(t).strip() +  a
    except:
        print("no tittle")
    try:
        a =  "\t" + str(url).strip() +  a

    except:
        print("url")
    return a + "\n"

inputFileName = "obama-url"

if __name__ == '__main__':
    g = Goose() #article extractor
    ctr = 0
    #print inputFileBase + part
    inputFile = open(inputFileName,'r')
    lines = inputFile.readlines()
    #print lines
    for line in lines:
        #print "hi"
        print(line)
        url = line
        #print url
        try:
            #page = urllib2.urlopen(url).read().decode("utf-8").replace("\n","")
            article =   g.extract(url=url)
            #print type(page)
            # It's entirely possible that this "clean page" will be a big mess. YMMV.
            # The good news is that summarize algorithm inherently accounts for handling
            # a lot of this noise.
        except:
            print("skipped :" , url)

        #clean_page = clean_html(page)
        summary = summarize(article.cleaned_text)
        #article.meta_description + "-><-" + article.title + "-><-" + summary
        sumout = ""
        for item in summary['top_n_summary']:
            item = item.replace("\r\n\t","|")
            item = ' '.join(item.split())
            #print item
            #item = re.sub(r'[\r\n\t]', " ", item.replace(' |', ';'))
            sumout = sumout+item
        #print type(article.meta_description)
        sumout = finalsum(sumout,article.title, article.meta_description,url)
        finalDoc = [i for i in sumout.split() if i not in stop]
        sumout = str(ctr) + "\t"  + " ".join(finalDoc) + "\n"
        ctr = ctr+1
        writeToFile(Tr,sumout)
        #print label+"\t"+str(counter)+"\t"+sumout.encode('utf8')
        #print re.sub(r'\s+', ' ', summary['top_n_summary'][i].replace(' |', ';'))
        #print summary['top_n_summary']
        #f.write(label + "\t" + url+"\n")


