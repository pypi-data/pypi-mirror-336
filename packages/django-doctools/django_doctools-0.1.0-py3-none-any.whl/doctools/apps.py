"""doctools app configuration."""

from django.apps import AppConfig


class DocToolsConfig(AppConfig):
    """Configuration for the doctools app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "doctools"
    verbose_name = "Docuemnt processing tools"
