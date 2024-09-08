from sqlalchemy import event, insert

from data.region import Region
import settings
from data.headquarter import Headquarter
from data.user import User


@event.listens_for(User, 'after_insert')
def add_first_hq(mapper, connection, target):
    hq_table = Headquarter.__table__
    region_table = Region.__table__
    region = connection.execute(
        region_table.select()
    ).first()
    if not region:
        region = connection.execute(
            region_table.insert().values(
                name='Поселок',
                description='Поселок в дали от города'
            ).returning(region_table.c.id)
        ).first()
    connection.execute(
        hq_table.insert().values(
            director_id=target.id,
            name='First headquarter',
            recruitment_process=settings.
            RECRUITMENT_PROCESS_TO_NEW_UNIT * settings.
            AMOUNT_UNIT_TO_START,
            region_id=region.id))
