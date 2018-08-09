# -*- coding: utf-8 -*-

import nltk
import os
import logging
from application.util import helper
from nltk.corpus import stopwords


_logger = logging.getLogger(__name__)
nltk.data.path = [os.path.join(helper.APP_PATH, "corpora", "nltk_data")]


def remove_stopwords(requirements):
    _logger.info("Removing stop-words from requirement' tokens")
    # TODO: add additional German stop words if necessary...
    stop_words_file_path = os.path.join(helper.APP_PATH, 'corpora', 'stopwords')
    data_set_stop_words = set()
    with open(stop_words_file_path, 'rb') as f:
        for line in f:
            data_set_stop_words.add(line.strip())

    stop_words = set(stopwords.words('english') + list(data_set_stop_words))

    for requirement in requirements:
        requirement.title_tokens = filter(lambda t: t not in stop_words, requirement.title_tokens)
        requirement.description_tokens = filter(lambda t: t not in stop_words, requirement.description_tokens)

