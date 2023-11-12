from fastapi import Depends, FastAPI, HTTPException
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from gensim.models import KeyedVectors
from swem import MeCabTokenizer
from swem import SWEM

import os, pickle, time

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
@app.get('/search/{index_name}/{query}')
def search_query(index_name, query):
    query = query

    embedding_start = time.time()
    query_vector = swem.average_pooling(query).tolist()
    embedding_time = time.time() - embedding_start
    
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }
    
    search_start = time.time()
    response = es.search(
        index=index_name,
        body={
            "size": 10,
            "query": script_query,
            "_source": {"includes": ["title", "text"]}
        }
    )
    search_time = time.time() - search_start
    print(f"search_time: {search_time}")
    
    # TOP5
    hits = response["hits"]["hits"]
    result = []
    for i in range(5):
        title = hits[i]["_source"]["title"]
        text = hits[i]["_source"]["text"][:200]
        result.append(
            {"title": title, "text": text}
        )
        
    return result