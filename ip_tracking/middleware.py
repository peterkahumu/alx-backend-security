from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from django.utils.timezone import now
from django.core.cache import cache
import os

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        ip = self.get_client_ip(request)

        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP is blocked.")

        # Log request
        RequestLog.objects.create(ip_address=ip, timestamp=now(), path=request.path)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

