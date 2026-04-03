from django.core.management.base import BaseCommand
from apps.products.tasks import sync_product_views

class Command(BaseCommand):
    help = "Sync product views from Redis to Database"

    def handle(self, *args, **kwargs):
        sync_product_views()
        self.stdout.write(self.style.SUCCESS("Successfully synced product views"))
    