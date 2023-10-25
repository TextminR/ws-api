from typing import Optional

from pydantic import BaseModel


class Text(BaseModel):
    id: int
    autor: str
    titel: str
    text: str

    class Config:
        from_attributes = True


class TextBase(BaseModel):
    autor: str
    titel: str


class TextCreate(TextBase):
    autor: str
    titel: str
    text: str


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
