#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    main -- Main entry point

    main is a function in this module that performs all steps of the entire pipeline

    usage:      python -m main

    @author:     Ralph Samer, Müslüm Atas
    @license:    MIT license
'''

import sys
import json
import twitter

#TODO: Calls are limited / Sth like 180 calls/day
# TODO: research about Tweepy

# TODO: update weights
weight_retweet_count = 1
weight_favorite_count = 50

def fetch_twitter(hashtag):
    response = twitter.fetch_tweets(hash_tags=['#{}'.format(hashtag)])
    #r = api.request('search/tweets', {'q':'@StettingerM', 'include_entities': True})
    #print(dir(response))
    print(response.get_rest_quota())
    #print(response.headers)
    # import sys;sys.exit()

    i = 0
    #favorite_count = 0
    #retweet_count = 0
    maut_result = 0
    for item in response:
        #print(item["id"])
        #print(item["text"])
        #print(item["favorite_count"])
        #print(item["retweet_count"])
        #print(json.dumps(item, indent=2, sort_keys=True))
        #print(str(item["entities"]["hashtags"]) + '\n')
        i += 1
        maut_result += weight_favorite_count*int(item["favorite_count"]) + weight_retweet_count*int(item["retweet_count"])
        #print(i, int(item["favorite_count"]), int(item["retweet_count"]));
        #favorite_count += int(item["favorite_count"])
        #retweet_count += int(item["retweet_count"])
    return (maut_result/i)

def main():
    favorite_count, retweet_count, maut_result, num_of_tweets = fetch_twitter()
    #print('-' * 80)
    #print('Total number of favorites: %d' % (favorite_count))
    #print('Total number of retweets: %d' % (retweet_count))
    #print("MAUT = %d" % (maut_result/num_of_tweets))
    #print("popularity = {0:.0f}%".format((maut_result/num_of_tweets/denominator) * 100))
    return 0

if __name__ == "__main__":
    sys.exit(main())