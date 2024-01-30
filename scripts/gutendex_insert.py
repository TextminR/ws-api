import requests
import psycopg2

# Verbindung zur PostgreSQL-Datenbank herstellen
connection = psycopg2.connect(
    host="localhost",
    database="text",
    user="postgres",
    password="postgres"
)
cursor = connection.cursor()
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

        # if text is None:
        # text = book.get("formats").get("text/plain; charset=us-ascii", None)

        if text is None:
            text = book.get("formats").get("text/plain", None)

        if text is not None:
            text = requests.get(text).text

            index_start = text.find("** START")
            index_start = text.find('\n', index_start) + 1
            index_end = text.find("** END")
            text = text[index_start:index_end]
            text = text.strip().replace("\n", " ").replace("\r", " ")

            sql = "INSERT INTO textdata (author, title, text, year, language) VALUES (%s, %s, %s, %s, %s)"
            values = (autorname, titel, text.strip(), year,
                      language)  # Entfernen Sie überflüssige Leerzeichen am Anfang und Ende des Texts
            cursor.execute(sql, values)
            connection.commit()

# while response.json().get("next"):
#
#     response = requests.get(response.json().get("next"), headers={"Accept": "application/json"})
#     gutendex_array = response.json().get("results")
#
#     for book in gutendex_array:
#         autor = book.get("authors")[0].get("name")
#         titel = book.get("title")
#         text = requests.get(book.get("formats").get("text/plain; charset=utf-8")).text
#         sql = "INSERT INTO textdata (autor, titel, text) VA LUES (%s, %s, %s)"
#         values = (autor, titel, text.strip())  # Entfernen Sie überflüssige Leerzeichen am Anfang und Ende des Texts
#         cursor.execute(sql, values)
#         connection.commit()
#
# # Verbindung zur PostgreSQL-Datenbank trennen
cursor.close()
connection.close()
