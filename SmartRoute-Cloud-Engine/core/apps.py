from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'core'

    # esto es el interruptor que enciende las señales
    def ready(self):
        # Importamos las señales aqui para que Django las registre
        # Cuando la aplicacion este lista.
        import core.signals
