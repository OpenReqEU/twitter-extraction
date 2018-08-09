# -*- coding: utf-8 -*-

import logging
import nltk
from nltk.corpus import wordnet
import os
from application.util import helper
#from pattern.de import singularize, conjugate, predicative


_logger = logging.getLogger(__name__)
nltk.data.path = [os.path.join(helper.APP_PATH, "corpora", "nltk_data")]


def word_net_lemmatizer(requirements):
    _logger.info("Lemmatization for requirements' tokens")
    try:
        from nltk.stem.wordnet import WordNetLemmatizer
    except ImportError:
        raise RuntimeError('Please install nltk library!')

    def map_stanford_to_wordnet_tag(stanford_tag):
        '''
        if stanford_tag.startswith('JJ'):
            return wordnet.ADJ
        elif stanford_tag.startswith('VB'):
            return wordnet.VERB
        elif stanford_tag.startswith('NN'):
            return wordnet.NOUN
        elif stanford_tag.startswith('RB'):
            return wordnet.ADV
        else:
            return ''
        '''

        if stanford_tag.startswith(('ADJA', 'ADJD', 'ADV')):
            return wordnet.ADJ
        elif stanford_tag.startswith(('VVFIN', 'VVIMP', 'VVINF', 'VVIZU', 'VVPP')):
            return wordnet.VERB
        elif stanford_tag.startswith(('NA', 'NE', 'NN')):
            return wordnet.NOUN
        elif stanford_tag.startswith('RB'):
            return wordnet.ADV
        else:
            print(stanford_tag)
            return ''

    # Funkmodule (NN) -> Funkmodul
    def lemma_via_patternlib(token, pos):
        # ['Chink', 'Chunk', 'Context', 'Lexicon', 'Model', 'Morphology', 'Parser', 'article', 'attributive', 'commandline', 'comparative', 'conjugate', 'find_lemmata', 'gender', 'grade', 'inflect', 'lemma', 'lexeme', 'lexicon', 'ngrams', 'os', 'parse', 'parser', 'parsetree', 'penntreebank2universal', 'pluralize', 'pprint', 'predicative', 'referenced', 'singularize', 'split', 'stts', 'stts2penntreebank', 'stts2universal', 'superlative', 'sys', 'table', 'tag', 'tagset', 'tenses', 'tokenize', 'tree', 'verbs']
        if pos in ("NOUN", "NA", "NE", "NN"): #("NA", "NE", "NN"):
            # singularize noun
            #return singularize(token)
            return token
        elif pos in ("VERB", "VAFIN", "VAIMP", "VAINF", "VAPP", "VMFIN", "VMINF", "VMPP", "VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP"): # ("VAFIN", "VAIMP", "VAINF", "VAPP", "VMFIN", "VMINF", "VMPP", "VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP"):
            # get infinitive of verb
            return conjugate(token).lower()
        elif pos in ("AJD", "ADJA", "ADJD"): #("ADJA", "ADJD"):
            # get baseform of adjective
            return predicative(token).lower()
        elif pos in ("ADV", "PAV", "PROAV", "PAVREL", "PWAV", "PWAVREL"): #("ADV", "PAV", "PROAV", "PAVREL", "PWAV", "PWAVREL"):
            # get baseform of adverb
            return predicative(token).lower()
        return token

    lemmatizer = WordNetLemmatizer()

    for requirement in requirements:
        # English lemmatizer
        #requirement.title_tokens = [lemmatizer.lemmatize(pos_tag[0], map_stanford_to_wordnet_tag(pos_tag[1])) for pos_tag in requirement.title_tokens_pos_tags]
        #requirement.description_tokens = [lemmatizer.lemmatize(pos_tag[0], map_stanford_to_wordnet_tag(pos_tag[1])) for pos_tag in requirement.description_tokens_pos_tags]

        # German lemmatizer
        requirement.title_tokens = map(lambda pos_tag: lemma_via_patternlib(pos_tag[0], pos_tag[1]), requirement.title_tokens_pos_tags)
        requirement.description_tokens = map(lambda pos_tag: lemma_via_patternlib(pos_tag[0], pos_tag[1]), requirement.description_tokens_pos_tags)

