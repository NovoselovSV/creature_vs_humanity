from celery.app import Celery

from settings import CELERY_TASK_EXPIRE_SEC, redis_url

celery_app = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url,
    include=('service.tasks',))

celery_app.conf.result_expires = CELERY_TASK_EXPIRE_SEC
