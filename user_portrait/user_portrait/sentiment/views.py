#-*- coding:utf-8 -*-

import os
import json
from flask import Blueprint, url_for, render_template, request,\
                    abort, flash, session, redirect
from utils import search_sentiment_all, search_sentiment_all_keywords,\
                  search_sentiment_domain, search_senitment_topic
from user_portrait.global_utils import es_flow_text, flow_text_index_name_pre, \
                flow_text_index_type, es_user_portrait, portrait_index_name ,\
                portrait_index_type


mod = Blueprint('sentiment', __name__, url_prefix='/sentiment')

#use to get all sentiment trend
@mod.route('/sentiment_all/')
def ajax_sentiment_all():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '') # limited by latest month
    results = search_sentiment_all(start_date, end_date)
    if not results:
        results = {}
    return json.dumps(results)

#use to submit all keywords sentiment trend compute task to redis and es
@mod.route('submit_sentiment_all_keywords')
def ajax_submit_sentiment_all_keywords():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    keywords_string = request.args.get('keywords', '') #keywords_string=word1,word2
    results = submit_sentiment_all_keywords(keywords_string, start_date, end_date)
    if not results:
        results = {}
    return json.dumps(results)

#use to show all keywords sentiment task compute status
@mod.route('show_sentiment_all_keywords_task')
def ajax_show_sentiment_all_keywords_task():
    submit_user = request.args.get('submit_user','')
    results = show_submit_sentiment_all_keywords_task(submit_user)
    if not results:
        results = {}
    return json.dumps(results)


#use to get all keywords sentiment trend
@mod.route('show_sentiment_all_keywords_results')
def ajax_senitment_all_keywords():
    keywords_string = request.args.get('keywords', '')
    start_date = request.args.get('start_date','')
    end_date = request.args.get('end_date', '') #limited by lastest month
    results = search_sentiment_all_keywords(keywords_string, start_date, end_date)
    if not results:
        results = {}
    return json.dumps(results)

#use to get domain sentiment trend for user in user_portrait
@mod.route('sentiment_domain')
def ajax_sentiment_domain():
    domain = request.args.get('domain', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '') #limited by lastest month
    results = search_sentiment_domain(domain, start_date, end_date)
    if not results:
        results = {}
    return json.dumps(results)

#use to get topic sentiment trend for user in user_portrait
@mod.route('sentiment_topic')
def ajax_senitment_topic():
    topic = request.args.get('topic', '')
    start_date = request.args.get('start_date', '')
    end_date = request.arg.get('end_date', '') #limited by latest month
    results = search_sentiment_topic(topic, start_date, end_date)
    if not results:
        results = {}
    return json.dumps(results)
