from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import os, pickle, time, json, gzip
import re
import pandas as pd

def get_index_info(es):
    """ インデックス一覧情報の取得
    Args:
        index_name (str): インデックス名
    Returns:
    """
    # インデックス一覧の取得
    indices = es.cat.indices(index="*", h='index').splitlines()
    # インデックスの表示
    indices_list = []
    for index in indices:
        if re.match(r"^[^.].*", index):
            indices_list.append(index)
    
    res = []
    for index in indices_list:
        doc_count = es.count(index=index)
        res.append({"index": index, "doc_count": doc_count["count"]})

    return res


def create_index(es, index_name="jawikinews"):
    """ インデックスの作成
    Args:
        es (Elasticsearch): Elasticsearchの接続情報
        index_name (str, optional): インデックス名. Defaults to "jawikinews".
    """
    
    es.indices.delete(index=index_name, ignore=[404])
    print(f"Deleted index {index_name}")
        
    with open("./config/index.json", "r") as f:
        mapping = json.load(f)

    es.indices.create(index=index_name, body=mapping)
    print(f"Created index {index_name}")

    if index_name == "jawikinews":
        def bulk_insert(docs):
            for doc in docs:
                yield {
                    "_op_type": "index",
                    "_index": index_name,
                    "title": doc["title"],
                    "text": doc["text"],
                }
        docs = []
        with gzip.open("./data/jawikinews-20231120-cirrussearch-general.json.gz") as f:
            for line in f:
                json_line = json.loads(line)
                if "index" not in json_line:
                    doc = json_line
                    docs.append(doc)
                    
        print("bulk insert start.")
        bulk(es, bulk_insert(docs))
        print("bulk insert end.")
        index_count = es.count(index=index_name)
        print(f"Indexed {index_count['count']} documents.")