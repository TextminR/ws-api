import os
from elasticsearch import AsyncElasticsearch

# ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
# ELASTIC_HOST = os.getenv("ELASTIC_HOST")
# ELASTIC_PORT = os.getenv("ELASTIC_PORT")
# ELASTIC_USER = os.getenv("ELASTIC_USER")

ELASTIC_HOST = "localhost"
ELASTIC_PORT = 9200
ELASTIC_USER = "elastic"
ELASTIC_PASSWORD = "GZLhtJXfckU-DcYQLgYU"


def get_es_client():
    es = AsyncElasticsearch(
        [f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"],
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        verify_certs=False
    )
    return es
