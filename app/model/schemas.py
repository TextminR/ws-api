from datetime import date

from pydantic import BaseModel


class TextMetadata(BaseModel):
    id: int
    author: str
    title: str
    year: int
    language: str


class Text(BaseModel):
    id: int
    author: str
    title: str
    text: str
    year: int
    language: str

    class Config:
        from_attributes = True


class TextBase(BaseModel):
    author: str
    title: str


class TextCreate(TextBase):
    author: str
    title: str
    text: str
    year: int
    language: str


class AuthorMetadata(BaseModel):
    birth_place: str
    coordinatex: str
    coordinatey: str


class Author(BaseModel):
    name: str
    birth_place: str
    coordinatex: str
    coordinatey: str

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: str
    birth_place: str
    coordinatex: str
    coordinatey: str


class AuthorCreate(AuthorBase):
    name: str
    birth_place: str
    coordinatex: str
    coordinatey: str


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
    title: str
    datum: date
    newspapername: str
    author: str
    text: str
    language: str


class NewsarticleBase(BaseModel):
    title: str
    datum: date
    newspapername: str
    text: str
    language: str


class NewsarticleCreate(NewsarticleBase):
    title: str
    datum: date
    newspapername: str
    author: str
    text: str
    language: str
