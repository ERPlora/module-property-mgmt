from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Property, Tenant

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'property_type', 'bedrooms', 'bathrooms', 'area_sqm', 'monthly_rent', 'status', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'address': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'property_type': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'bedrooms': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'bathrooms': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'area_sqm': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'monthly_rent': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'email', 'phone', 'id_number', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'email': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'id_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

