import os

from celery import Celery
from celery.schedules import crontab
# from room import tasks
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-week': {
        'task': 'tasks.league_prize',
        'schedule': crontab(day_of_week='friday',minute=0,hour=0),
        # 
    },
    'add-every-day': {
        'task': 'tasks.daily_prize',
        'schedule': crontab(minute=0, hour=0),
        # 
    },
}
