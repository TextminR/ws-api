from ssl import create_default_context

from elasticsearch import Elasticsearch

ELASTIC_PASSWORD = "NXbH08hH*jzw=swo6AC3"


def get_es_client():
    context = create_default_context(cafile="es_client/http_ca.crt")

    es = Elasticsearch(
        ['https://localhost:9200'],
        basic_auth=('elastic', ELASTIC_PASSWORD),
        ssl_context=context
    )

    return es
