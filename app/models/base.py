from datetime import datetime

from sqlalchemy import Boolean, Column, CheckConstraint, DateTime, Integer


class CharityDonationMixin:
    full_amount = Column(Integer, default=1, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            'invested_amount >= 0', name='check1_invested_amount'
        ),
        CheckConstraint(
            'invested_amount <= full_amount', name='check2_invested_amount'
        )
    )
