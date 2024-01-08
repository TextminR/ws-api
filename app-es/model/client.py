import os
from elasticsearch import AsyncElasticsearch

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
ELASTIC_HOST = os.getenv("ELASTIC_HOST")
ELASTIC_PORT = os.getenv("ELASTIC_PORT")
ELASTIC_USER = os.getenv("ELASTIC_USER")


def get_es_client():
    es = AsyncElasticsearch(
        [f"https://{ELASTIC_HOST}:{ELASTIC_PORT}"],
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        verify_certs=False
    )
    return es
