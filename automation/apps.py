# automation/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _  # opcional p/ i18n

class AutomationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "automation"              # NÃO mude: é o path do app
    verbose_name = _("Engenharia de Automação")    # <-- o nome que aparece no admin
    # exemplo: _("JF Metrics"), _("Tempo & Produção"), etc.
