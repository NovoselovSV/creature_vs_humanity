from typing import Any, Dict

from . import celery_acts as acts
from .shortcuts import loop
from SQL_db.database import SQLALCHEMY_DATABASE_URL, get_db
from celery_app import celery_app


@celery_app.task
@acts.deleting_key
def get_experience_celery(group_id: int):
    loop.run_until_complete(acts.get_experience_act(group_id))


@celery_app.task
@acts.deleting_key
def create_hq_celery(hq_data: Dict[str, Any],
                     director_id: int,
                     group_id: int):
    loop.run_until_complete(acts.create_hq_act(hq_data, director_id, group_id))


@celery_app.task
@acts.deleting_key
def create_unit_celery(unit_data: Dict[str, Any],
                       director_id: int):
    loop.run_until_complete(acts.create_unit_act(unit_data, director_id))


@celery_app.task
@acts.deleting_key
def increase_recruitment_celery(headquarter_id: int,
                                amount_units: int):
    loop.run_until_complete(
        acts.increase_recruitment_act(
            headquarter_id,
            amount_units))
