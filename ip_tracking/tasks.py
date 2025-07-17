from celery import shared_task
from django.utils import timezone
from .models import RequestLog

@shared_task
def delete_old_logs():
    cutoff = timezone.now() - timezone.timedelta(hours=24)
    deleted, _ = RequestLog.objects.filter(timestamp_lt=cutoff).delete()
    return f"{deleted} logs nukes"