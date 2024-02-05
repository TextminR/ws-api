import logging
import os
import json
from elasticsearch import Elasticsearch
import torch
from transformers import AutoModel, AutoTokenizer

ES_HOST = "https://es.textminr.tech:9200"
ES_USER = "elastic"
ES_PASSWORD = "A_2LfPT*rVitjUvp0vwX"

def main(input_dir: str, model_id: str, device_name: str, limit = 2048):
    es = Elasticsearch([ES_HOST], basic_auth=(ES_USER, ES_PASSWORD), verify_certs=False)
    metadata = json.load(open(os.path.join(input_dir, "metadata.json")))

    device = torch.device(device_name)
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    for book in metadata:
        text = open(os.path.join(input_dir, book["file"])).read()
        index_start = text.find("** START")
        index_start = text.find("\n", index_start) + 1
        index_end = text.find("** END")
        text = text[index_start:index_end]
        
        batch_dict = tokenizer(text, return_tensors="pt")
        tokens = batch_dict["input_ids"].squeeze()
        token_parts = [tokens[i : i + limit] for i in range(0, len(tokens), limit)]
        parts = []

        for part in token_parts:
            # if part.size(dim=0) > 2500:
                # text_part = [tokenizer.decode(part)]
                # decoded_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(text_part))
            parts.append(tokenizer.decode(part))
        
        if parts:
            embeddings = []
            text_parts = []

            for part in parts:
                embeddings.append({"vector": model.encode(part, show_progress_bar=False)})
                text_parts.append({"part": part})

            document = {
                "author": book["author"],
                "title": book["title"],
                "year": book["year"],
                "language": book["language"],
                "source": book["source"],
                "text_parts": text_parts,
                "embeddings": embeddings,
            }

            es.index(index="texts", body=document)
            logging.info(f"Indexed book {book['id']}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("input_dir", type=str)
    parser.add_argument(
        "--model", type=str, default="jinaai/jina-embeddings-v2-base-de"
    )
    parser.add_argument("--device", type=str, default="cpu")

    args = parser.parse_args()
    main(args.input_dir, args.model, args.device)
