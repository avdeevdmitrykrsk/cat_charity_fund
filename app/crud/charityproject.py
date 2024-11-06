from datetime import datetime

from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models.charityproject import CharityProject
from app.models.donation import Donation
from app.schemas.charityproject import CharityProjectCreate
from app.services import InvestingService


class CharityCRUD(InvestingService):

    async def create(
        self,
        obj_in,
        session: AsyncSession
    ):
        obj_in_data = obj_in.dict()
        db_obj = CharityProject(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        obj = await self.investing_service(db_obj, session)
        return obj


charity_crud = CharityCRUD(Donation)
