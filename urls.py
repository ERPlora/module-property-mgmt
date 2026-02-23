from django.urls import path
from . import views

app_name = 'property_mgmt'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('properties/', views.properties, name='properties'),
    path('tenants/', views.tenants, name='tenants'),
    path('leases/', views.leases, name='leases'),
    path('settings/', views.settings, name='settings'),
]
