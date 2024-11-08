from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (DonationCreate, DonationCreateDB, DonationDB,
                                  UserDonationDB)

router = APIRouter()


@router.get(
    '/my',
    response_model=list[UserDonationDB],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    db_objs = await donation_crud.get_donations(user, session)
    return db_objs


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    db_objs = await donation_crud.get_multi(session)
    return db_objs


@router.post(
    '/',
    response_model=DonationCreateDB,
)
async def make_donation(
    obj_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> DonationDB:
    db_obj = await donation_crud.create(
        obj_in=obj_in, user=user, session=session
    )
    db_obj = await donation_crud.make_transactions(db_obj, session)
    return db_obj
