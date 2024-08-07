from django.apps import AppConfig

class TeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'te'

    def ready(self):
        import te.signals
