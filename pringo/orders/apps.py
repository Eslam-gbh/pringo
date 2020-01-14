from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'pringo.orders'

    def ready(self):
        import pringo.orders.signals  # noqa