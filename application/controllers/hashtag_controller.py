import connexion
import six

from application.models.requirement import Requirement  # noqa: E501
from application.models.requirement_popularity import RequirementPopularity  # noqa: E501
from application.entities import requirement
from application.preprocessing import preprocessing
from application.twitter import twitter


# TODO: Calls are limited / Sth like 180 calls/day
# TODO: research about Tweepy

# TODO: update weights
weight_retweet_count = 1
weight_favorite_count = 50


def fetch_twitter(hashtag):
    response = twitter.fetch_tweets(hash_tags=['#{}'.format(hashtag)])
    #r = api.request('search/tweets', {'q':'@StettingerM', 'include_entities': True})
    #print(dir(response))
    #print(response.get_rest_quota())
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


def compute_popularity(body):  # noqa: E501
    """Retrieve a list with values for given set of requirements indicating their popularity for the crowd on twitter.

     # noqa: E501

    :param body: Requirement objects for which the social popularity should be measured
    :type body: list | bytes

    :rtype: List[RequirementPopularity]
    """
    response_list = []
    if connexion.request.is_json:
        content = connexion.request.get_json()
        assert isinstance(content, list)
        requirements = [Requirement.from_dict(d) for d in content]  # noqa: E501
        requirements = map(lambda r: requirement.Requirement(r.id, r.title, r.description), requirements)
        requirements = preprocessing.preprocess_requirements(requirements,
                                                             enable_pos_tagging=True,
                                                             enable_lemmatization=False,
                                                             enable_stemming=False)
        # Extend stop word list: https://www.wordfrequency.info/free.asp?s=y

        maut_results = []
        for requ in requirements:
            print(requ)
            maut_temp = 0
            if len(list(requ.title_tokens_pos_tags)) > 0:
                for tag in requ.title_tokens_pos_tags:
                    for matching_pos_classes in ["NN", "NE", "FW"]:
                        if matching_pos_classes in tag:
                            maut_temp += fetch_twitter(str(tag[0]))
            else:
                for token in requ.title:
                    maut_temp += fetch_twitter(token)
            maut_results.append(maut_temp)

        for idx, requ in enumerate(requirements):
            response_list.append(RequirementPopularity(
                id=requ.id,
                #'totalNumberOfFavorites': favorite_count,
                #'totalNumberOfRetweets': retweet_count,
                #'MAUT': (maut_result/num_of_tweets),
                #'popularity': "{0:.5f}".format((maut_results[i] / sum(maut_results))*100)
                popularity=((maut_results[idx] * 100) / sum(maut_results) if sum(maut_results) > 0 else 0)
            ))

    return response_list

