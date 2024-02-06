from celery import shared_task
from celery.schedules import crontab

from django.utils import timezone

from celery_app import app
from posts import models


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=25),
        delete_expired_reports.s(),
        name='delete_expired_reports'
    )


@shared_task
def delete_expired_reports():
    """Delete all reports where the expire
    time is less than the current one."""
    now = timezone.now()
    expired_posts = models.Report.objects.filter(expire_time__lt=now)
    expired_posts.delete()
