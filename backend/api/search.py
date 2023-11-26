
def search_keyword(es, index_name, search_word, size=30):
    def create_query(search_word):
        """ クエリの作成
        Args:
            search_word (str): 検索クエリ
        Returns:
            dict: クエリ
        """

        script_query =  {
            "bool": {
            "should": [
                {
                    "match": {
                        "title": search_word
                    }
                },
                {
                    "match": {
                        "text": search_word
                    }
                }
            ]
            }
        }
        return script_query


    script_query = create_query(search_word)

    response = es.search(
        index=index_name,
        body={
            "size": size,
            "query": script_query,
            "_source": {"includes": ["title", "text"]}
        }
    )

    result = []
    for hit in response["hits"]["hits"]:
        title = hit["_source"]["title"]
        text = hit["_source"]["text"][:500]
        score = hit["_score"]
        result.append({"title": title, "text": text, "score": score})
    
    return result