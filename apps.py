from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PropertyMgmtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'property_mgmt'
    label = 'property_mgmt'
    verbose_name = _('Property Management')

    def ready(self):
        pass
