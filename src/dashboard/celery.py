from celery import Celery
from celery.schedules import crontab
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings.development')
app = Celery('dashboard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'testing_celery_task': {
        'task': 'testing',
        'schedule': crontab(minute='*/1'),
    }
}
