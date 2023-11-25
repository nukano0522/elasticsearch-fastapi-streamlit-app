from fastapi import Depends, FastAPI, HTTPException
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import os, pickle, time, json
import pandas as pd


app = FastAPI()

print("###### model_loading #####")
# Elasticsearchのコンテナが立ち上がるまで接続試行する
conn = False
try_num = 0
while not conn:
    try:
        es = Elasticsearch(
            "https://es01:9200",
            ca_certs="./ca.crt",
            basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
        )
        
        es_info = es.info()
        conn = True
    except:
        print("try connecting to elasticsearch...")
        try_num += 1
        time.sleep(3)
        if try_num >= 10:
            print("connection failed.")
            break
print("Connection to elasticsearch is complete.")
print(f"es-info: {es.info()}")

@app.get("/")
def read_root():
    return {"Hello": "World"}

# インデックス情報
@app.get('/es/index/info/{index_name}')
def get_index_info(index_name):
    index_exists = es.indices.exists(index=index_name)
    if index_exists:        
        doc_count = es.count(index=index_name)
        return {"index_exists": index_exists, "doc_count": doc_count["count"]}
    else:
        return {"index_exists": index_exists}

# インデックス作成
@app.post('/es/create_index/{index_name}/{data_path}')
def create_index(index_name, data_path):
    index_exists = es.indices.exists(index=index_name)
    if index_exists:
        # return {"message": "index already exists."}
        es.indices.delete(index=index_name, ignore=[404])
        print(f"Deleted index {index_name}")
        
    with open("./config/index.json", "r") as f:
        mapping = json.load(f)

    es.indices.create(index=index_name, body=mapping)

    df = pd.read_csv("./data/生活記録DAR_20220702_TSV", sep="\t")
    dar_text = df[(df["DAR内容"].notnull()) & (df["DAR内容"].str.len()>10)]["DAR内容"].values
    print(len(dar_text))
    
    # データをインデックスに登録
    def bulk_insert(docs):
        for doc in docs:
            yield {
                "_op_type": "index",
                "_index": index_name,
                "text": doc,
            }
    
    print("bulk insert start.")
    bulk(es, bulk_insert(dar_text))
    print("bulk insert end.")
    
    return {"message": "index created."}

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
        text = hit["_source"]["text"][:200]
        result.append({"text": text})
    
        
    return result


