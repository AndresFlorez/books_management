from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Book(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id", serialization_alias="id")
    title: str
    author: str
    published_date: datetime
    genre: str
    description: str
    price: float

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
