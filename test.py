from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
resp = es.search(index="text_index", query={"match_all": {}})
