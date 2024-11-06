from datetime import datetime

from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import CharityProject, Donation
from app.models.user import User
from app.schemas.charityproject import CharityProjectCreate
from app.services import InvestingService


class DonationCRUD(InvestingService):

    async def create_transaction(
        self,
        obj_in,
        user: User,
        session: AsyncSession
    ):
        obj_in_data = obj_in.dict()
        db_obj = Donation(user_id=user.id, **obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        obj = await self.investing_service(db_obj, session)
        return obj


donation_crud = DonationCRUD(CharityProject)
