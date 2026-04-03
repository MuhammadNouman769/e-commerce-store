''' ------------------- IMPORT ------------------- '''
from django.apps import AppConfig

''' ------------------- APP CONFIG ------------------- '''
class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'

    def ready(self):
        """ import signals """
        import apps.products.signals 
        
