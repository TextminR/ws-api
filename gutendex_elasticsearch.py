import requests
from elasticsearch import Elasticsearch
import tensorflow as tf
from transformers import AutoModel
from ssl import create_default_context

context = create_default_context(cafile="http_ca.crt")
ELASTIC_PASSWORD = "NXbH08hH*jzw=swo6AC3"

es = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=('elastic', ELASTIC_PASSWORD),
    ssl_context=context
)
print(es.info())
response = requests.get("https://gutendex.com/books/?page=1", headers={"Accept": "application/json"})
gutendex_array = response.json().get("results")

for book in gutendex_array:

    if not book.get("copyright"):

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
            text = text.strip().replace("\n", " ").replace("\r", " ")

            model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True)
            embedding = model.encode([text])

            if embedding.shape[1] != 512:
                # Hier verwenden wir eine einfache lineare Schicht zur Dimensionalitätsreduktion/Erhöhung
                resize_layer = tf.keras.layers.Dense(512, input_shape=(embedding.shape[1],))
                embedding = resize_layer(embedding)

            document = {
                "author": autorname,
                "title": titel,
                "year": year,
                "language": language,
                "text": text,
                "embedding": embedding[0]  # Beispiel-Embedding
            }

            print(autorname, titel, year, language, embedding)

            res = es.index(index="text_index", document=document)
            print(res['result'])
