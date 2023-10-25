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

    if(len(book.get("authors")) == 0):
        autorname = "unknown"
    else:
        autor = book.get("authors")[0]
        autorname = autor.get("name")


    titel = book.get("title")
    text = book.get("formats").get("text/plain; charset=utf-8", None)

    if text is None:
        text = book.get("formats").get("text/plain; charset=us-ascii", None)
    text = requests.get(text).text

    year = (autor.get("birth_year") + autor.get("death_year"))/2

    index_start = text.find("** START")
    index_start = text.find('\n', index_start) + 1
    index_end = text.find("** END")
    text = text[index_start:index_end]

    sql = "INSERT INTO textdata (autor, titel, text, year) VALUES (%s, %s, %s, %s)"
    values = (autorname, titel, text.strip(), year)  # Entfernen Sie überflüssige Leerzeichen am Anfang und Ende des Texts
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