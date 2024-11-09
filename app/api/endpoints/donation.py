from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import (DonationCreate, DonationCreateDB, DonationDB,
                                  UserDonationDB)
from app.services import make_investition

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
    db_objs = await donation_crud.get_multi(
        user=user, session=session
    )
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
    db_objs = await donation_crud.get_multi(session=session)
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
    investing_objs = await donation_crud.get_investing_objs(
        CharityProject, session
    )
    if investing_objs:
        db_objs = make_investition(db_obj, investing_objs)
        session.add_all(db_objs)

    await session.commit()
    await session.refresh(db_obj)
    return db_obj
