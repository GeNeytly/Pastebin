import os
from datetime import timedelta

from django.conf import settings
from celery import Celery
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.beat_schedule = {
    'delete_expired_reports': {
        'task': 'api.tasks.delete_expired_reports',
        'schedule': timedelta(days=1)
    },
}
app.conf.timezone = settings.CELERY_TIMEZONE
app.autodiscover_tasks()


@app.task()
def debug_task():
    print(timezone.now())
