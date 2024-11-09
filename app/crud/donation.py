from app.crud.base import CRUDBase
from app.models import Donation


class DonationCRUD(CRUDBase):
    pass


donation_crud = DonationCRUD(Donation)
