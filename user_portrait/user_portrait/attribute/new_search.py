# -*- coding: UTF-8 -*-
'''
use to get new attribute overview
write in version: 16-03-15
'''
import IP
import json
import time
from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type,\
                          es_flow_text, flow_text_index_name_pre, flow_text_index_type,\
                          es_user_profile, profile_index_name, profile_index_type
from user_portrait.global_utils import R_CLUSTER_FLOW2 as r_cluster
from user_portrait.global_utils import es_retweet, retweet_index_name_pre, retweet_index_type,\
                                     be_retweet_index_name_pre, be_retweet_index_type,\
                                     es_comment, comment_index_name_pre, comment_index_type,\
                                     be_comment_index_name_pre, be_comment_index_type
from user_portrait.global_utils import ES_COPY_USER_PORTRAIT, COPY_USER_PORTRAIT_INFLUENCE, COPY_USER_PORTRAIT_INFLUENCE_TYPE,\
              COPY_USER_PORTRAIT_IMPORTANCE, COPY_USER_PORTRAIT_IMPORTANCE_TYPE, COPY_USER_PORTRAIT_ACTIVENESS,\
              COPY_USER_PORTRAIT_ACTIVENESS_TYPE, COPY_USER_PORTRAIT_SENSITIVE, COPY_USER_PORTRAIT_SENSITIVE_TYPE
from user_portrait.parameter import verified_num2ch_dict, IP_TIME_SEGMENT, DAY, MAX_VALUE
from user_portrait.parameter import RUN_TYPE, RUN_TEST_TIME
from user_portrait.global_config import R_BEGIN_TIME
from user_portrait.time_utils import ts2datetime, datetime2ts, ts2date


evaluate_index_dict = {'bci': [COPY_USER_PORTRAIT_INFLUENCE, COPY_USER_PORTRAIT_INFLUENCE_TYPE], \
                       'importance': [COPY_USER_PORTRAIT_IMPORTANCE, COPY_USER_PORTRAIT_IMPORTANCE_TYPE],\
                       'activeness': [COPY_USER_PORTRAIT_ACTIVENESS, COPY_USER_PORTRAIT_ACTIVENESS_TYPE],\
                       'sensitive': [COPY_USER_PORTRAIT_SENSITIVE, COPY_USER_PORTRAIT_SENSITIVE_TYPE ]}

r_beigin_ts = datetime2ts(R_BEGIN_TIME)
FILTER_ITER_COUNT = 100

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

#get evaluate rank
def get_evaluate_rank(evaluate_ts, evaluate_value, evaluate_index):
    result = []
    evaluate_index_key = evaluate_index + '_' + str(evaluate_ts)
    query_body = {
        'query':{
            'range':{
                evaluate_index_key:{
                    'gte': evaluate_value,
                    'lt': MAX_VALUE
                    }
                }
            }
        }
    #get index_name, index_type
    index_infor_item = evaluate_index_dict[evaluate_index]
    index_name = index_infor_item[0]
    index_type = index_infor_item[1]
    evaluate_rank = ES_COPY_USER_PORTRAIT.count(index=index_name, doc_type=index_type, body=query_body)
    if evaluate_rank['_shards']['successful'] != 0:
        rank = evaluate_rank['count']
    else:
        rank = ''
    return rank


#use to get evaluate max/min/now_value/rank
def get_evaluate_max_min_now(history_dict, evaluate_index):
    results = []
    date_evaluate_dict = {}
    for item in history_dict:
        item_list = item.split('_')
        if len(item_list)==2 and item_list[0]==evaluate_index:
            evaluate_ts = int(item_list[1])
            date_evaluate_dict[evaluate_ts] = history_dict[item]
    sort_date_evaluate_list = sorted(date_evaluate_dict.items(), key=lambda x:x[0])
    sort_value_evaluate_list = sorted(date_evaluate_dict.items(), key=lambda x:x[1], reverse=True)
    #get now evaluate value and rank
    now_evaluate_value = sort_date_evaluate_list[-1][1]
    now_evaluate_ts = sort_date_evaluate_list[-1][0]
    now_evaluate_rank = get_evaluate_rank(now_evaluate_ts, now_evaluate_value ,evaluate_index)
    #get max evalute and min evaluate
    max_value = sort_value_evaluate_list[0][1]
    min_value = sort_value_evaluate_list[-1][1]
    results = [now_evaluate_value, now_evaluate_rank, max_value, min_value]
    return results

#use to get user evaluate index
#return result: [now_evaluate_value, now_evaluate_rank, max_value, min_value, all_count]
def new_get_user_evaluate(uid):
    results = {}
    #get all count in user_portrait
    query_body = {
            'query':{
                'match_all': {}
                }
            }
    all_count_results = es_user_portrait.count(index=portrait_index_name, doc_type=portrait_index_type, body=query_body)
    if all_count_results['_shards']['successful'] != 0:
        all_count = all_count_results['count']
    else:
        all_count = ''
    #get influence from es influence history
    try:
        influence_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_INFLUENCE, doc_type=COPY_USER_PORTRAIT_INFLUENCE_TYPE, \
                id = uid)['_source']
    except:
        influence_history = []
    #get max value/min value/week ave value
    if influence_history:
        influence_max_min_now_list =  get_evaluate_max_min_now(influence_history, 'bci')
        influence_max_min_now_list.append(all_count)
        results['influence'] = influence_max_min_now_list
    else:
        results['influence'] = ['', '', '', '', all_count]
    #get importance from es importance history
    try:
        importance_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_IMPORTANCE, doc_type=COPY_USER_PORTRAIT_IMPORTANCE_TYPE, \
                id = uid)['_source']
    except:
        importance_history = []
    #get max value/min value/now value
    if importance_history:
        importance_max_min_now_list = get_evaluate_max_min_now(importance_history, 'importance')
        importance_max_min_now_list.append(all_count)
        results['importance'] = importance_max_min_now_list
    else:
        results['importance'] = ['', '', '', '', all_count]
    #get activeness from es activeness history
    try:
        activeness_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_ACTIVENESS, doc_type=COPY_USER_PORTRAIT_ACTIVENESS_TYPE ,\
                id = uid)['_source']
    except:
        activeness_history = []
    #get max value/min value/ now value
    if activeness_history:
        activeness_max_min_now_list = get_evaluate_max_min_now(activeness_history, 'activeness')
        activeness_max_min_now_list.append(all_count)
        results['activeness'] = activeness_max_min_now_list
    else:
        results['activeness'] = ['', '', '', '', all_count]

    #get sensitive from es sensitive history
    try:
        sensitive_history = ES_COPY_USER_PORTRAIT.get(index=COPY_USER_PORTRAIT_SENSITIVE, doc_type=COPY_USER_PORTRAIT_SENSITIVE_TYPE, \
                id = uid)['_source']
    except:
        sensitive_history = []
    #get max value/min value/ now value
    if sensitive_history:
        sensitive_max_min_now_list = get_evaluate_max_min_now(sensitive_history, 'sensitive')
        sensitive_max_min_now_list.append(all_count)
        results['sensitive'] = sensitive_max_min_now_list
    else:
        results['sensitive'] = ['', '', '', '', all_count]
    
    return results

#use to get user location
def new_get_user_location(uid):
    results = {}
    now_date = ts2datetime(time.time())
    now_date_ts = datetime2ts(now_date)
    #run type
    if RUN_TYPE == 0:
        now_date_ts = datetime2ts(RUN_TEST_TIME) - DAY
        now_date = ts2datetime(now_date_ts)
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
    sort_ip_timestamp = sorted(ip_max_timestamp_list, key=lambda x:int(x[1]), reverse=True)
    day_ip_list = [ip_item[0] for ip_item in sort_ip_timestamp]
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
                ip_timesegment = (int(ip_timestamp) - timestamp) / IP_TIME_SEGMENT
                if ip_timesegment not in day_result:
                    day_result[ip_timesegment] = {}
                try:
                    day_result[ip_timesegment][ip] += 1
                except:
                    day_result[ip_timesegment][ip] = 1
                try:
                    week_result[ip] += 1
                except:
                    week_result[ip] = 1
    #main ip
    sort_week_result = sorted(week_result.items(), key=lambda x:x[1], reverse=True)
    if sort_week_result:
        main_ip = sort_week_result[0][0]
        main_city = ip2city(main_ip)
    else:
        main_ip = ''
        main_city = ''
    results['main_ip'] = [main_ip, main_city]
    #abnormal ip
    week_ip_set = set(week_result.keys())
    abnormal_ip_set = set(day_ip_list) - week_ip_set
    abnormal_ip_list = list(abnormal_ip_set)
    sort_abnormal_ip_list = [ip for ip in day_ip_list if ip in abnormal_ip_list]
    if len(sort_abnormal_ip_list) == 0:
        abnormal_ip = ''
        abnormal_city = ''
    else:
        abnormal_ip = sort_abnormal_ip_list[0][0]
        abnormal_city = ip2city(abnormal_ip)
    results['abnormal_ip'] = [abnormal_ip, abnormal_city]
    #home ip
    for i in range(0, 6):
        try:
            segment_dict = day_result[i]
        except:
            day_result[i] = {}
    home_segment_dict = day_result[0]
    sort_home_segment_dict = sorted(home_segment_dict.items(), key=lambda x:x[1], reverse=True)
    if sort_home_segment_dict:
        home_ip = sort_home_segment_dict[0][0]
        home_city = ip2city(home_ip)
    else:
        home_ip = ''
        home_city = ''
    results['home_ip'] = [home_ip, home_city]
    #job ip
    job_segment_dict = day_result[2]
    sort_job_segment_dict = sorted(job_segment_dict.items(), key=lambda x:x[1], reverse=True)
    if sort_job_segment_dict:
        job_ip = sort_job_segment_dict[0][0]
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


#use to get db num
def get_db_num(timestamp):
    date = ts2datetime(timestamp)
    date_ts = datetime2ts(date)
    db_number = ((date_ts - r_beigin_ts) / (DAY * 7)) % 2 + 1
    if RUN_TYPE == 0:
        db_number = 1
    return db_number

#union dict
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    return _total


#filter in user_portrait by uid
def filter_in_uid(input_dict):
    input_uid = input_dict.keys()
    all_count = len(input_uid)
    iter_count = 0
    in_portrait_result = []
    while iter_count < all_count:
        iter_user_list = input_uid[iter_count: iter_count+FILTER_ITER_COUNT]
        try:
            portrait_result = es_user_portrait.mget(index=portrait_index_name, doc_type=portrait_index_type,\
                    body={'ids': iter_user_list}, _source=False, fields=['photo_url', 'uname'])['docs']
        except:
            portrait_result = []
        if portrait_result:
            iter_in_portrait = [[item['_id'], item['fields']['uname'][0], item['fields']['photo_url'][0],input_dict[item['_id']]] for item in portrait_result if item['found']==True]
        in_portrait_result.extend(iter_in_portrait)
        iter_count += FILTER_ITER_COUNT
    
    return in_portrait_result

#filter in user_portrait by uname
def filter_in_uname(input_dict):
    input_uname = input_dict.keys()
    all_count = len(input_uname)
    iter_count = 0
    in_portrait_result = []
    while iter_count < all_count:
        iter_user_list = input_uname[iter_count: iter_count+FILTER_ITER_COUNT]
        try:
            portrait_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
                    body={'query':{'terms': {'uname': iter_user_list}}}, _source=False, fields=['photo_url', 'uname'])['hits']['hits']
        except:
            portrait_result = []
        if portrait_result:
            iter_in_portrait = [[item['_id'], item['uname'][0], item['photo_url'][0], input_uname[item['uname']]] for item in portrait_result]
        in_portrait_result.extend(iter_in_portrait)
        iter_count += FILTER_ITER_COUNT
    return in_portrait_result

#get interaction user
#retweet_comment_dict/be_retweet_comment_dict: [[id, uname, photo_url, count]]
def get_user_interaction(retweet_comment_list, be_retweet_comment_list):
    results = []
    retweet_comment_uid_set = set([item[0] for item in retweet_comment_list])
    be_retweet_comment_uid_set = set([item[0] for item in be_retweet_comment_list])
    if len(retweet_comment_uid_set) < len(be_retweet_comment_uid_set):
        iter_user_list = retweet_comment_list
    else:
        iter_user_list = be_retweet_comment_list
    interaction_uid_set = retweet_comment_uid_set & be_retweet_comment_uid_set
    interaction_uid_list = list(interaction_uid_set)
    if interaction_uid_list:
        results = [item for item in iter_user_list if item[0] in interaction_uid_list]

    return results

#search mention
def search_mention(uid):
    now_date_ts = datetime2ts(ts2datetime(time.time()))
    #run type
    if RUN_TYPE == 0:
        now_date_ts = datetime2ts(RUN_TEST_TIME)
    day_result_dict_list = []
    for i in range(7,0, -1):
        iter_ts = now_date_ts - i * DAY
        try:
            result_string = r_cluster.hget('at_' + str(ts), str(uid))
        except:
            result_string = ''
        if not result_string:
            continue
        day_result_dict = json.loads(results_string)
        day_result_dict_list.append(day_result_dict)
    if day_result_dict_list:
        week_result_dict = union_dict(day_result_dict_list)
    else:
        week_result_dict = {}
    return week_result_dict 

#get social domain statistic result
def get_social_domain(uid_set):
    results = {}
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{
                        'uid': list(uid_set)
                        }
                    }
                }
            },
        'aggs':{
            'all_domain':{
                'terms':{'field': 'domain'}
                }
            }
        }
    search_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type, \
            body=query_body)['aggregations']['all_domain']['buckets']
    print 'search_result:', search_result
    for item in search_result:
        results[item['key']] = item['doc_count']

    return results

#get social topic statistic result
def get_social_topic(uid_set):
    results = {}
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{
                        'uid': list(uid_set)
                        }
                    }
                }
            },
        'aggs':{
            'all_topic':{
                'terms':{'field': 'topic_string'}
                }
            }
        }
    search_result = es_user_portrait.search(index=portrait_index_name, doc_type=portrait_index_type,\
            body=query_body)['aggregations']['all_topic']['buckets']
    for item in search_result:
        results[item['key']] = item['doc_count']

    return results



#use to get user social
def new_get_user_social(uid):
    results = {}
    now_ts = time.time()
    db_number = get_db_num(now_ts)
    #step1:retweet/comment
    retweet_index_name = retweet_index_name_pre + str(db_number)
    comment_index_name = comment_index_name_pre + str(db_number)
    try:
        retweet_result = es_retweet.get(index=retweet_index_name, doc_type=retweet_index_type,\
                id=uid)['_source']['uid_retweet']
        retweet_result = json.loads(retweet_result)
    except:
        retweet_result = {}
    try:
        comment_result = es_comment.get(index=comment_index_name, doc_type=comment_index_type,\
                id=uid)['_source']['uid_comment']
        comment_result = json.loads(comment_result)
    except:
        comment_result = {}
    #union retweet and comment dict
    union_retweet_comment_result = union_dict(retweet_result, comment_result)
    try:
        union_retweet_comment_result.pop(uid)
    except:
        pass
    #filter who in in user_portrait by uid
    in_retweet_comment_result = filter_in_uid(union_retweet_comment_result) # [[id, uname, photo_url, count],...]
    top_user_retweet_comment = sorted(in_retweet_comment_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_retweet_comment'] = top_user_retweet_comment
    #step2:be_retweet/be_comment
    be_retweet_index_name = be_retweet_index_name_pre + str(db_number)
    be_comment_index_name = be_comment_index_name_pre + str(db_number)
    try:
        be_retweet_result = es_retweet.get(index=be_retweet_index_name, doc_type=be_retweet_index_type,\
                id=uid)['_source']['uid_be_retweet']
        be_retweet_result = json.loads(be_retweet_result)
    except:
        be_retweet_result = {}
    try:
        be_comment_result = es_comment.get(index=be_comment_index_name, doc_type=be_comment_index_type,\
                id=uid)['_source']['uid_be_comment']
        be_comment_result = json.loads(be_comment_result)
    except:
        be_comment_result = {}
    #union be_retweet and be_comment dict
    union_be_retweet_comment_result = union_dict(be_retweet_result, be_comment_result)
    try:
        union_be_retweet_comment_result.pop(uid)
    except:
        pass
    #filter who in user_portrait by uid
    in_be_retweet_comment_result = filter_in_uid(union_be_retweet_comment_result) # [[id, uname, photo_url, count],...]
    top_user_be_retweet_comment = sorted(in_be_retweet_comment_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_be_retweet_comment'] = top_user_be_retweet_comment
    #step3:interaction
    interaction_result = get_user_interaction(in_retweet_comment_result, in_be_retweet_comment_result)
    top_user_interaction = sorted(interaction_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_interaction'] = top_user_interaction
    #step4:at
    mention_result = search_mention(uid)
    #filter who in user_portrait
    in_mention_result = filter_in_uname(mention_result) # [[id, uname, photo_url, count],...]
    top_user_mention = sorted(in_mention_result, key=lambda x:x[3], reverse=True)[:20]
    results['top_mention'] = top_user_mention
    #step5:user domain and topic who in user_portrait
    in_retweet_comment_uid_set = set([item[0] for item in in_retweet_comment_result])
    in_be_retweet_comment_uid_set = set([item[0] for item in in_be_retweet_comment_result])
    in_mention_result = set([item[0] for item in in_mention_result])
    all_in_uid_set = in_retweet_comment_uid_set | in_be_retweet_comment_uid_set | in_mention_result - set([uid])
    #compute domain
    domain_statis_dict = get_social_domain(all_in_uid_set)
    sort_domain_statis_dict = sorted(domain_statis_dict.items(), key=lambda x:x[1], reverse=True)[:20]
    results['in_domain'] = sort_domain_statis_dict
    #compute topic
    topic_statis_dict = get_social_topic(all_in_uid_set)
    sort_topic_statis_dict = sorted(topic_statis_dict.items(), key=lambda x:x[1], reverse=True)[:20]
    results['in_topic'] = sort_topic_statis_dict

    return results

#use to get user weibo
#sort_type = timestamp/retweet_count/comment_count/sensitive
def new_get_user_weibo(uid, sort_type):
    results = []
    weibo_list = []
    now_date = ts2datetime(time.time())
    #run_type
    if RUN_TYPE == 0:
        now_date = RUN_TEST_TIME
        sort_type = 'timestamp'
    #step1:get user name
    try:
        user_profile_result = es_user_profile.get(index=profile_index_name, doc_type=profile_index_type,\
                id=uid, _source=False, fields=['nick_name'])
    except:
        user_profile_result = {}
    if user_profile_result:
        uname = user_profile_result['fields']['nick_name'][0]
    else:
        uname = ''
    #step2:get user weibo
    for i in range(7, 0, -1):
        iter_date = ts2datetime(datetime2ts(now_date) - i * DAY)
        index_name = flow_text_index_name_pre + iter_date
        try:
            weibo_result = es_flow_text.search(index=index_name, doc_type=flow_text_index_type,\
                    body={'query':{'filtered':{'filter':{'term': {'uid': uid}}}}, 'sort':sort_type, 'size':100})['hits']['hits']
        except:
            weibo_result = []
        if weibo_result:
            weibo_list.extend(weibo_result)
    print 'weibo_list:', weibo_list[0]
    sort_weibo_list = sorted(weibo_list, key=lambda x:x['_source'][sort_type], reverse=True)[:100]
    for weibo_item in sort_weibo_list:
        source = weibo_item['_source']
        uid = source['uid']
        text = source['text']
        ip = source['geo']
        date = ts2date(source['timestamp'])
        sentiment = source['sentiment']
        #run_type
        if RUN_TYPE == 1:
            retweet_count = source['retweet_count']
            comment_count = source['comment_count']
            sensitive_score = source['sensitive']
        else:
            retweet_count = 0
            comment_count = 0
            sensitive_score = 0
        city = ip2city(ip)
        results.append([uid, text, ip, city, date, retweet_count, comment_count, sensitive_score])

    return results
