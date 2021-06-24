from django.apps import AppConfig


class DeveloperConfig(AppConfig):
    name = 'developer'

    def ready(self):
        import developer.signals