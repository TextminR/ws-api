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

