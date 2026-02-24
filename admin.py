from django.contrib import admin

from .models import Property, Tenant, Lease

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'property_type', 'bedrooms', 'bathrooms', 'created_at']
    search_fields = ['name', 'address', 'property_type', 'status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'id_number', 'is_active', 'created_at']
    search_fields = ['name', 'email', 'phone', 'id_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ['property', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'created_at']
    search_fields = ['status']
    readonly_fields = ['created_at', 'updated_at']

