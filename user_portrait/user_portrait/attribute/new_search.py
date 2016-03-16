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
from user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.parameter import verified_num2ch_dict, IP_TIME_SEGMENT


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
    #get influence from es influence history
    try:
        influence_history = es_influence_history.get(index=influence_history_index_name, doc_type=influence_history_index_type, \
                id = uid)['_source']
    except:
        influence_history = []
    #get importance from es importance history
    try:
        importance_history = es_importance_history.get(index=importance_history_index_name, doc_type=importance_index_type, \
                id = uid)['_source']
    except:
        importance_history = []
    #get activeness from es activeness history
    try:
        activeness_history = es_activeness_history.get(index=activness_history_index_name, doc_type=activeness_index_type ,\
                id = uid)['_source']
    except:
        activeness_history = []
    #get sensitive from es sensitive history
    try:
        sensitive_history = es_sensitive_history.get(index=sensitive_history_index_name, doc_type=sensitive_index_type, \
                id = uid)['_source']
    except:
        sensitive_history = []

    results = {}
    return results

#use to get user location
def new_get_user_location(uid):
    results = {}
    now_date = ts2datetime(time.time())
    now_date_ts = datetime2ts(now_date)
    #now ip
    try:
        ip_time_string = r_cluster.hget('new_ip_'+str(now_date_ts), uid)
    except Exception, e:
        raise e
    if ip_time_string:
        ip_time_dict = json.loads(ip_time_string)
    else:
        ip_time_dict = {}
    ip_max_timestamp_list = [[ip, max(ip_time_dict[ip].split('&'))] for ip in ip_time_dict]
    sort_ip_timestamp = sorted(ip_max_timestamp, key=lambda x:int(x[1]), reverse=True)
    day_ip_list = [ip for ip in sort_ip_timestamp]
    try:
        now_ip = sort_ip_timestamp[0][0]
        now_city = ip2city(now_ip)
    except:
        now_ip = ''
        now_city = ''
    results['now_ip'] = [now_ip, now_city]
    #main ip
    day_result = {}
    week_result = {}
    for i in range(7, 0, -1):
        timestamp = now_date_ts - i * DAY
        try:
            ip_time_string = r_cluster.hget('new_ip_'+str(timestamp), uid)
        except:
            ip_time_string = {}
        if ip_time_string:
            ip_time_dict = json.loads(ip_time_string)
        else:
            ip_time_dict = {}
        for ip in ip_time_dict:
            ip_time_list = ip_time_dict[ip].split('&')
            for ip_timestamp in ip_time_list:
                ip_timesegment = (int(ip_timestamp) - now_day_ts) / IP_TIME_SEGMENT
                try:
                    day_result[ip_timesegment][ip] += 1
                except:
                    day_result[ip_timesegment] = {ip : 1}
                try:
                    week_result[ip] += 1
                except:
                    week_result[ip] = 1
    #main ip
    sort_week_result = sorted(week_result.items(), key=lambda x:x[1], reverse=True)
    if sort_week_result:
        main_ip = sort_week_result[0]
        main_city = ip2city(main_ip)
    else:
        main_ip = ''
        main_city = ''
    #abnormal ip
    week_ip_set = set(week_result.keys())
    abnormal_ip_set = set(day_ip_list) - week_ip_set
    abnormal_ip_list = list(abnormal_ip_set)
    sort_abnormal_ip_list = [ip for ip in day_ip_list if ip in abnoraml_ip_list]
    if len(sort_abnormal_ip_list) == 0:
        abnormal_ip = ''
        abnormal_city = ''
    else:
        abnormal_ip = sort_abnormal_ip_list[0]
        abnormal_city = ip2city(abnormal_ip)
    resuls['abnormal_ip'] = [abnormal_ip, abnormal_city]
    #home ip
    for i in range(0, 6):
        try:
            segment_dict = day_result[i]
        except:
            day_result[i] = {}
    home_segment_dict = day_result[0]
    sort_home_segment_dict = sorted(home_segment_dict.items(), key=lambda x:x[1], reverse=True)
    if sort_home_segment_dict:
        home_ip = sort_home_segment_dict[0]
        home_city = ip2city(home_ip)
    else:
        home_ip = ''
        home_city = ''
    results['home_ip'] = [home_ip, home_city]
    #job ip
    job_segment_dict = day_result[2]
    sort_job_segment_dict = sorted(job_segment_dict.items(), key=lambda x:x[1], reverse=True)
    if sort_job_segment_dict:
        job_ip = sort_job_segment_dict[0]
        job_city = ip2city(job_ip)
    else:
        job_ip = ''
        job_city = ''
    results['job_ip'] = [job_ip, job_city]
    return results

#ip2city
def ip2city(ip):
    try:
        city = IP.find(str(ip))
        if city:
            city = city.encode('utf-8')
        else:
            return None
        city_list = city.split('\t')
        if len(city_list)==4:
            city = '\t'.join(city_list[:3])
    except Exception,e:
        return None
    return city

#use to get user social
def new_get_user_social(uid):
    results = {}
    return results

#use to get user weibo
#sort_type = timestamp/retweet_count/comment_count/sensitive
def new_get_user_weibo(uid, sort_type):
    results = []
    weibo_list = []
    now_date = ts2datetime(time.time())
    for i in range(7, -1, -1):
        iter_date = ts2datetime(datetime2ts(now_date) - i * DAY)
        index_name = flow_text_index_name_pre + iter_date
        try:
            weibo_result = es_flow_text.search(index=index_name, doc_type=flow_text_index_type,\
                    query={'query':{'filtered':{'filter':{'term': {'uid': uid}}}}, 'sort':sort_type, 'size':100})
        except:
            weibo_result = []
        if weibo_result:
            weibo_list.extend(weibo_result)
    sort_weibo_list = sorted(weibo_list, key=lambda x:x[sort_type], reverse=True)[:100]
    for weibo_item in sort_weibo_list:
        uid = weibo_item['uid']
        text = weibo_item['text']
        ip = weibo_item['geo']
        city = ip2city(ip)
        results.append([uid, text, ip])
    return results
