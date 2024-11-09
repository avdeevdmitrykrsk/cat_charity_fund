from sqlalchemy import Column, ForeignKey, Integer, Text

from . import CharityDonationBase
from app.core.db import Base


class Donation(Base, CharityDonationBase):

    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)
