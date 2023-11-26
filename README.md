# Elasticsearch + FastAPI + Streamlit を使った検索アプリ

## 実行環境
- Ubuntu 20.04.6 LTS (Focal Fossa)
- Docker version 20.10.25
- docker-compose version 1.29.0

## 準備

``` bash
# Wikipediaのデータを使うため、ダウンロードしておく
wget -P ./backend/api/data https://dumps.wikimedia.org/other/cirrussearch/20231120/jawikinews-20231120-cirrussearch-general.json.gz
```

## Usage
``` bash
# コンテナ立ち上げ
docker-compose up

# FastAPI経由でインデックス作成
curl -X POST http://localhost:8002/es/create_index/jawikinews
```
- http://localhost:8501/ からStreamlitアプリにアクセス


## Screenshots

Include screenshots or demo videos of the project here.

![Screenshot](image URL)



## 参考資料
- https://techblog.zozo.com/entry/elasticsearch-mapping-config-for-japanese-search
- https://qiita.com/shin_hayata/items/41c07923dbf58f13eec4




