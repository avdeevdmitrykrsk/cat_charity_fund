from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_crud
from app.models import CharityProject


async def check_unique_name(*, name: str, obj=None, session: AsyncSession):
    query = select(CharityProject).where(CharityProject.name == name)
    if obj:
        query = select(CharityProject).where(
            (CharityProject.name == name) & (CharityProject.name != obj.name)
        )
    db_obj = await session.execute(query)
    db_obj = db_obj.scalars().first()

    if db_obj:
        raise HTTPException(
            status_code=400,
            detail='Имя занято.'
        )
    return obj


async def check_obj_exist(
    project_id: int,
    session: AsyncSession
):
    db_obj = await charity_crud.get(session, id=project_id)
    if not db_obj:
        raise HTTPException(
            status_code=422,
            detail=f'Проекта с id={project_id} не существует'
        )
    return db_obj


async def check_fully_invested(db_obj: CharityProject):
    if db_obj.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя изменять/удалять закрытый проект.'
        )
    return db_obj


async def validate_before_update(
    db_obj: CharityProject,
    obj_in: CharityProject
):
    db_obj = await check_fully_invested(db_obj)
    if obj_in.full_amount:
        if obj_in.full_amount < db_obj.invested_amount:
            raise HTTPException(
                status_code=400,
                detail=(
                    'Нелья установить значение '
                    'full_amount меньше уже вложенной суммы.'
                )
            )

    return db_obj


async def validate_before_delete(db_obj: CharityProject):
    db_obj = await check_fully_invested(db_obj)
    if db_obj.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя удалять проект, '
                'в который уже были инвестированы средства.'
            )
        )

    return db_obj
