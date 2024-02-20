from elasticsearch import Elasticsearch
from elasticsearch.helpers import async_scan


async def scroller_text(client, only_text, only_embeddings, include_text, include_embeddings):
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

    elif only_text:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}}, "_source": ["text"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)


    elif not only_text and not only_embeddings:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}},
                       "_source": ["author", "title", "year", "language", "source"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)

    elif include_text:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}},
                       "_source": ["author", "title", "year", "language", "source", "text"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)

    elif include_embeddings:
        async for hit in async_scan(
                client,
                query={"query": {"match_all": {}},
                       "_source": ["author", "title", "year", "language", "source", "embeddings"]},
                index="texts",
                scroll="1m",
                size=1000
        ):
            result.append(hit)

    return result


async def scroller_default(client, index):
    result = []
    async for hit in async_scan(
            client,
            query={"query": {"match_all": {}}},
            index=index,
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


async def data_to_list_text(response, only_text, only_embeddings, include_text, include_embeddings, scroller, sampled):
    if response != "No data":
        result = []
        document = {}
        if not scroller:
            zw = response['hits']['hits']
        else:
            zw = response
        for doc in zw:
            if not only_embeddings and not only_text:
                document = {
                    "_id": doc['_id'],
                    "author": doc['_source']['author'],
                    "title": doc['_source']['title'],
                    "year": doc['_source']['year'],
                    "language": doc['_source']['language'],
                    "source": doc['_source']['source']
                }

            elif only_text:
                document = {
                    "text": doc['_source']['text']
                }

            elif only_embeddings:
                document = {
                    "embeddings": doc['_source']['embeddings']
                }

            if include_text and not sampled:
                document["text"] = doc['_source']['text']

            if include_embeddings:
                document["embeddings"] = doc['_source']['embeddings']

            if sampled:
                document["text"] = doc['fields']['middle_part']

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
                "date": doc['_source']['date_publish'],
                "source": doc['_source']['source_domain'],
                "authors": doc['_source']['authors'],
                "language": doc['_source']['language']
            }
            if include_text:
                document["text"] = doc['_source']['maintext']
            result.append(document)
    else:
        for doc in response:
            document = {
                "_id": doc['_id'],
                "title": doc['_source']['title'],
                "date": doc['_source']['date_publish'],
                "source": doc['_source']['source_domain'],
                "authors": doc['_source']['authors'],
                "language": doc['_source']['language']
            }
            if include_text:
                document["text"] = doc['_source']['maintext']
            result.append(document)
    return result


async def build_query_text(client, id, author, title, minYear, maxYear, language, only_text, only_embeddings,
                           include_text, include_embeddings, sampled):
    query_parts = []
    response = "No data"
    sampler = {}

    if not id and not author and not title and not minYear and not maxYear and not language:
        zw = await scroller_text(client=client, only_text=only_text, only_embeddings=only_embeddings,
                                 include_text=include_text, include_embeddings=include_embeddings, sampled=sampled)
        return await data_to_list_text(response=zw, only_text=only_text, only_embeddings=only_embeddings, scroller=True,
                                       include_text=include_text, include_embeddings=include_embeddings,
                                       sampled=sampled)

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
    if sampled:
        sampler = {
            "middle_part": {
                "script": {
                    "source": """
                    def fifthPart = null;
                    def textArray = params['_source']['text'];
                    if (textArray != null && textArray.size() > 2) {
                        fifthPart = textArray[textArray.size()/2].part;
                    }
                return fifthPart;
                """
                }
            }
        }

    if only_embeddings:
        response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                                            "_source": ["embeddings"]})

    elif only_text:
        if sampled:
            response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                                                "_source": [], "script_fields": sampler})
        else:
            response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                                                "_source": ["text"]})

    elif include_text:
        if sampled:
            response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                                                "_source": ["id", "title", "author", "year", "language",
                                                                            "source"], "script_fields": sampler})
        else:
            response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                                                "_source": ["id", "title", "author", "year", "language",
                                                                            "source", "text"]})

    elif include_embeddings:
        response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                                            "_source": ["id", "title", "author", "year", "language",
                                                                        "source", "embeddings"]})

    elif not only_text and not only_embeddings and not include_text and not include_embeddings:
        response = await client.search(index="texts", body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                                            "_source": ["id", "title", "author", "year", "language",
                                                                        "source"]})
    return await data_to_list_text(response=response, only_text=only_text, only_embeddings=only_embeddings,
                                   scroller=False, include_text=include_text, include_embeddings=include_embeddings,
                                   sampled=sampled)


async def build_query_author(client, id, name, birth_place, country):
    query_parts = []
    if not id and not name and not birth_place and not country:
        zw = await scroller_default(client, "authors")
        return await data_to_list_author(response=zw, scroller=True)

    if id:
        query_parts.append({"match": {"_id": id}})
    if name:
        query_parts.append({"match": {"name": name}})
    if birth_place:
        query_parts.append({"match": {"birth_place": birth_place}})
    if country:
        query_parts.append({"match": {"country": country}})

    response = await client.search(index="authors", body={"query": {"bool": {"must": query_parts}}, "size": 1000, },
                                   timeout=60)
    return await data_to_list_author(response=response, scroller=False)


async def build_query_newsarticle(client, id, title, minDate, maxDate, source, author, language, include_text):
    query_parts = []
    if not id and not title and not minDate and not maxDate and not source and not author and not language:
        zw = await scroller_default(client, "newsarticles")
        return await data_to_list_newsarticle(zw, include_text, True)

    if id:
        query_parts.append({"match": {"_id": id}})

    if title:
        query_parts.append({"match": {"title": title}})

    if source:
        query_parts.append({"match": {"source_domain": source}})

    if author:
        query_parts.append({"match": {"authors": author}})

    if language:
        query_parts.append({"match": {"language": language}})

    range_query = {}
    if minDate:
        range_query["gte"] = minDate
    if maxDate:
        range_query["lte"] = maxDate

    if range_query:
        query_parts.append({"range": {"date_publish": range_query}})

    if include_text:
        response = await client.search(index="newsarticles",
                                       body={"query": {"bool": {"must": query_parts}}, "size": 1000})
    else:
        response = await client.search(index="newsarticles",
                                       body={"query": {"bool": {"must": query_parts}}, "size": 1000,
                                             "_source": ["title", "date_publish", "source_domain", "authors",
                                                         "language"]})
    return await data_to_list_newsarticle(response, include_text, False)


async def get_texts(client: Elasticsearch, id: list[str], title: list[str], minYear: int, maxYear: int,
                    author: list[str],
                    language: str, only_text, only_embeddings, include_text, include_embeddings, sampled: bool):
    return await build_query_text(client, id, author, title, minYear, maxYear, language, only_text, only_embeddings,
                                  include_text, include_embeddings, sampled)


async def get_authors(client: Elasticsearch, id: str, name: str, birth_place: str, country: str):
    return await build_query_author(client, id=id, name=name, birth_place=birth_place, country=country)


async def get_newsarticles(client: Elasticsearch, id: str, title: str, minDate: str, maxDate: str, source: str,
                           author: str, language: str, include_text):
    return await build_query_newsarticle(client, id, title, minDate, maxDate, source, author, language, include_text)
