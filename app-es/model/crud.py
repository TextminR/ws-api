from elasticsearch import Elasticsearch


def build_query(id, author, minYear, maxYear, language):
    query_parts = []

    if id:
        query_parts.append({"match": {"_id": id}})

    if author:
        query_parts.append({"match": {"author": author}})

    if language:
        query_parts.append({"match": {"language": language}})

    range_query = {}
    if minYear:
        range_query["gte"] = minYear
    if maxYear:
        range_query["lte"] = maxYear

    if range_query:
        query_parts.append({"range": {"year": range_query}})

    return {"bool": {"must": query_parts}}


def data_to_list(response, method):
    result = []
    for doc in response['hits']['hits']:
        document = {
            "_id": doc['_id'],
            "author": doc['_source']['author'],
            "title": doc['_source']['title'],
            "year": doc['_source']['year'],
            "language": doc['_source']['language']
            # "embedding": doc['_source']['embedding']
        }
        if method == "text":
            document = {
                "_id": doc['_id'],
                "author": doc['_source']['author'],
                "title": doc['_source']['title'],
                "year": doc['_source']['year'],
                "language": doc['_source']['language'],
                # "embedding": doc['_source']['embedding'],
                "text": doc['_source']['text']
            }
        result.append(document)
    return result


def get_metadata(client: Elasticsearch, id: str, minYear: int, maxYear: int, author: str, language: str):
    query = build_query(id, author, minYear, maxYear, language)
    response = client.search(index="text_index", body={"query": query, "size": 100})
    return data_to_list(response=response, method="")


def get_texts(client: Elasticsearch, id: str, minYear: int, maxYear: int, author: str, language: str):
    query = build_query(id, author, minYear, maxYear, language)
    response = client.search(index="text_index", body={"query": query, "size": 100})
    return data_to_list(response=response, method="text")
