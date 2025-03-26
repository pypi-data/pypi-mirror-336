"""
Django apps config file for dcauth.
"""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """
    App config for dcauth.

    Needed to register signal for CAS authentication.
    """
    name = "dc_auth"

    def ready(self):
        # pylint: disable=import-outside-toplevel,unused-import
        import dc_auth.signals  # noqa: F401
