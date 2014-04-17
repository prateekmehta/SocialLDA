from twython import Twython, TwythonError
from collections import defaultdict
from pprint import pprint
import sys

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
#-------------Write Finished-------------#


APP_KEY =#addyourAPPKEY 
APP_SECRET =#addyoutappsecret 


ACCESS_TOKEN = #addyours



twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
inputid =  sys.argv[1]
f = open(inputid+"_tweets",'a')
f1 = open(inputid+"_urls",'a')
tweets = []
urls_d = defaultdict(int)
user_timeline = twitter.get_user_timeline(user_id = inputid,count=3200)



print(len(user_timeline))
for tweet in user_timeline:
    # Add whatever you want from the tweet, here we just add the text
    #print(tweet)
    #print("next Batch")
    #--cleansing tweets--
    item = tweet['text']
    item = item.replace("\r\n\t","|")
    item = ' '.join(item.split())
    tweet_line = tweet['id_str'] + "\t" + item + "\n" 
    tweets.append(tweet_line)
    print tweet_line
    for url in tweet['entities']['urls']:
        #print(1)
        #print(url)
        '''for i in url:
            urls_d[i["expanded_url"]] += 1'''
        #print(url["expanded_url"])
        urls_d[url["expanded_url"]] += 1

    #urls.append(tweet.entities)

# Count could be less than 200, see:
# https://dev.twitter.com/discussions/7513
print(len(tweets))
count = 0
for item in tweets:
    #count+=1
    #line = str(count) + "\t" + item + "\n"
    writeToFile(f,item)
    #f.write(count)
    #f.write(line)

for items in urls_d:
    #print(items)
    f1.writelines("%s\n" %items)



f.close()
f1.close()
