"""Tests for property_mgmt models."""
import pytest
from django.utils import timezone

from property_mgmt.models import Property, Tenant


@pytest.mark.django_db
class TestProperty:
    """Property model tests."""

    def test_create(self, property):
        """Test Property creation."""
        assert property.pk is not None
        assert property.is_deleted is False

    def test_str(self, property):
        """Test string representation."""
        assert str(property) is not None
        assert len(str(property)) > 0

    def test_soft_delete(self, property):
        """Test soft delete."""
        pk = property.pk
        property.is_deleted = True
        property.deleted_at = timezone.now()
        property.save()
        assert not Property.objects.filter(pk=pk).exists()
        assert Property.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, property):
        """Test default queryset excludes deleted."""
        property.is_deleted = True
        property.deleted_at = timezone.now()
        property.save()
        assert Property.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, property):
        """Test toggling is_active."""
        original = property.is_active
        property.is_active = not original
        property.save()
        property.refresh_from_db()
        assert property.is_active != original


@pytest.mark.django_db
class TestTenant:
    """Tenant model tests."""

    def test_create(self, tenant):
        """Test Tenant creation."""
        assert tenant.pk is not None
        assert tenant.is_deleted is False

    def test_str(self, tenant):
        """Test string representation."""
        assert str(tenant) is not None
        assert len(str(tenant)) > 0

    def test_soft_delete(self, tenant):
        """Test soft delete."""
        pk = tenant.pk
        tenant.is_deleted = True
        tenant.deleted_at = timezone.now()
        tenant.save()
        assert not Tenant.objects.filter(pk=pk).exists()
        assert Tenant.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, tenant):
        """Test default queryset excludes deleted."""
        tenant.is_deleted = True
        tenant.deleted_at = timezone.now()
        tenant.save()
        assert Tenant.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, tenant):
        """Test toggling is_active."""
        original = tenant.is_active
        tenant.is_active = not original
        tenant.save()
        tenant.refresh_from_db()
        assert tenant.is_active != original


