from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.services import InvestingService


class CharityCRUD(CRUDBase, InvestingService):

    async def get(
        self,
        project_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(CharityProject).where(CharityProject.id == project_id)
        )
        return db_obj.scalars().first()

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession
    ) -> CharityProject:
        obj_in_data = obj_in.dict(exclude_unset=True)
        db_obj_data = jsonable_encoder(db_obj)

        if obj_in_data.get('full_amount'):
            if obj_in_data['full_amount'] == db_obj_data['invested_amount']:
                setattr(db_obj, 'fully_invested', True)
                setattr(db_obj, 'close_date', datetime.now())
        for field in obj_in_data:
            if field in db_obj_data:
                setattr(db_obj, field, obj_in_data[field])

        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db_obj,
            session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def create(
        self,
        obj_in,
        session: AsyncSession,
    ) -> CharityProject:
        obj_in_data = obj_in.dict()
        new_obj = CharityProject(**obj_in_data)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj


charity_crud = CharityCRUD(CharityProject)
