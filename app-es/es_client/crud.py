from elasticsearch import Elasticsearch


def build_query(author, minYear, maxYear, language):
    query_parts = []

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


def metadata_to_list(response):
    result = []
    for doc in response['hits']['hits']:
        document = {
            "_id": doc['_id'],
            "author": doc['_source']['author'],
            "title": doc['_source']['title'],
            "year": doc['_source']['year'],
            "language": doc['_source']['language']
        }
        result.append(document)
    return result


def get_metadata_filter(client: Elasticsearch, minYear: int, maxYear: int, author: str, language: str):
    query = build_query(author, minYear, maxYear, language)
    response = client.search(index="text_index", body={"query": query})
    return metadata_to_list(response=response)
