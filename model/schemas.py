from pydantic import BaseModel


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
