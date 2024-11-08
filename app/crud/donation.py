from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.models.user import User


class DonationCRUD(CRUDBase):

    async def get_donations(
        self,
        user: User,
        session: AsyncSession
    ) -> list[Donation]:
        db_objs = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        db_objs = db_objs.scalars().all()
        return db_objs

    async def create(
        self,
        obj_in,
        user: User,
        session: AsyncSession
    ) -> Donation:
        obj_in_data = obj_in.dict()
        new_obj = Donation(user_id=user.id, **obj_in_data)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj


donation_crud = DonationCRUD(Donation)
