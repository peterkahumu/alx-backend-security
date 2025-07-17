from celery import shared_task
from django.utils import timezone
from .models import RequestLog, SuspiciousIP
from datetime import timedelta
from django.db import models

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_suspicious_ips():
    now = timezone.now()
    one_hour_ago = now - timedelta(hours=1)


    # IP's with more than 100 requests in the last hour.
    heavy_hitters = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=models.Count('id'))
        .filter(count__gte=100)
    )

    for entry in heavy_hitters:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_addresss'],
            defaults={'reason': "Excessive requests in one hour"}
        )

    for path in SENSITIVE_PATHS:
        logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago,path__icontains= path)

        for log in logs:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                defaults={'reason': f'Accessed sensitive path: {log.path}'}
            )

@shared_task
def delete_old_logs():
    cutoff = timezone.now() - timezone.timedelta(hours=24)
    deleted, _ = RequestLog.objects.filter(timestamp_lt=cutoff).delete()
    return f"{deleted} logs nukes"