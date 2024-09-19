import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creatures.settings')
app = Celery('api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_routes = {'beast.tasks.*': {'queue': 'creatures'},
                        'nest.tasks.*': {'queue': 'creatures'}}
