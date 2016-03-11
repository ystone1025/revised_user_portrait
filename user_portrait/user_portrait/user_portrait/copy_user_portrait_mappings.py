# -*- coding: utf-8 -*-

import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from global_utils import es_user_portrait as es

index_info = {
    "settings":{
        "analysis":{
            "analyzer":{
                "my_analyzer":{
                    "type": "pattern",
                    "pattern": "&"
                }
            }
        }
    },

    "mappings":{
        "manage":{
            "properties":{
                "uid":{
                    "type": "string",
                    "index": "not_analyzed"
                },
                "aver_importance": {
                    "type": "double"
                },
                "aver_influence": {
                    "type": "double"
                },
                "aver_activeness": {
                    "type": "double"
                },
                "low_number": {
                    "type": "long"
                }
            }
        }
    }
}


es.indices.create(index="this_is_a_copy_user_portrait", body=index_info, ignore=400)

'''
es.indices.put_mapping(index='user_portrait_1222', doc_type='user', \
        body={'properties':{'character_text':{'type':'string', 'index':'not_analyzed'}, \
        'character_sentiment':{'type':'string', 'index':'not_analyzed'}}}, ignore=400)
'''
