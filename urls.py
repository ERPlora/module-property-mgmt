from django.urls import path
from . import views

app_name = 'property_mgmt'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Property
    path('properties/', views.properties_list, name='properties_list'),
    path('properties/add/', views.property_add, name='property_add'),
    path('properties/<uuid:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<uuid:pk>/delete/', views.property_delete, name='property_delete'),
    path('properties/<uuid:pk>/toggle/', views.property_toggle_status, name='property_toggle_status'),
    path('properties/bulk/', views.properties_bulk_action, name='properties_bulk_action'),

    # Tenant
    path('tenants/', views.tenants_list, name='tenants_list'),
    path('tenants/add/', views.tenant_add, name='tenant_add'),
    path('tenants/<uuid:pk>/edit/', views.tenant_edit, name='tenant_edit'),
    path('tenants/<uuid:pk>/delete/', views.tenant_delete, name='tenant_delete'),
    path('tenants/<uuid:pk>/toggle/', views.tenant_toggle_status, name='tenant_toggle_status'),
    path('tenants/bulk/', views.tenants_bulk_action, name='tenants_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
