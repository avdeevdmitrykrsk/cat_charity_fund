from typing import Generic, Optional, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import CharityProject, Donation
from app.services import InvestingService

ModelType = TypeVar('ModelType', bound=Base)  # type: ignore
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
    InvestingService
):

    def __init__(self, model):
        self.model = model

    async def get_investing_obj(
        self,
        model: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> Optional[Union[list[CharityProject], list[Donation]]]:
        swap_models = {
            Donation: CharityProject,
            CharityProject: Donation
        }
        model = swap_models[model]
        db_obj = await session.execute(
            select(model).where(
                model.fully_invested.is_(False)
            ).order_by(asc(model.id))
        )
        db_obj = db_obj.scalars().all()
        return db_obj

    async def make_transactions(
        self,
        new_obj: Union[CharityProject, Donation],
        session: AsyncSession
    ):
        investing_objs = await self.get_investing_obj(
            new_obj.__class__, session
        )
        if investing_objs:
            for obj in investing_objs:
                session.add(obj)
            session.add(new_obj)
            new_obj, investing_objs = self.cursed_service(
                new_obj=new_obj,
                investing_objs=investing_objs,
            )
            await session.commit()
            await session.refresh(new_obj)
        return new_obj

    async def get_multi(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()
