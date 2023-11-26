from fastapi import FastAPI
from connector import connect_to_elasticsearch
from index import create_index, get_index_info
from search import search_keyword

app = FastAPI()
es = connect_to_elasticsearch()

# test
@app.get("/")
def read_root():
    return {"Hello": "World"}

# インデックス情報
@app.get('/es/index/info')
def get_index_info_route(index_name: str = "jawikinews"):
    return get_index_info(es)


# インデックス作成
@app.post('/es/create_index/{index_name}')
def create_index_route(index_name: str = "jawikinews"):
    create_index(es, index_name)
    return {"message": "index created."}


# クエリを指定して検索
@app.get('/search/{index_name}/{search_word}')
def search_keyword_route(index_name: str = "jawikinews", search_word: str = "日本"):
    return search_keyword(es, index_name, search_word)


