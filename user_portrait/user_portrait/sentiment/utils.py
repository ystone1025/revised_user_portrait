#-*- coding:utf-8 -*-
import sys
import json


from user_portrait.global_utils import es_user_portrait, portrait_index_name,\
                                     portrait_index_type, es_flow_text, flow_text_index_name_pre ,\
                                     flow_text_index_type
from user_portrait.time_utils import ts2datetime


#use to get all sentiment trend by date
def search_sentiment_all(start_date, end_date):
    results = {}
    return results

#use to get all keywords sentiment trend by date
def search_sentiment_all_keywords(keywords_string, start_date, end_date):
    results = {}
    return results


#use to submit keywords sentiment trend task
def submit_sentiment_all_keywords(keywords_string, start_date, end_date):
    results = {}
    return results

#use to get domain sentiment trend by date for user in user_portrait
def search_sentiment_domain(domain, start_date, end_date):
    results = {}
    return results

#use to get topic sentiment trend by date for user in user_portrait
def search_senitment_topic(topic, start_date, end_date):
    results = {}
    return results
