import os
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status

import model.msg as msg
from model import crud, client, extract_ner

ES = client.get_es_client()
app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")
api_key = os.getenv("API_KEY")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == api_key:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@app.get("/texts", response_model=msg.Response)
async def texts(api_key: str = Security(get_api_key), id: Annotated[list, Query()] = None,
                title: Annotated[list, Query()] = None, minYear: int = None,
                maxYear: int = None,
                author: Annotated[list, Query()] = None,
                language: str = None, sampled: bool = False):
    data = await crud.get_texts(client=ES, id=id, title=title, minYear=minYear, maxYear=maxYear, author=author,
                                language=language, only_text=True, only_embeddings=False, include_text=False,
                                include_embeddings=False, sampled=sampled)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/texts/metadata", response_model=msg.Response)
async def text_metadata(api_key: str = Security(get_api_key), id: Annotated[list, Query()] = None,
                        title: Annotated[list, Query()] = None,
                        minYear: int = None, maxYear: int = None,
                        author: Annotated[list, Query()] = None,
                        language: str = None):
    data = await crud.get_texts(client=ES, id=id, title=title, minYear=minYear, maxYear=maxYear, author=author,
                                language=language, only_text=False, only_embeddings=False, include_text=False,
                                include_embeddings=False, sampled=False)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/texts/metadata_with_texts", response_model=msg.Response)
async def text_metadata_with_texts(api_key: str = Security(get_api_key), id: Annotated[list, Query()] = None,
                                   title: Annotated[list, Query()] = None,
                                   minYear: int = None, maxYear: int = None,
                                   author: Annotated[list, Query()] = None,
                                   language: str = None, sampled: bool = False):
    data = await crud.get_texts(client=ES, id=id, title=title, minYear=minYear, maxYear=maxYear, author=author,
                                language=language, only_text=False, only_embeddings=False, include_text=True,
                                include_embeddings=False, sampled=sampled)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/texts/metadata_with_embeddings", response_model=msg.Response)
async def text_metadata_with_texts(api_key: str = Security(get_api_key), id: Annotated[list, Query()] = None,
                                   title: Annotated[list, Query()] = None,
                                   minYear: int = None, maxYear: int = None,
                                   author: Annotated[list, Query()] = None,
                                   language: str = None):
    data = await crud.get_texts(client=ES, id=id, title=title, minYear=minYear, maxYear=maxYear, author=author,
                                language=language, only_text=False, only_embeddings=False, include_text=False,
                                include_embeddings=True)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/texts/embeddings", response_model=msg.Response)
async def text_metadata(api_key: str = Security(get_api_key), id: Annotated[list, Query()] = None,
                        title: Annotated[list, Query()] = None,
                        minYear: int = None, maxYear: int = None,
                        author: Annotated[list, Query()] = None,
                        language: str = None):
    data = await crud.get_texts(client=ES, id=id, title=title, minYear=minYear, maxYear=maxYear, author=author,
                                language=language, only_text=False, only_embeddings=True, include_text=False,
                                include_embeddings=False)
    return msg.Response(status="200", message="OK", data=data)


@app.post("/extract_data", response_model=msg.Response)
async def extract_data(api_key: str = Security(get_api_key), texts: list[str] = None):
    if texts is not None:
        data = await extract_ner.extraction(texts)
        return msg.Response(status="200", message="OK", data=data)
    return msg.Response(status="400", message="NO DATA", data="")


@app.get("/authors", response_model=msg.Response)
async def authors(api_key: str = Security(get_api_key), id: str = None, name: str = None, birth_place: str = None,
                  country: str = None):
    data = await crud.get_authors(client=ES, id=id, name=name, birth_place=birth_place, country=country)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/newsarticles", response_model=msg.Response)
async def newsarticles(api_key: str = Security(get_api_key), id: str = None, title: str = None, minDate: str = None,
                       maxDate: str = None, source: str = None,
                       author: str = None, language: str = None):
    data = await crud.get_newsarticles(client=ES, id=id, title=title, minDate=minDate, maxDate=maxDate, source=source,
                                       author=author, language=language, include_text=True)
    return msg.Response(status="200", message="OK", data=data)


@app.get("/newsarticles/metadata", response_model=msg.Response)
async def newsarticle_metadata(api_key: str = Security(get_api_key), id: str = None, title: str = None,
                               minDate: str = None, maxDate: str = None,
                               source: str = None,
                               author: str = None, language: str = None):
    data = await crud.get_newsarticles(client=ES, id=id, title=title, minDate=minDate, maxDate=maxDate, source=source,
                                       author=author, language=language, include_text=False)
    return msg.Response(status="200", message="OK", data=data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
