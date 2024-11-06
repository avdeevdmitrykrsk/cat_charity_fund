from datetime import datetime

from typing import Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.schemas.charityproject import CharityProjectCreate
from app.services import InvestingService


class CharityCRUD(CRUDBase, InvestingService):

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def create(
        self,
        obj_in,
        session: AsyncSession
    ) -> CharityProject:
        obj_in_data = obj_in.dict()
        db_obj = CharityProject(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        obj = await self.investing_service(db_obj, session)
        return obj


charity_crud = CharityCRUD(CharityProject)
