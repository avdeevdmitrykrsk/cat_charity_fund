from datetime import datetime
from typing import Optional, Union

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation
from app.models import CharityProject


class InvestingService:

    @staticmethod
    async def __calculate_invest(obj_in, db_obj):
        if obj_in.__class__ == CharityProject:
            obj_in, db_obj = db_obj, obj_in

        obj_in_invest_amount = obj_in.invested_amount
        obj_in_full_amount = obj_in.full_amount - obj_in_invest_amount

        db_obj_invest_amount = db_obj.invested_amount
        db_obj_full_amount = db_obj.full_amount - db_obj_invest_amount

        if db_obj_full_amount > obj_in_full_amount:
            db_obj_invest_amount += obj_in_full_amount
            obj_in_invest_amount += obj_in_full_amount
        elif db_obj_full_amount <= obj_in_full_amount:
            profit = db_obj_full_amount - db_obj_invest_amount
            db_obj_invest_amount += profit
            obj_in_invest_amount += profit

        return (
            obj_in_invest_amount,
            obj_in_full_amount,
            db_obj_invest_amount,
            db_obj_full_amount
        )

    @staticmethod
    async def __get_investing_obj(
        model: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> Optional[Union[CharityProject, Donation]]:
        db_obj = await session.execute(
            select(model).where(
                model.fully_invested.is_(False)
            ).order_by(asc(model.id))
        )
        db_obj = db_obj.scalars().first()
        return db_obj

    @staticmethod
    async def __get_invest_model(obj_in: Union[CharityProject, Donation]):
        SWAP_MODELS = {
            Donation: CharityProject,
            CharityProject: Donation
        }
        return SWAP_MODELS[obj_in.__class__]

    async def investing_service(
        self,
        obj_in: Union[CharityProject, Donation],
        session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        model = await self.__get_invest_model(obj_in)

        while True:
            db_obj = await self.__get_investing_obj(model, session)
            if db_obj:
                (
                    obj_in_invest_amount, obj_in_full_amount,
                    db_obj_invest_amount, db_obj_full_amount
                ) = await self.__calculate_invest(obj_in, db_obj)

                setattr(obj_in, 'invested_amount', obj_in_invest_amount)
                setattr(db_obj, 'invested_amount', db_obj_invest_amount)
                if db_obj.full_amount == db_obj.invested_amount:
                    setattr(db_obj, 'fully_invested', True)
                    setattr(db_obj, 'close_date', datetime.now())
                    session.add(db_obj)
            break

        if obj_in.full_amount == obj_in.invested_amount:
            setattr(obj_in, 'fully_invested', True)
            setattr(db_obj, 'close_date', datetime.now())
            session.add(obj_in)
        await session.commit()
        await session.refresh(obj_in)
        return obj_in
