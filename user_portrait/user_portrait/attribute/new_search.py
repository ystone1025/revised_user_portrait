# -*- coding: UTF-8 -*-
'''
use to get new attribute overview
write in version: 16-03-15
'''
import IP
import json

from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type,\
                          es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                          es_user_profile, profile_index_name, profile_index_type
from user_portrait.parameter import verified_num2ch_dict


#use to get user profile information
def new_get_user_profile(uid):
    try:
        results = es_user_profile.get(index=profile_index_name, doc_type=profile_index_type,\
                id=uid)['_source']
    except:
        results = {}
    if not results:
        results['uid'] = uid
        results['photo_url'] = ''
        results['nick_name'] = ''
        results['verified_type'] = ''
        results['verified_type_ch'] = ''
        results['fansnum'] = ''
        results['friendsnum'] = ''
        results['statusnum'] = ''
        results['user_location'] = ''
        results['description'] = ''
    else:
        verified_num_type = results['verified_type']
        verified_ch_type = verified_num2ch_dict[verified_num_type]
        results['verified_type_ch'] = verified_ch_type

    return results

#use to get tag information/sensitive_words&keywords&hashtag/domain&topic&character
def new_get_user_portrait(uid, admin_user):
    results = {}
    try:
        user_portrait_result = es_user_portrait.get(index=portrait_index_name, doc_type=portrait_index_type,\
                id=uid)['_source']
    except:
        user_portrait_result = {}
    if not user_portrait_result:
        results['tag_remark'] = {}
        results['attention_information'] = {}
        results['tendency'] = {}
    else:
        #step1: get attention_information
        #sensitive words
        try:
            sensitive_words_dict = json.loads(user_portrait_result['sensitive_words_dict'])
        except:
            sensitive_words_dict = {}
        sort_sensitive_words = sorted(sensitive_words_dict.items(), key=lambda x:x[1], reverse=True)
        results['attention_information'] = {'sensitive_words': sort_sensitive_words}
        #keywords
        sort_keywords = json.loads(user_portrait_result['keywords'])
        results['attention_information']['keywords'] = sorted(sort_keywords)
        #hashtag
        hashtag_dict = json.loads(user_portrait_result['hashtag_dict'])
        sort_hashtag = sorted(hashtag_dict.items(), key=lambda x:x[1], reverse=True)
        results['attention_information']['hashtag'] = sort_hashtag
        #step2: get tendency_information
        results['tendency'] = {'domain':user_portrait_result['domain']}
        results['tendency']['topic'] = user_portrait_result['topic_string'].split('&')[0]
        results['tendency']['character_sentiment'] = user_portrait_result['character_sentiment']
        results['tendency']['character_text'] = user_portrait_result['character_text']
        #step3: get tag_information
        #tag
        try:
            admin_tag = user_portrait_result[admin_user]
        except:
            admin_tag = {}
        if not admin_tag:
            results['tag_remark'] = {'tag': []}
        else:
            tag_list = admin_tag.split('&')
            results['tag_remark'] = {'tag': tag_list}
        #remark
        try:
            remark = user_portrait_result['remark']
        except:
            remark = ''
        results['tag_remark']['remark'] = remark

    return results

#use to get user evaluate index
def new_get_user_evaluate(uid):
    results = {}
    return results

#use to get user location
def new_get_user_location(uid):
    results = {}
    return results

#use to get user social
def new_get_user_social(uid):
    results = {}
    return results

#use to get user weibo
def new_get_user_weibo(uid, sort_type):
    results = {}
    return results
