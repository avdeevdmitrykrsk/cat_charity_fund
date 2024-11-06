from datetime import datetime

from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, PositiveInt, Field, validator
from sqlalchemy import select

from app.models import CharityProject


class CharityProjectCreate(BaseModel):

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectDB(BaseModel):
    name: str
    description: str
    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]
