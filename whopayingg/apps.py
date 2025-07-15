from django.apps import AppConfig


class WhopayinggConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'whopayingg'
    def ready(self):
        import whopayingg.signal
