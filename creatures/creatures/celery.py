import os

from celery import Celery

_settings_module = 'creatures.settings'
if 'PYTEST_CURRENT_TEST' in os.environ:
    _settings_module = 'creatures.settings_to_tests'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', _settings_module)
app = Celery('api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.task_routes = {'beast.tasks.*': {'queue': 'creatures'},
                        'nest.tasks.*': {'queue': 'creatures'}}
