from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

PROP_STATUS = [
    ('available', _('Available')),
    ('rented', _('Rented')),
    ('maintenance', _('Under Maintenance')),
    ('sold', _('Sold')),
]

class Property(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    address = models.TextField(verbose_name=_('Address'))
    property_type = models.CharField(max_length=30, default='residential', verbose_name=_('Property Type'))
    bedrooms = models.PositiveIntegerField(default=0, verbose_name=_('Bedrooms'))
    bathrooms = models.PositiveIntegerField(default=0, verbose_name=_('Bathrooms'))
    area_sqm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name=_('Area Sqm'))
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default='0', verbose_name=_('Monthly Rent'))
    status = models.CharField(max_length=20, default='available', choices=PROP_STATUS, verbose_name=_('Status'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'property_mgmt_property'

    def __str__(self):
        return self.name


class Tenant(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_('Phone'))
    id_number = models.CharField(max_length=30, blank=True, verbose_name=_('Id Number'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'property_mgmt_tenant'

    def __str__(self):
        return self.name


class Lease(HubBaseModel):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Monthly Rent'))
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default='0', verbose_name=_('Deposit'))
    status = models.CharField(max_length=20, default='active', verbose_name=_('Status'))

    class Meta(HubBaseModel.Meta):
        db_table = 'property_mgmt_lease'

    def __str__(self):
        return str(self.id)

