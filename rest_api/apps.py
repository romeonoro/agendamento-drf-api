from django.apps import AppConfig  # type: ignore


class RestApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rest_api"
