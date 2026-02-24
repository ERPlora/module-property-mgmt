"""Tests for property_mgmt views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('property_mgmt:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('property_mgmt:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('property_mgmt:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestPropertyViews:
    """Property view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('property_mgmt:properties_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('property_mgmt:properties_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('property_mgmt:properties_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('property_mgmt:properties_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('property_mgmt:properties_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('property_mgmt:properties_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('property_mgmt:property_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('property_mgmt:property_add')
        data = {
            'name': 'New Name',
            'address': 'Test description',
            'property_type': 'New Property Type',
            'bedrooms': '5',
            'bathrooms': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, property):
        """Test edit form loads."""
        url = reverse('property_mgmt:property_edit', args=[property.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, property):
        """Test editing via POST."""
        url = reverse('property_mgmt:property_edit', args=[property.pk])
        data = {
            'name': 'Updated Name',
            'address': 'Test description',
            'property_type': 'Updated Property Type',
            'bedrooms': '5',
            'bathrooms': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, property):
        """Test soft delete via POST."""
        url = reverse('property_mgmt:property_delete', args=[property.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        property.refresh_from_db()
        assert property.is_deleted is True

    def test_toggle_status(self, auth_client, property):
        """Test toggle active status."""
        url = reverse('property_mgmt:property_toggle_status', args=[property.pk])
        original = property.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        property.refresh_from_db()
        assert property.is_active != original

    def test_bulk_delete(self, auth_client, property):
        """Test bulk delete."""
        url = reverse('property_mgmt:properties_bulk_action')
        response = auth_client.post(url, {'ids': str(property.pk), 'action': 'delete'})
        assert response.status_code == 200
        property.refresh_from_db()
        assert property.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('property_mgmt:properties_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestTenantViews:
    """Tenant view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('property_mgmt:tenants_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('property_mgmt:tenants_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('property_mgmt:tenants_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('property_mgmt:tenants_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('property_mgmt:tenants_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('property_mgmt:tenants_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('property_mgmt:tenant_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('property_mgmt:tenant_add')
        data = {
            'name': 'New Name',
            'email': 'test@example.com',
            'phone': 'New Phone',
            'id_number': 'New Id Number',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, tenant):
        """Test edit form loads."""
        url = reverse('property_mgmt:tenant_edit', args=[tenant.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, tenant):
        """Test editing via POST."""
        url = reverse('property_mgmt:tenant_edit', args=[tenant.pk])
        data = {
            'name': 'Updated Name',
            'email': 'test@example.com',
            'phone': 'Updated Phone',
            'id_number': 'Updated Id Number',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, tenant):
        """Test soft delete via POST."""
        url = reverse('property_mgmt:tenant_delete', args=[tenant.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        tenant.refresh_from_db()
        assert tenant.is_deleted is True

    def test_toggle_status(self, auth_client, tenant):
        """Test toggle active status."""
        url = reverse('property_mgmt:tenant_toggle_status', args=[tenant.pk])
        original = tenant.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        tenant.refresh_from_db()
        assert tenant.is_active != original

    def test_bulk_delete(self, auth_client, tenant):
        """Test bulk delete."""
        url = reverse('property_mgmt:tenants_bulk_action')
        response = auth_client.post(url, {'ids': str(tenant.pk), 'action': 'delete'})
        assert response.status_code == 200
        tenant.refresh_from_db()
        assert tenant.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('property_mgmt:tenants_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('property_mgmt:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('property_mgmt:settings')
        response = client.get(url)
        assert response.status_code == 302

