from django.apps import AppConfig


class FumetsuConfig(AppConfig):
    name = 'fumetsu'

    def ready(self):
        import fumetsu.signals