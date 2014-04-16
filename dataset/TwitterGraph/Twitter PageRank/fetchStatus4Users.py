# -*- coding: utf-8 -*-

import sys
import tweepy
from tweepy import Cursor

# Query terms

'''u_id = sys.argv[1:]
f = open(u_id[0],'a')'''

#Q = ["news","breaking news","News","Breaking News","BREAKING NEWS","Politics","POLITICS","BreakingNews","NEWS","WORLD","BUSINESS","TECHNOLOGY","ENTERTAINMENT","SPORTS","SCIENCE","HEALTH","Enetertainment","Sports","Science","Health"]

# Get these values from your application settings.

#addyourownkeys
CONSUMER_KEY = 
CONSUMER_SECRET =
# Get these values from the "My Access Token" link located in the
# margin of your application details, or perform the full OAuth
# dance.
ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET = 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

print api.me().name

for status in Cursor(api.user_timeline).items():
    # process status here
    f.write(status)
    print(status)

