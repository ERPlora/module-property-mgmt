from django.contrib import admin

from .models import Property, Tenant, Lease

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'property_type', 'bedrooms', 'bathrooms']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'id_number', 'is_active']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['property', 'tenant', 'start_date', 'end_date', 'monthly_rent']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

