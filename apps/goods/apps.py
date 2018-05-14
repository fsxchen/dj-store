from django.apps import AppConfig


class GoodsConfig(AppConfig):
    name = 'goods'
    def ready(self):
        import goods.signals