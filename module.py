    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'property_mgmt'
    MODULE_NAME = _('Property Management')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'home-outline'
    MODULE_DESCRIPTION = _('Property listings, tenants and lease management')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'specialized'

    MENU = {
        'label': _('Property Management'),
        'icon': 'home-outline',
        'order': 92,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Properties'), 'icon': 'home-outline', 'id': 'properties'},
{'label': _('Tenants'), 'icon': 'people-outline', 'id': 'tenants'},
{'label': _('Leases'), 'icon': 'document-text-outline', 'id': 'leases'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'property_mgmt.view_property',
'property_mgmt.add_property',
'property_mgmt.change_property',
'property_mgmt.delete_property',
'property_mgmt.view_tenant',
'property_mgmt.add_tenant',
'property_mgmt.change_tenant',
'property_mgmt.view_lease',
'property_mgmt.add_lease',
'property_mgmt.change_lease',
'property_mgmt.manage_settings',
    ]
