from celery.app import Celery

from settings import redis_url

celery_app = Celery(
    __name__,
    broker=redis_url,
    backend=redis_url,
    include=('service.tasks',))
