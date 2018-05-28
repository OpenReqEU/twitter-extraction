# -*- coding: utf-8 -*-

import csv, logging, os
from entities.tag import Tag
from entities.post import Post
from util import helper

_logger = logging.getLogger(__name__)


def replace_tag_synonyms(tags, posts):
    synonyms_file_path = os.path.join(helper.APP_PATH, 'corpora', 'tags', 'synonyms')
    tag_name_replacement_map = {}
    with open(synonyms_file_path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            assert row[1] not in tag_name_replacement_map, "Synonym entry %s is ambiguous." % row[1]
            tag_name_replacement_map[row[1].strip()] = row[0].strip()

    tag_name_tag_map = dict(map(lambda t: (t.name, t), tags))
    remaining_tags = filter(lambda t: t.name not in tag_name_replacement_map, tags)
    counter_assigned_synonym_tags = 0
    for post in posts:
        assert isinstance(post, Post)
        new_tag_set = set()
        for old_tag in post.tag_set:
            if old_tag.name in tag_name_replacement_map:
                new_tag_name = tag_name_replacement_map[old_tag.name]
                if new_tag_name not in tag_name_tag_map:
                    _logger.debug("Can only replace tag with (other) existing tag %s", new_tag_name)
                    new_tag_set.add(old_tag) # keep old tag
                    continue
                new_tag = tag_name_tag_map[new_tag_name]
                _logger.debug("Replaced %s with %s", old_tag, new_tag)
                new_tag_set.add(new_tag) # replace old tag with new tag
                counter_assigned_synonym_tags += 1
            else:
                new_tag_set.add(old_tag) # keep old tag
        post.tag_set = new_tag_set
        assert len(post.tag_set) > 0 # sanity check

    _logger.info("Found and replaced %s synonym tags", len(tags) - len(remaining_tags))
    _logger.info("Replaced %s assignments of synonym tags in all posts", counter_assigned_synonym_tags)
    Tag.update_tag_counts_according_to_posts(remaining_tags, posts)
    return remaining_tags, posts


def replace_adjacent_tag_occurences(posts, tag_names):
    '''
        Replaces "-" by " " in all tag names e.g. "object-oriented" -> "object oriented"
        and then looks for two (or more) adjacent words that represent a known tag name
        e.g. current token list ["I", "love", "object", "oriented", "code"]
        -> should be converted to ["I", "love", "object-oriented", "code"]
        since "object-oriented" is a tag name in our tag list
    '''
    for tag_name in tag_names:
        if "-" not in tag_name:
            continue

        splitted_tag_name = tag_name.replace("-", " ")
        for post in posts:
            assert isinstance(post, Post)
            post.title = post.title.replace(splitted_tag_name, ' %s ' % tag_name)
            post.body = post.body.replace(splitted_tag_name, ' %s ' % tag_name)


def strip_invalid_tags_from_posts_and_remove_untagged_posts(posts, tags):
    '''
        Unassigns all removed tags from posts to avoid data-inconsistency issues.
        After that step a few posts may not contain tags any more (i.e. unlabeled instances).
        Therefore these posts are removed, since they became useless
        for both training and testing.
    '''
    _logger.info("Stripping invalid tags from posts and removing untagged posts")
    new_post_list = []
    for post in posts:
        assert isinstance(post, Post)
        post.tag_set = post.tag_set.intersection(tags) # removes invalid tags
        if len(post.tag_set) > 0: # removes untagged posts
            new_post_list.append(post)
    return new_post_list
