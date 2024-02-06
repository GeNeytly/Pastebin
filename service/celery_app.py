import os
import time

from django.conf import settings
from django.utils import timezone
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.timezone = settings.CELERY_TIMEZONE
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(5)
    print('Hello from debug task!')
    print(timezone.now())
