from datetime import date

from pydantic import BaseModel


class TextMetadata(BaseModel):
    id: int
    autor: str
    titel: str
    year: int


class Text(BaseModel):
    id: int
    autor: str
    titel: str
    text: str
    year: int

    class Config:
        from_attributes = True


class TextBase(BaseModel):
    autor: str
    titel: str


class TextCreate(TextBase):
    autor: str
    titel: str
    text: str
    year: int


class Author(BaseModel):
    name: str
    birth_place: str

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    birth_place: str


class AuthorCreate(AuthorBase):
    name: str
    birth_place: str


class Extraction(BaseModel):
    text: str
    author: str


class NER_Data(BaseModel):
    id: int
    prompt: str
    author: str
    date: str


class NER_DataBase(BaseModel):
    prompt: str
    author: str
    date: str


class NER_DataCreate(NER_DataBase):
    prompt: str
    author: str
    date: str


class Newsarticle(BaseModel):
    id: int
    titel: str
    datum: date
    newspapername: str
    autor: str
    text: str


class NewsarticleBase(BaseModel):
    titel: str
    datum: date
    newspapername: str
    text: str


class NewsarticleCreate(NewsarticleBase):
    titel: str
    datum: date
    newspapername: str
    autor: str
    text: str
