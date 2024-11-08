import logging
from datetime import datetime
from typing import Union

from app.models import CharityProject, Donation

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=(logging.StreamHandler(),)
)

logger = logging.getLogger(__name__)


class InvestingService:

    @staticmethod
    def __calculate_invest(new_obj, investing_obj):

        new_obj_invested_amount = new_obj.invested_amount
        new_obj_full_amount = new_obj.full_amount

        investing_obj_invested_amount = investing_obj.invested_amount
        investing_obj_full_amount = (
            investing_obj.full_amount
        )

        expected_value = (
            investing_obj_full_amount - investing_obj_invested_amount
        )
        logger.info(f'{new_obj_full_amount} --- {expected_value}')
        if new_obj_full_amount < expected_value:
            logger.info('if')
            investing_obj_invested_amount += new_obj_full_amount
            new_obj_invested_amount = new_obj_full_amount
        elif new_obj_full_amount > expected_value:
            logger.info('elif')
            new_obj_invested_amount += (
                investing_obj_full_amount - investing_obj_invested_amount
            )
            investing_obj_invested_amount = investing_obj_full_amount
        else:
            logger.info('else')
            new_obj_invested_amount = new_obj_full_amount
            investing_obj_invested_amount = investing_obj_full_amount

        logger.info(f'{investing_obj_invested_amount}')
        return (
            new_obj_invested_amount,
            new_obj_full_amount,
            investing_obj_invested_amount,
            investing_obj_full_amount
        )

    def cursed_service(
        self,
        new_obj: Union[CharityProject, Donation],
        investing_objs: Union[CharityProject, Donation],
    ) -> Union[CharityProject, Donation]:
        model = new_obj.__class__
        for investing_obj in investing_objs:
            if new_obj.__class__ == CharityProject:
                new_obj, investing_obj = investing_obj, new_obj
            (
                new_obj_invested_amount,
                new_obj_full_amount,
                investing_obj_invested_amount,
                investing_obj_full_amount
            ) = self.__calculate_invest(new_obj, investing_obj)

            new_obj.invested_amount = new_obj_invested_amount
            investing_obj.invested_amount = investing_obj_invested_amount

            if investing_obj.full_amount == investing_obj.invested_amount:
                setattr(investing_obj, 'fully_invested', True)
                setattr(investing_obj, 'close_date', datetime.now())
            if new_obj.full_amount == new_obj.invested_amount:
                setattr(new_obj, 'fully_invested', True)
                setattr(new_obj, 'close_date', datetime.now())
                break

        if model == CharityProject:
            new_obj, investing_obj = investing_obj, new_obj
        return new_obj, investing_objs
