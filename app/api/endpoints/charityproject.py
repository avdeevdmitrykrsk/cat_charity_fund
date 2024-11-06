from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_unique_name, check_obj
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_crud
from app.models.charity_project import CharityProject
from app.schemas.charityproject import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)

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
):
    db_obj = await check_obj(
        project_id=project_id, obj_in=obj_in, session=session
    )
    db_obj = await check_unique_name(obj_in.name, session)
    db_obj = await charity_crud.update(db_obj, obj_in, session)
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
    db_obj = await check_obj(project_id=project_id, session=session)
    db_obj = await charity_crud.delete(db_obj, session)
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
    db_obj = await check_unique_name(obj_in.name, session)
    db_obj = await charity_crud.create(obj_in, session)
    return db_obj


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectDB]:
    db_objs = await charity_crud.get_multi(session)
    return db_objs
