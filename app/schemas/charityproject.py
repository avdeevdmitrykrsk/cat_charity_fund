from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectCreate(BaseModel):

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int
    invested_amount: int = Field(default=0)


class CharityProjectDB(BaseModel):
    id: int

    class Config:
        orm_mode = True
