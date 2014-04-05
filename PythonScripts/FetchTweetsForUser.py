from twython import Twython, TwythonError
from collections import defaultdict
from pprint import pprint

APP_KEY = "Ll0HHLMotb4zxsXEahZbWw"
APP_SECRET = "mObYZaX05NN6WvWxSMMpWAjVZDcO9o80QG62N4QHL0"


ACCESS_TOKEN = "AAAAAAAAAAAAAAAAAAAAAIJJTgAAAAAAXzwcZzDyC7tsE%2B2fNLPKxcjyrww%3DngL1bdArGrwqpfqdjQz2LHt7F6iLMVajjTm2zDGAaVqAL241IY"
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

f = open("Obama",'a')
f1 = open("obama-urls",'a')
tweets = []
urls_d = defaultdict(int)
user_timeline = twitter.get_user_timeline(user_id = "813286",count=3200)



print(len(user_timeline))
for tweet in user_timeline:
    # Add whatever you want from the tweet, here we just add the text
    #print(tweet)
    #print("next Batch")
    tweets.append(tweet['text'])
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
    count+=1
    #f.write(count)
    f.writelines("%d\t%s\n" %(count,item))

for items in urls_d:
    print(items)
    f1.writelines("%s\n" %items)



