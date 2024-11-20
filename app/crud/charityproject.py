from datetime import datetime

from sqlalchemy import and_, between, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityCRUD(CRUDBase):

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(True)
            ).order_by(
                func.extract('year', CharityProject.close_date).desc(),
                func.extract('month', CharityProject.close_date).desc(),
                func.extract('day', CharityProject.close_date).desc(),
                func.extract('hour', CharityProject.close_date).desc(),
                func.extract('minute', CharityProject.close_date).desc(),
                func.extract('second', CharityProject.close_date).desc(),
            )
        )
        return projects.scalars().all()


charity_crud = CharityCRUD(CharityProject)
