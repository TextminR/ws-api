from typing import Any
from pydantic import BaseModel


class Response(BaseModel):
    status: str
    message: str
    data: Any
