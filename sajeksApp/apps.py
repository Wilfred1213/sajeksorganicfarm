from django.apps import AppConfig


class SajeksappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sajeksApp'

    def ready(self):
        """Import signals here to ensure they are connected when Django starts."""
        import sajeksApp.signals 
