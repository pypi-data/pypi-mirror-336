from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApikeyAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apikey_auth"
    verbose_name = _("Django ApiKey Auth")

    def ready(self):
        """This method is called when the application is fully loaded.

        Its main purpose is to perform startup tasks, such as importing
        and registering system checks for validating the configuration
        settings of the app. It ensures that all necessary configurations
        are in place and properly validated when the Django project initializes.

        In this case, it imports the settings checks from the
        `apikey_auth.settings` module to validate the configuration
        settings.

        """
        from apikey_auth.settings import checks
