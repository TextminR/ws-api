import requests
from json import dumps
from hdfs import Client
from pywebhdfs.webhdfs import PyWebHdfsClient

client = PyWebHdfsClient(host="localhost", port="9870")
print("connected")

response = requests.get("https://gutendex.com/books/?page=1", headers={"Accept": "application/json"})
gutendex_array = response.json().get("results")

i = 1

for book in gutendex_array:
    autor = ""
    if len(book.get("authors")) == 0:
        autorname = "unknown"
    else:
        autor = book.get("authors")[0]
        autorname = autor.get("name")

    titel = book.get("title")
    text = book.get("formats").get("text/plain; charset=utf-8", None)

    if text is None:
        text = book.get("formats").get("text/plain", None)

    if text is None:
        text = book.get("formats").get("text/plain; charset=us-ascii", None)

    text = requests.get(text).text

    year = (autor.get("birth_year") + autor.get("death_year")) / 2

    index_start = text.find("** START")
    index_start = text.find('\n', index_start) + 1
    index_end = text.find("** END")
    text = text[index_start:index_end]

    data = {
        'id': i,
        'author': autor,
        'title': titel,
        'text': text,
        'year': year
    }

    client.create_file(f'user/root/gutendata/{i}.json', file_data=dumps(data))

    i = i + 1
