from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Block and IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to be blocked')
    
    def handle(self, *args, **kwargs):
        ip = kwargs['ip_address']
        obj, created = BlockedIP.objects.get_or_create(ip_address = ip)
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully blocked ip {ip}"))
        else:
            self.stdout.write(self.style.WARNING(f"IP already blocked. {ip}"))