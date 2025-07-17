import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'alx_backend_security.settings')

app = Celery('alx_backend_security')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'nuke-logs-every-hour': {
        'task' : 'ip_tracking.tasks.delete_old_logs',
        'schedule': timedelta(seconds=5), # crontab(minute=0, hour='*') # for production
    },
}