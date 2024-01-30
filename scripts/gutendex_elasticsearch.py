import requests
from elasticsearch import Elasticsearch
from transformers import AutoModel, AutoTokenizer
import torch
import warnings

warnings.filterwarnings("ignore")

response = requests.get("https://gutendex.com/books/?page=1&author_year_start=1800", headers={"Accept": "application/json"})
gutendex_array = response.json().get("results")
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True, torch_dtype=torch.float16).cuda()
tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v2-small-en", use_fast=True)


def split_string_with_limit(text: str, limit: int):

    batch_dict = tokenizer(text, return_tensors='pt')
    tokens = batch_dict['input_ids'].squeeze()
    token_parts = [tokens[i:i + limit] for i in range(0, len(tokens), limit)]
    text_parts = []

    for part in token_parts:
        if part.size(dim=0) > 2500:
          text_part = [tokenizer.decode(token) for token in part]
          decoded_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(text_part))
          text_parts.append(decoded_text)
    return text_parts


es = Elasticsearch(
    ['https://es.textminr.tech:9200'],
    basic_auth=("elastic", "A_2LfPT*rVitjUvp0vwX"),
    verify_certs=False
)
print(es.info())
i = 1

max_pages = 10
page = 0

while response.json().get("next") and page < max_pages:
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
              if parts:
                  embeddings = []
                  text_parts = []
                  
                  for part in parts:
                      embeddings.append(model.encode(part))
                      text_parts.append({"part": part})

                  doc_embeddings = []
                  for emb in embeddings:
                      doc_embeddings.append({"vector": emb})

                  document = {
                      "author": autorname,
                      "title": titel,
                      "year": year,
                      "language": language,
                      "source": "gutenberg",
                      "text": text_parts,
                      "embeddings": doc_embeddings
                  }

                  res = es.index(index="texts", document=document)
                  print(f"Dokument `{titel}` Nummer {i} erstellt.")
      i += 1

  response = requests.get(response.json().get("next"), headers={"Accept": "application/json"})
  gutendex_array = response.json().get("results")
  
  page += 1