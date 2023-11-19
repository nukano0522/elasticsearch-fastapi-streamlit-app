from fastapi import Depends, FastAPI, HTTPException
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from gensim.models import KeyedVectors
from swem import MeCabTokenizer
from swem import SWEM

# import streamlit as st

import os, pickle, time


### backend - FastAPI
MODEL_W2V = "wiki/w2v.pickle"

app = FastAPI()

print("###### model_loading #####")
es = Elasticsearch("http://elasticsearch_pg_elasticsearch_1:9200")

if os.path.exists(MODEL_W2V):
    print("Loading saved model...")
    with open(MODEL_W2V, mode="rb") as f:
        w2v = pickle.load(f)
    print("...Complete.")
        
else:
    print("Creating w2v model...")
    w2v_path = "./wiki/jawiki.word_vectors.200d.txt"
    w2v = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
    print("Saving model...")
    with open(MODEL_W2V, mode="wb") as f:
        pickle.dump(w2v, f)
    print("...Complete.")
    
tokenizer = MeCabTokenizer("-O wakati")
swem = SWEM(w2v, tokenizer)
    
# インデックス情報
@app.get('/es/index/info/{index_name}')
def get_index_info(index_name):
    index_exists = es.indices.exists(index=index_name)
    if index_exists:        
        doc_count = es.count(index=index_name)
        return {"index_exists": index_exists, "doc_count": doc_count["count"]}
    else:
        return {"index_exists": index_exists}
    

# クエリを指定して検索
@app.get('/search/{index_name}/{search_word}')
def search_query(index_name, search_word):
    
    def print_res(response):
        print("{} total hits.".format(response["hits"]["total"]["value"]))
        for hit in response["hits"]["hits"]:
            print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
            print(hit["_source"]["text"][:200])
            print()
            
    
    def create_query(search_word, is_vector=False):        
        if is_vector:
            query_vector = swem.average_pooling(search_word).tolist()
            script_query = {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            }
        else:
            script_query = {
                "match": {
                    "text": {
                        "query": search_word,
                    }
                }
            }
        return script_query
    
    script_query = create_query(search_word)
    
    response = es.search(
        index=index_name,
        body={
            "size": 30,
            "query": script_query,
            "_source": {"includes": ["text"]}
        }
    )
    
    result = []
    for hit in response["hits"]["hits"]:
        # title = hit["_source"]["title"]
        text = hit["_source"]["text"][:200]
        result.append({"text": text})
    
        
    return result


