from django.apps import AppConfig
import os

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'

    def ready(self):
        """
        Automatically load initial fixtures (master data) if missing.
        Prevent duplicates and run only once.
        """
        from django.core.management import call_command
        from django.db.utils import OperationalError, ProgrammingError

        # Prevent runserver double-load
        if os.environ.get('RUN_MAIN'):
            return

        # List of fixture names (without .json)
        fixtures = ['brands', 'colors', 'sizes', 'materials', 'styles', 'technologies', 'categories']

        for fixture in fixtures:
            try:
                # Call Django loaddata in silent mode
                call_command('loaddata', fixture, verbosity=0)
            except (OperationalError, ProgrammingError):
                # Database not ready yet (migrations not applied), ignore
                pass
            except Exception as e:
                # Other errors ignored silently
                pass
