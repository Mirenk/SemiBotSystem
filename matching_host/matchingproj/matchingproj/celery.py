import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matchingproj.settings')

app = Celery('matchingproj')
app.conf.CELERY_ACKS_LATE = True
app.conf.CELERYD_PREFETCH_MULTIPLIER = 1
app.conf.CELERY_ROUTES = ([
    ('matching.tasks.join_task', {'queue': 'join'}),
    ('matching.tasks.cancel_task', {'queue': 'join'}),
],)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()