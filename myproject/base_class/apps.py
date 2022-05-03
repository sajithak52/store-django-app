from django.apps import AppConfig


class BaseClassConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_class'
