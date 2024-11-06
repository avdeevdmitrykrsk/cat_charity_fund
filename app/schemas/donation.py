from datetime import datetime

from typing import Optional

from pydantic import BaseModel, PositiveInt, Field, validator


class DonationCreate(BaseModel):

    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(BaseModel):

    full_amount: int
    comment: Optional[str]
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationCreateDB(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class UserDonationDB(DonationCreateDB):
    pass
