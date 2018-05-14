from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'

    def ready(self):
        import goods.signals