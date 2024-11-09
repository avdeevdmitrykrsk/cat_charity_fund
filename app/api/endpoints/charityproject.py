from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_obj_exist, check_unique_name,
                                validate_before_delete, validate_before_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_crud
from app.models import Donation
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.services import make_investition

router = APIRouter()


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для суперюзеров."""
    db_obj = await check_obj_exist(project_id, session)
    db_obj = await check_unique_name(
        name=obj_in.name, obj=db_obj, session=session
    )
    db_obj = await validate_before_update(db_obj, obj_in)
    db_obj = await charity_crud.update(db_obj, obj_in, session)
    return db_obj


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def make_charity_project(
    obj_in: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Только для суперюзеров."""
    db_obj = await check_unique_name(name=obj_in.name, session=session)
    db_obj = await charity_crud.create(obj_in=obj_in, session=session)

    investing_objs = await charity_crud.get_investing_objs(Donation, session)
    if investing_objs:
        db_objs = make_investition(db_obj, investing_objs)
        session.add_all(db_objs)
    session.add(db_obj)

    await session.commit()
    await session.refresh(db_obj)
    return db_obj


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    db_obj = await check_obj_exist(project_id, session)
    db_obj = await validate_before_delete(db_obj)
    db_obj = await charity_crud.delete(db_obj, session)
    return db_obj


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectDB]:
    db_objs = await charity_crud.get_multi(session=session)
    return db_objs
