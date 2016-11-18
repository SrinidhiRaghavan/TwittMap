import json
from TwitterSearch import *

#Config stores various credentials
from config import TWITTER_ACCESS, TWITTER_SECRET, \
                   TWITTER_CON_SECRET, TWITTER_CON_ACCESS, \
                   AWS_ES_INDEX, AWS_ES_TYPE
from settings import gmaps
from settings import es
from utils import get_category


try:
    tso = TwitterSearchOrder()
    #By default we collect the tweets of the Sports Category. This can be modified to any other category based on the application
    tso.set_keywords(['sports'])
    tso.set_language('en')

    ts = TwitterSearch(
        consumer_key = TWITTER_CON_ACCESS,
        consumer_secret = TWITTER_CON_SECRET,
        access_token = TWITTER_ACCESS,
        access_token_secret = TWITTER_SECRET
     )

    count = 0
    
    for tweet in ts.search_tweets_iterable(tso):
        try:
            #The tweets are retrieved only if the geolocation is tagegd
            if tweet['user'].get('location') is not None:
                location = tweet['user'].get('location')
                tweet_id = str(tweet['id'])
                geocode_result = gmaps.geocode(location)
                print geocode_result
                tweet_text = tweet['text'].lower().encode('ascii', 'ignore').decode('ascii')
                raw_tweet = {
                    'user': tweet['user']['screen_name'],
                    'text': tweet_text,
                    'location': tweet['user']['location'],
                    'coordinates': geocode_result, 
                    'time': tweet['created_at'],
                    'category': get_category(tweet_text)
                }
                es.index(index=AWS_ES_INDEX, doc_type=AWS_ES_TYPE, id=tweet_id, body=raw_tweet)
        except Exception as e:
            print e
            continue

except TwitterSearchException as e:
    print(e)
