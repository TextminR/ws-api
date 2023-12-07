import uvicorn
from fastapi import FastAPI
import model.msg as msg
from es_client import crud, client

app = FastAPI()
ES = client.get_es_client()


def to_text_list(texts):
    text_list = []
    for text in texts:
        text_list.append(text)
    return text_list


@app.post("/text_metadata", response_model=msg.Response)
async def metadata(id: str = None, minYear: int = None, maxYear: int = None, author: str = None, language: str = None):
    data = crud.get_metadata(client=ES, id=id, minYear=minYear, maxYear=maxYear, author=author, language=language)
    return msg.Response(status="200", message="OK", data=data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
