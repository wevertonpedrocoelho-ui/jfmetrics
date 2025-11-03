# epe/apps.py
from django.apps import AppConfig

class EpeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "epe"
    verbose_name = "Engenharia de Painéis Elétricos"
