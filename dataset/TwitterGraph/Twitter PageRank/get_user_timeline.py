from twython import Twython, TwythonError

APP_KEY = "Ll0HHLMotb4zxsXEahZbWw"
APP_SECRET = "mObYZaX05NN6WvWxSMMpWAjVZDcO9o80QG62N4QHL0"

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)

print 1

ACCESS_TOKEN = twitter.obtain_access_token()

print ACCESS_TOKEN

#ACCESS_TOKEN_SECRET = "v8saE2br55dtSY2IwSKLnhl8DmwlFb44M9lcng3kQl4"

# Requires Authentication as of Twitter API v1.1
#twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

try:
    user_timeline = twitter.get_user_timeline(screen_name='ryanmcgrath')
except TwythonError as e:
    print e

#print user_timeline
