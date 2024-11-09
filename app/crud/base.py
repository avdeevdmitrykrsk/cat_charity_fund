from datetime import datetime
from typing import Generic, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import CharityProject, Donation
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)  # type: ignore
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

DEFAULT_INVEST_COUNT = 0


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model):
        self.model = model

    async def create(
        self,
        *,
        obj_in,
        user=None,
        session: AsyncSession,
    ):
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        new_obj = self.model(**obj_in_data)

        session.add(new_obj)
        return new_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession
    ):
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
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get(
        self,
        project_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == project_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        *,
        user: User = None,
        session: AsyncSession
    ):
        select_stmt = select(self.model)
        if user:
            select_stmt = select(self.model).where(
                self.model.user_id == user.id
            )
        db_objs = await session.execute(select_stmt)
        return db_objs.scalars().all()

    async def get_investing_objs(
        self,
        model: Union[CharityProject, Donation],
        session: AsyncSession
    ):
        db_objs = await session.execute(
            select(model).where(
                model.fully_invested.is_(False)
            ).order_by(asc(model.id))
        )
        db_objs = db_objs.scalars().all()
        return db_objs
