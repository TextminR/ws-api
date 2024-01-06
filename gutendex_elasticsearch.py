import requests
from elasticsearch import Elasticsearch
from transformers import AutoModel, AutoTokenizer, BertTokenizerFast
import transformers as tf
import numpy as np

response = requests.get("https://gutendex.com/books/?page=1", headers={"Accept": "application/json"})
gutendex_array = response.json().get("results")
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True)
tokenizer = BertTokenizerFast.from_pretrained("jinaai/jina-embeddings-v2-small-en")


def split_string_with_limit(text: str, limit: int):

    tokens = tokenizer(text).data['input_ids']
    token_parts = [tokens[i:i + limit] for i in range(0, len(tokens), limit)]
    text_parts = []

    for part in token_parts:
        text_part = [tokenizer.decode(token) for token in part]
        decoded_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(text_part))
        text_parts.append(decoded_text)
    i = 1
    return text_parts


es = Elasticsearch(
    ['https://localhost:9200'],
    basic_auth=("elastic", "GZLhtJXfckU-DcYQLgYU"),
    verify_certs=False
)
print(es.info())
i = 1

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

            parts = split_string_with_limit(text, 8150)
            embeddings = []

            for part in parts:
                embedding = (model.encode([part]))

                if embedding.shape[1] != 512:
                    resize_layer = tf.keras.layers.Dense(512, input_shape=(embedding.shape[1],))
                    embedding = resize_layer(embedding)

                embeddings.append(embedding)

            doc_embeddings = []
            for emb in embeddings:
                doc_embeddings.append({"vector": emb[0]})

            document = {
                "author": autorname,
                "title": titel,
                "year": year,
                "language": language,
                "source": "gutenberg",
                "text": text,
                "embeddings": doc_embeddings
            }

            res = es.index(index="texts", document=document)
            print(f"Dokument {titel} Nummer {i} erstellt.")
    i += 1
