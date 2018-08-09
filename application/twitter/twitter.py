# Ziel: wie populaer ist das Requirement
#       Popularitaet: Anzahl der Google Suchergebnisse fuer Hashtag
#       Popularitaet: #g * 0.2 + (#l) * 0.6
# #g = Anzahl der Google Suchergebnisse fuer Hashtag
# R1 -> 50 Posts

from TwitterAPI import TwitterAPI


def fetch_tweets(hash_tags=[]):
    consumer_key = 'J5S0tA4qG5UK45gLOUccT4yBd'
    consumer_secret = '6qsTntxDb5oxRpGCy9hjWHKtZVzkz7V0dY2vTAr04tM4D2ddnI'
    access_token = '811159293751857224-qSPuXZ5NzYAuhBcF8fM1R4JAaLmxi83'
    access_secret = '0CW7zVieofbn6tjlpp9HVbtJ1aoi9bkibunuY5QyPaXqu'
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_secret)

    return api.request('search/tweets', {'q': ','.join(hash_tags), 'include_entities': False, 'count': 100})


# import tweepy
# from tweepy import OAuthHandler
#
# # api = twitter.Api(
# #     consumer_key='J5S0tA4qG5UK45gLOUccT4yBd',
# #     consumer_secret='6qsTntxDb5oxRpGCy9hjWHKtZVzkz7V0dY2vTAr04tM4D2ddnI',
# #     access_token_key='811159293751857224-qSPuXZ5NzYAuhBcF8fM1R4JAaLmxi83',
# #     access_token_secret='0CW7zVieofbn6tjlpp9HVbtJ1aoi9bkibunuY5QyPaXqu'
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
