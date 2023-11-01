from pydantic import BeforeValidator, BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from typing import Optional, List

PyObjectId = Annotated[str, BeforeValidator(str)]


class TextModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    autor: str = Field(...)
    text: str = Field(...)
    titel: str = Field(...)
    year: Optional[float] = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "autor": "Yusuf Akalin",
                "titel": "Mein Text",
                "text": "Ich bin der Yusuf.",
                "year": 2023
            }
        },
    )


class TextCollection(BaseModel):
    texts: List[TextModel]
