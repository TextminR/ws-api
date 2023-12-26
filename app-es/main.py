import uvicorn
from fastapi import FastAPI
import model.msg as msg
from model import crud, client

app = FastAPI()
ES = client.get_es_client()


@app.get("/text_metadata", response_model=msg.Response)
async def text_metadata(id: str = None, title: str = None, minYear: int = None, maxYear: int = None, author: str = None,
                        language: str = None):
    data = await crud.get_texts(client=ES, id=id, title=title, minYear=minYear, maxYear=maxYear, author=author,
                                language=language, include_text=False)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/texts", response_model=msg.Response)
async def texts(id: str = None, title: str = None, minYear: int = None, maxYear: int = None, author: str = None,
                language: str = None):
    data = await crud.get_texts(client=ES, id=id, title=title, minYear=minYear, maxYear=maxYear, author=author,
                                language=language, include_text=True)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/authors", response_model=msg.Response)
async def authors(id: str = None, name: str = None, birth_place: str = None, country: str = None):
    data = await crud.get_authors(client=ES, id=id, name=name, birth_place=birth_place, country=country)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/newsarticles", response_model=msg.Response)
async def newsarticles(id: str = None, title: str = None, minDate: str = None, maxDate: str = None, source: str = None,
                       author: str = None, language: str = None):
    data = await crud.get_newsarticles(client=ES, id=id, title=title, minDate=minDate, maxDate=maxDate, source=source,
                                       author=author, language=language, include_text=True)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/newsarticle_metadata", response_model=msg.Response)
async def newsarticle_metadata(id: str = None, title: str = None, minDate: str = None, maxDate: str = None,
                               source: str = None,
                               author: str = None, language: str = None):
    data = await crud.get_newsarticles(client=ES, id=id, title=title, minDate=minDate, maxDate=maxDate, source=source,
                                       author=author, language=language, include_text=False)
    return msg.Response(status="200", message="OK", data=data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
