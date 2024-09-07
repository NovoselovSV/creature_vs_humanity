from sqlalchemy import event, insert

import settings
from data.headquarter import Headquarter
from data.user import User


@event.listens_for(User, 'after_insert')
def add_first_hq(mapper, connection, target):
    hq_table = Headquarter.__table__
    connection.execute(
        hq_table.insert().values(
            director_id=target.id,
            name='First headquarter',
            recruitment_process=settings.
            RECRUITMENT_PROCESS_TO_NEW_UNIT * settings.
            AMOUNT_UNIT_TO_START,
            region_id=1))
