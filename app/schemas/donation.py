from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationCreate(BaseModel):

    full_amount: int
    comment: str


class DonationDB(BaseModel):

    id: int
    comment: str
    full_amount: int
    create_date: datetime

    class Config:
        orm_mode = True
