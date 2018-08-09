# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger(__name__)


class Requirement(object):
    def __init__(self, id, title, description):
        self.id = int(id)
        self.title = title
        self.description = description
        self.title_tokens = []
        self.description_tokens = []
        self.title_tokens_pos_tags = []
        self.description_tokens_pos_tags = []

    def tokens(self, title_weight=1, description_weight=1):
        return (self.title_tokens * title_weight) + (self.description_tokens * description_weight)

    def pos_tokens(self, weight=1):
        return (map(lambda p: p[1], self.title_tokens_pos_tags) * weight)\
               + (map(lambda p: p[1], self.description_tokens_pos_tags) * weight)

    def __repr__(self):
      return self.__str__()

    def __str__(self):
        return "Requirement(id = {}, title = {}, description = {}...)"\
               .format(self.id, repr(self.title), repr(self.description)[:10])

