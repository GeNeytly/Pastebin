from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task
from celery import Celery
from celery.schedules import crontab

from posts import models

from celery.schedules import crontab

from celery_app import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=3, minute=0),
        delete_expired_reports(),
    )


@shared_task
def delete_expired_reports():
    """Delete all reports where the expire
    time is less than the current one"""
    now = timezone.now()
    expired_posts = models.Post.objects.filter(expire_time__lt=now)
    expired_posts.delete()


@shared_task
def debug_task():
    """Delete all reports where the expire
    time is less than the current one"""
    now = timezone.now()
    print(now)



