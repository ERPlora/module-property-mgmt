"""
Property Management Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('property_mgmt', 'dashboard')
@htmx_view('property_mgmt/pages/dashboard.html', 'property_mgmt/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('property_mgmt', 'properties')
@htmx_view('property_mgmt/pages/properties.html', 'property_mgmt/partials/properties_content.html')
def properties(request):
    """Properties view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('property_mgmt', 'tenants')
@htmx_view('property_mgmt/pages/tenants.html', 'property_mgmt/partials/tenants_content.html')
def tenants(request):
    """Tenants view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('property_mgmt', 'leases')
@htmx_view('property_mgmt/pages/leases.html', 'property_mgmt/partials/leases_content.html')
def leases(request):
    """Leases view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('property_mgmt', 'settings')
@htmx_view('property_mgmt/pages/settings.html', 'property_mgmt/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

