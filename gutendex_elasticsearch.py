import requests
from elasticsearch import Elasticsearch
#import tensorflow as tf
#from transformers import AutoModel

es = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=("elastic", "GZLhtJXfckU-DcYQLgYU"),
    verify_certs=False
)
print(es.info())
response = requests.get("https://gutendex.com/books/?page=1", headers={"Accept": "application/json"})
gutendex_array = response.json().get("results")
#model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True)
#i = 1

for book in gutendex_array:

    if not book.get("copyright"):
        autor = ""
        if len(book.get("authors")) == 0:
            autorname = "unknown"
        else:
            autor = book.get("authors")[0]
            autorname = autor.get("name")

        if len(book.get("languages")) == 0:
            language = "unknown"
        else:
            language = book.get("languages")[0]

        if autor.get("birth_year") is not None and autor.get("death_year") is not None:
            year = (autor.get("birth_year") + autor.get("death_year")) / 2
        else:
            year = -111111111

        titel = book.get("title")
        text = book.get("formats").get("text/plain; charset=utf-8", None)

        if text is None:
            text = book.get("formats").get("text/plain; charset=us-ascii", None)

        if text is None:
            text = book.get("formats").get("text/plain", None)

        if text is not None:
            text = requests.get(text).text

            index_start = text.find("** START")
            index_start = text.find('\n', index_start) + 1
            index_end = text.find("** END")
            text = text[index_start:index_end]

            #text_chunks = [chunk.strip() for chunk in text.split("\r\n\r\n") if chunk.strip()]
            #print(text)
            #for chunk in text_chunks:
                #print(chunk)
                #chunk = chunk.strip().replace("\n", " ").replace("\r", " ")
                #embedding = model.encode([chunk])

                #if embedding.shape[1] != 512:
                    #resize_layer = tf.keras.layers.Dense(512, input_shape=(embedding.shape[1],))
                    #embedding = resize_layer(embedding)

            document = {
                "author": autorname,
                "title": titel,
                "year": year,
                "language": language,
                "source": "gutenberg",
                "text": text
                #"embedding": [0]
            }

            res = es.index(index="text_index", document=document)
                #print(f"Dokument {titel} mit ID {i} erstellt.")
    #i += 1
