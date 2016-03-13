# -*- coding:utf-8 -*-
import os
import sys

reload(sys)
sys.path.append('../../')
from user_portrait.global_utils import es_user_portrait, portrait_index_name, portrait_index_type

#use to read task information from redis queue
def get_task_information():
    results = {}
    return results


#use to read task information from queue
def scan_sentiment_keywords_task():
    #step1: read task information from reids queue
    #step2: identify the task information is exist in es
    #step3: compute the sentiment trend task
    while True:
        #read task informaiton from redis queue
        sentiment_task_information = get_task_information()
        #when redis queue null - file break
        if not sentiment_task_information:
            break
        #identify the task is exist in es
        exist_mark = identify_task_exist(sentiment_task_information)
        if exist_mark:
            results = compute_sentiment_task(sentiment_task_information)
            #save results
            save_mark = save_task_results(results)
            #identify save status
            if not save_mark:
                #status fail: push task information to redis queue
                push_task_information(sentiment_task_information)
        else:
            #if no exist - pass
            pass



if __name__=='__main__':
    scan_sentiment_keywords_task()
