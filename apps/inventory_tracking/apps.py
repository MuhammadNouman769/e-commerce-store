from django.apps import AppConfig


class InventoryTrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory_tracking'

    def ready(self):
        import apps.inventory_tracking.signals
