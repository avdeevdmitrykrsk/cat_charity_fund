from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class CharityDonationBase:
    full_amount = Column(Integer, default=1, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
