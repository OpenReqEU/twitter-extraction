# Ziel: wie populaer ist das Requirement
#       Popularitaet: Anzahl der Google Suchergebnisse fuer Hashtag
#       Popularitaet: #g * 0.2 + (#l) * 0.6
# #g = Anzahl der Google Suchergebnisse fuer Hashtag
# R1 -> 50 Posts

from TwitterAPI import TwitterAPI


def fetch_tweets(hash_tags=[]):
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_secret)

    return api.request('search/tweets', {'q': ','.join(hash_tags), 'include_entities': False, 'count': 100})


# import tweepy
# from tweepy import OAuthHandler
#
# # api = twitter.Api(
# #     consumer_key='',
# #     consumer_secret='',
# #     access_token_key='',
# #     access_token_secret=''
# # )
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)
#
# api = tweepy.API(auth)
#
# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     print(status.text)
