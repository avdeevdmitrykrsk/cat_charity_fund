from sqlalchemy import Column, String, Text

from . import CharityDonationBase
from app.core.db import Base


class CharityProject(Base, CharityDonationBase):

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
