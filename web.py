#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import main
import json
from entities import requirement
from preprocessing import preprocessing

app = Flask(__name__)

# python .\web.py flask run
# http://0.0.0.0:9001/popularity/hashtag


@app.route("/popularity/hashtag/", methods=['GET', 'POST'])
def requirement_popularity():
    #print (request.is_json)
    content = request.get_json()
    #print (content)
    #print(type(content))
    assert isinstance(content, list)

    requirements = map(lambda d: requirement.Requirement(d["id"], d["title"], d["description"]), content)
    requirements = preprocessing.preprocess_requirements(requirements, enable_pos_tagging=True, enable_lemmatization=False, enable_stemming=False)
    # Extend stop word list: https://www.wordfrequency.info/free.asp?s=y

    response_dict = []
    maut_results = []
    for requ in requirements:
        maut_temp = 0
        #print requ.title_tokens
        #print requ.description_tokens
        print(requ.title_tokens_pos_tags)
        for tag in requ.title_tokens_pos_tags:
            for matching_pos_classes in ["NN", "NE", "FW"]:
                if matching_pos_classes in tag:
                    maut_temp += main.fetch_twitter(str(tag[0]))
        print(maut_temp)
        maut_results.append(maut_temp)
        #print requ.description_tokens_pos_tags
        print('-'*80)

    i = 0
    for requ in requirements:
        response_dict.append({
            'id': requ.id,
            #'totalNumberOfFavorites': favorite_count,
            #'totalNumberOfRetweets': retweet_count,
            #'MAUT': (maut_result/num_of_tweets),
            #'popularity': "{0:.5f}".format((maut_results[i] / sum(maut_results))*100)
            'popularity': ((maut_results[i] * 100) / sum(maut_results) if sum(maut_results) > 0 else 0)
        })
        i += 1

    return json.dumps(response_dict)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=9001)
