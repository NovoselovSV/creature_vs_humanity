from typing import Any

from redis_app import redis_instance

import settings


def create_group_task(group_id: int, task: Any, *args: Any) -> None:
    create_base_task(
        settings.REDIS_GROUP_KEY.format(group_id=group_id),
        task,
        args,
        settings.REDIS_GROUP_MISSION_SECOND)


def create_hq_task(hq_id: int, task: Any, *args: Any) -> None:
    create_base_task(
        settings.REDIS_HQ_KEY.format(hq_id=hq_id),
        task,
        args,
        settings.REDIS_HQ_WORKING_SECOND)


def create_base_task(key: str, task: Any, args: tuple[Any], time_seconds: int):
    redis_instance.set(key, task.apply_async(
        args,
        {'key': key},
        countdown=time_seconds).id,
        ex=time_seconds * settings.MULT_TASK_TIME)
