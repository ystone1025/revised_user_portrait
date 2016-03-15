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
