# elasticsearch_pg

## 参考資料
- https://techblog.zozo.com/entry/elasticsearch-mapping-config-for-japanese-search
- https://qiita.com/shin_hayata/items/41c07923dbf58f13eec4


## アナライザーの確認
- kuromoji
curl -X GET "localhost:9200/kaigo_swem_02/_analyze?pretty" -H 'Content-Type: application/json' -d'
{
  "analyzer": "kuromoji_normalize",
  "text": "寿司"
}
'
- なし
curl -X GET "localhost:9200/kaigo_swem_01/_analyze?pretty" -H 'Content-Type: application/json' -d'
{
  "text": "日本橋"
}
'