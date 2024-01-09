from elasticsearch import Elasticsearch
from elasticsearch.helpers import async_scan


async def scroller_text(client, include_text, include_embeddings, only_embeddings):
    result = []
    if only_embeddings:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}}, "_source": ["embeddings"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)

    elif not include_text and not include_embeddings:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}}, "_source": ["author", "title", "year", "language", "source"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)
    elif include_text and not include_embeddings:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}}, "_source": ["author", "title", "year", "language", "source", "text"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)
    elif not include_text and include_embeddings:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}}, "_source": ["author", "title", "year", "language", "source", "embeddings"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)
    elif include_text and include_embeddings:
        result = scroller_default(client)
    return result


async def scroller_default(client):
    result = []
    async for hit in async_scan(
            client,
            query={"query": {"match_all": {}}},
            index="authors",
            scroll="1m",
            size=1000
    ):
        result.append(hit)
    return result


async def data_to_list_author(response, scroller):
    result = []
    if not scroller:
        for doc in response['hits']['hits']:
            document = {
                "_id": doc['_id'],
                "name": doc['_source']['name'],
                "birth_place": doc['_source']['birth_place'],
                "lat": doc['_source']['lat'],
                "long": doc['_source']['long'],
                "country": doc['_source']['country']
            }
            result.append(document)
    else:
        for doc in response:
            document = {
                "_id": doc['_id'],
                "name": doc['_source']['name'],
                "birth_place": doc['_source']['birth_place'],
                "lat": doc['_source']['lat'],
                "long": doc['_source']['long'],
                "country": doc['_source']['country']
            }
            result.append(document)
    return result


async def data_to_list_text(response, include_text, include_embeddings, only_embeddings, scroller):
    if response != "No data":
        result = []
        document = {}
        if not scroller:
            zw = response['hits']['hits']
        else:
            zw = response
        for doc in zw:
            if not only_embeddings:
                document = {
                    "_id": doc['_id'],
                    "author": doc['_source']['author'],
                    "title": doc['_source']['title'],
                    "year": doc['_source']['year'],
                    "language": doc['_source']['language'],
                    "source": doc['_source']['source']
                }
                if include_text:
                    document["text"] = doc['_source']['text']
            if include_embeddings or only_embeddings:
                document["embeddings"] = doc['_source']['embeddings']
            result.append(document)
        return result
    return "No data"


async def data_to_list_newsarticle(response, include_text, scroller):
    result = []
    if not scroller:
        for doc in response['hits']['hits']:
            document = {
                "_id": doc['_id'],
                "title": doc['_source']['title'],
                "date": doc['_source']['date'],
                "source": doc['_source']['source'],
                "author": doc['_source']['author'],
                "language": doc['_source']['language']
            }
            if include_text:
                document["text"] = doc['_source']['text']
            result.append(document)
    else:
        for doc in response:
            document = {
                "_id": doc['_id'],
                "title": doc['_source']['title'],
                "date": doc['_source']['date'],
                "source": doc['_source']['source'],
                "author": doc['_source']['author'],
                "language": doc['_source']['language']
            }
            if include_text:
                document["text"] = doc['_source']['text']
            result.append(document)
    return result


async def build_query_text(client, id, author, title, minYear, maxYear, language, include_text, include_embeddings, only_embeddings):
    query_parts = []
    response = "No data"

    if not id and not author and not title and not minYear and not maxYear and not language:
        zw = await scroller_text(client=client, include_text=include_text, include_embeddings=include_embeddings, only_embeddings=only_embeddings)
        return await data_to_list_text(response=zw, include_text=include_text, include_embeddings=include_embeddings, only_embeddings=only_embeddings, scroller=True)

    if id:
        query_parts.append({"terms": {"_id": id}})

    if author:
        query_parts.append({"terms": {"author": author}})

    if title:
        query_parts.append({"terms": {"title": title}})

    if language:
        query_parts.append({"match": {"language": language}})

    range_query = {}
    if minYear:
        range_query["gte"] = minYear
    if maxYear:
        range_query["lte"] = maxYear

    if range_query:
        query_parts.append({"range": {"year": range_query}})

    if only_embeddings:
        response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 100,
                                                            "_source": ["embeddings"]})

    elif include_text and include_embeddings:
        response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 100})
    else:
        if include_text and not include_embeddings:
            response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 100,
                                                                "_source": ["author", "title", "year", "language",
                                                                            "source", "text"]})
        if include_embeddings and not include_text:
            response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 100,
                                                                "_source": ["author", "title", "year", "language",
                                                                            "source", "embeddings"]})
        if not include_text and not include_embeddings:
            response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 100})
    return await data_to_list_text(response=response, include_text=include_text, include_embeddings=include_embeddings, only_embeddings=only_embeddings, scroller=False)


async def build_query_author(client, id, name, birth_place, country):
    query_parts = []
    if not id and not name and not birth_place and not country:
        zw = await scroller_default(client)
        return await data_to_list_author(response=zw, scroller=True)

    if id:
        query_parts.append({"match": {"_id": id}})
    if name:
        query_parts.append({"match": {"name": name}})
    if birth_place:
        query_parts.append({"match": {"birth_place": birth_place}})
    if country:
        query_parts.append({"match": {"country": country}})

    response = await client.search(index="authors", body={"query": {"bool": {"must": query_parts}}, "size": 100})
    return await data_to_list_author(response=response, scroller=False)


async def build_query_newsarticle(client, id, title, minDate, maxDate, source, author, language, include_text):
    query_parts = []
    if not id and not title and not minDate and not maxDate and not source and not author and not language:
        zw = await scroller_default(client)
        return await data_to_list_newsarticle(zw, include_text, True)

    if id:
        query_parts.append({"match": {"_id": id}})

    if title:
        query_parts.append({"match": {"title": title}})

    if source:
        query_parts.append({"match": {"source": source}})

    if author:
        query_parts.append({"match": {"author": author}})

    if language:
        query_parts.append({"match": {"language": language}})

    range_query = {}
    if minDate:
        range_query["gte"] = minDate
    if maxDate:
        range_query["lte"] = maxDate

    if range_query:
        query_parts.append({"range": {"year": range_query}})

    if include_text:
        response = await client.search(index="newsarticles",
                                       body={"query": {"bool": {"must": query_parts}}, "size": 100})
    else:
        response = await client.search(index="newsarticles",
                                       body={"query": {"bool": {"must": query_parts}}, "size": 100,
                                             "_source": ["title", "date", "source", "author",
                                                         "language"]})
    return data_to_list_newsarticle(response, include_text, False)


async def get_texts(client: Elasticsearch, id: list[str], title: list[str], minYear: int, maxYear: int,
                    author: list[str],
                    language: str, include_text, include_embeddings, only_embeddings):
    return await build_query_text(client, id, author, title, minYear, maxYear, language, include_text,
                                  include_embeddings, only_embeddings)


async def get_authors(client: Elasticsearch, id: str, name: str, birth_place: str, country: str):
    return await build_query_author(client, id=id, name=name, birth_place=birth_place, country=country)


async def get_newsarticles(client: Elasticsearch, id: str, title: str, minDate: str, maxDate: str, source: str,
                           author: str, language: str, include_text):
    return await build_query_newsarticle(client, id, title, minDate, maxDate, source, author, language, include_text)
