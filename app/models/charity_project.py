from sqlalchemy import Column, String, Text

from .base import CharityDonationMixin
from app.core.db import Base


class CharityProject(CharityDonationMixin, Base):

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
