from django.apps import AppConfig


class WalletsConfig(AppConfig):
    name = "apps.wallets"

    def ready(self):
        from . import signals  # noqa: F401
