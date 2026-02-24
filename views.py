"""
Property Management Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Property, Tenant, Lease

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('property_mgmt', 'dashboard')
@htmx_view('property_mgmt/pages/index.html', 'property_mgmt/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_properties': Property.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_tenants': Tenant.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Property
# ======================================================================

PROPERTY_SORT_FIELDS = {
    'name': 'name',
    'status': 'status',
    'is_active': 'is_active',
    'monthly_rent': 'monthly_rent',
    'area_sqm': 'area_sqm',
    'bathrooms': 'bathrooms',
    'created_at': 'created_at',
}

def _build_properties_context(hub_id, per_page=10):
    qs = Property.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'properties': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_properties_list(request, hub_id, per_page=10):
    ctx = _build_properties_context(hub_id, per_page)
    return django_render(request, 'property_mgmt/partials/properties_list.html', ctx)

@login_required
@with_module_nav('property_mgmt', 'properties')
@htmx_view('property_mgmt/pages/properties.html', 'property_mgmt/partials/properties_content.html')
def properties_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Property.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(address__icontains=search_query) | Q(property_type__icontains=search_query) | Q(status__icontains=search_query))

    order_by = PROPERTY_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'status', 'is_active', 'monthly_rent', 'area_sqm', 'bathrooms']
        headers = ['Name', 'Status', 'Is Active', 'Monthly Rent', 'Area Sqm', 'Bathrooms']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='properties.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='properties.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'property_mgmt/partials/properties_list.html', {
            'properties': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'properties': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def property_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        property_type = request.POST.get('property_type', '').strip()
        bedrooms = int(request.POST.get('bedrooms', 0) or 0)
        bathrooms = int(request.POST.get('bathrooms', 0) or 0)
        area_sqm = request.POST.get('area_sqm', '0') or '0'
        monthly_rent = request.POST.get('monthly_rent', '0') or '0'
        status = request.POST.get('status', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = Property(hub_id=hub_id)
        obj.name = name
        obj.address = address
        obj.property_type = property_type
        obj.bedrooms = bedrooms
        obj.bathrooms = bathrooms
        obj.area_sqm = area_sqm
        obj.monthly_rent = monthly_rent
        obj.status = status
        obj.is_active = is_active
        obj.save()
        return _render_properties_list(request, hub_id)
    return django_render(request, 'property_mgmt/partials/panel_property_add.html', {})

@login_required
def property_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Property, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.address = request.POST.get('address', '').strip()
        obj.property_type = request.POST.get('property_type', '').strip()
        obj.bedrooms = int(request.POST.get('bedrooms', 0) or 0)
        obj.bathrooms = int(request.POST.get('bathrooms', 0) or 0)
        obj.area_sqm = request.POST.get('area_sqm', '0') or '0'
        obj.monthly_rent = request.POST.get('monthly_rent', '0') or '0'
        obj.status = request.POST.get('status', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_properties_list(request, hub_id)
    return django_render(request, 'property_mgmt/partials/panel_property_edit.html', {'obj': obj})

@login_required
@require_POST
def property_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Property, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_properties_list(request, hub_id)

@login_required
@require_POST
def property_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Property, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_properties_list(request, hub_id)

@login_required
@require_POST
def properties_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Property.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_properties_list(request, hub_id)


# ======================================================================
# Tenant
# ======================================================================

TENANT_SORT_FIELDS = {
    'name': 'name',
    'is_active': 'is_active',
    'email': 'email',
    'phone': 'phone',
    'id_number': 'id_number',
    'created_at': 'created_at',
}

def _build_tenants_context(hub_id, per_page=10):
    qs = Tenant.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'tenants': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_tenants_list(request, hub_id, per_page=10):
    ctx = _build_tenants_context(hub_id, per_page)
    return django_render(request, 'property_mgmt/partials/tenants_list.html', ctx)

@login_required
@with_module_nav('property_mgmt', 'tenants')
@htmx_view('property_mgmt/pages/tenants.html', 'property_mgmt/partials/tenants_content.html')
def tenants_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Tenant.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query) | Q(phone__icontains=search_query) | Q(id_number__icontains=search_query))

    order_by = TENANT_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'is_active', 'email', 'phone', 'id_number']
        headers = ['Name', 'Is Active', 'Email', 'Phone', 'Id Number']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='tenants.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='tenants.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'property_mgmt/partials/tenants_list.html', {
            'tenants': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'tenants': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def tenant_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        id_number = request.POST.get('id_number', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = Tenant(hub_id=hub_id)
        obj.name = name
        obj.email = email
        obj.phone = phone
        obj.id_number = id_number
        obj.is_active = is_active
        obj.save()
        return _render_tenants_list(request, hub_id)
    return django_render(request, 'property_mgmt/partials/panel_tenant_add.html', {})

@login_required
def tenant_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Tenant, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.email = request.POST.get('email', '').strip()
        obj.phone = request.POST.get('phone', '').strip()
        obj.id_number = request.POST.get('id_number', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_tenants_list(request, hub_id)
    return django_render(request, 'property_mgmt/partials/panel_tenant_edit.html', {'obj': obj})

@login_required
@require_POST
def tenant_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Tenant, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_tenants_list(request, hub_id)

@login_required
@require_POST
def tenant_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Tenant, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_tenants_list(request, hub_id)

@login_required
@require_POST
def tenants_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Tenant.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_tenants_list(request, hub_id)


@login_required
@with_module_nav('property_mgmt', 'settings')
@htmx_view('property_mgmt/pages/settings.html', 'property_mgmt/partials/settings_content.html')
def settings_view(request):
    return {}

