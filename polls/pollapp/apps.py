'''from django.apps import AppConfig


class PollappConfig(AppConfig):
    name = 'pollapp'

    '''

from django.apps import AppConfig


class AuthappConfig(AppConfig):
    name = 'pollapp'

    def ready(self):
        import pollapp.signals
