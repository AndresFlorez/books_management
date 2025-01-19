from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class Book(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id", serialization_alias="id")
    title: str
    author: str
    published_date: datetime
    genre: str
    description: str
    price: float

    @field_validator('price')
    def price_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('Price must be non-negative')
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
