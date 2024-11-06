from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
)
async def make_donation(
    obj_in: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> DonationDB:
    donation = await donation_crud.create_transaction(
        obj_in=obj_in, user=user, session=session
    )
    return donation
