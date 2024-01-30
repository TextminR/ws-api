import logging
import os
import json

import requests


def main(start_year: int, end_year: int, languages: str, output_dir: str):
    os.makedirs(output_dir)

    metadata = []
    url = f"https://gutendex.com/books/?author_year_start={start_year}&author_year_end={end_year}&mime_type=text%2Fplain&languages={languages}"
    while True:
        res = requests.get(url)

        if res.status_code != 200:
            logging.error(f"Error while downloading metadata: {res.text}")
            break

        data = res.json()
        for book in data.get("results"):
            raw_text = requests.get(book.get("formats").get("text/plain; charset=us-ascii")).text
                
            if raw_text:
                open(os.path.join(output_dir, f"book_{book.get('id')}.txt"), "w").write(raw_text)

                metadata.append({
                    "id": book.get("id"),
                    "file": f"book_{book.get('id')}.txt",
                    "author": book.get("authors")[0].get("name"),
                    "title": book.get("title"),
                    "year": book.get("authors")[0].get("birth_year"),
                    "language": book.get("languages")[0],
                    "source": "gutenberg"
                })

                logging.info(f"Downloaded book {book.get('id')}")

        if data.get("next") is None:
            break

        url = data.get("next")
    
    json.dump(metadata, open(os.path.join(output_dir, "metadata.json"), "w"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--start-year", help="Minimum year of publication", type=int, default=0
    )
    parser.add_argument(
        "--end-year", help="Maximum year of publication", type=int, default=2024
    )
    parser.add_argument(
        "--languages", help="Languages to download", type=str, default="en,de"
    )
    parser.add_argument("--output", help="Output directory", type=str, default="books")

    args = parser.parse_args()
    main(args.start_year, args.end_year, args.languages, args.output)
