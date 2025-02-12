from datetime import datetime


def make_investition(target, sources):
    changed_sources = []

    for source in sources:

        #  Затычка для тестов.
        if not getattr(target, 'invested_amount'):
            target.invested_amount = 0

        target_available = target.full_amount - target.invested_amount
        source_available = source.full_amount - source.invested_amount

        accepted_value = min(target_available, source_available)
        if not accepted_value:
            break

        for obj in (target, source):
            obj.invested_amount += accepted_value
            if obj.invested_amount == obj.full_amount:
                setattr(obj, 'fully_invested', True)
                setattr(obj, 'close_date', datetime.now())

        changed_sources.append(source)

    return changed_sources
