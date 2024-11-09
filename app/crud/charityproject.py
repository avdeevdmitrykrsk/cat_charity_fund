from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityCRUD(CRUDBase):
    pass


charity_crud = CharityCRUD(CharityProject)
