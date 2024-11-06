from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def check_unique_name(name: str, session: AsyncSession):
    db_obj = await session.execute(
        select(CharityProject).where(CharityProject.name == name)
    )
    db_obj = db_obj.scalars().first()
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail='Имя занято.'
        )
    return db_obj


async def check_obj(
    *,
    project_id: int,
    obj_in: Optional[CharityProject] = None,
    session: AsyncSession
):
    db_obj = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    db_obj = db_obj.scalars().first()

    if not db_obj:
        raise HTTPException(
            status_code=422,
            detail=f'Проекта с id={project_id} не существует'
        )

    if db_obj.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя изменять/удалять закрытый проект.'
        )

    if obj_in:
        if obj_in.full_amount < db_obj.invested_amount:
            raise HTTPException(
                status_code=400,
                detail=(
                    'Нелья установить значение '
                    'full_amount меньше уже вложенной суммы.'
                )
            )
        return db_obj


    if db_obj.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя удалять проект, '
                'в который уже были инвестированы средства.'
            )
        )

    return db_obj
