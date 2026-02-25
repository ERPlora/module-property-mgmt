# Property Management Module

Property listings, tenants and lease management.

## Features

- Property records with address, type, bedrooms, bathrooms, and area
- Property status tracking: available, rented, under maintenance, sold
- Monthly rent assignment per property
- Tenant management with contact information and ID number
- Active/inactive tenant status
- Lease contracts linking properties to tenants
- Lease terms with start/end dates, monthly rent, and deposit amounts
- Lease status tracking

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Property Management > Settings**

## Usage

Access via: **Menu > Property Management**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/property_mgmt/dashboard/` | Property portfolio overview and statistics |
| Properties | `/m/property_mgmt/properties/` | Manage property listings |
| Tenants | `/m/property_mgmt/tenants/` | Manage tenant records |
| Leases | `/m/property_mgmt/leases/` | Create and manage lease contracts |
| Settings | `/m/property_mgmt/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `Property` | Property listing with name, address, type, bedrooms, bathrooms, area, monthly rent, status, and active flag |
| `Tenant` | Tenant record with name, email, phone, ID number, and active status |
| `Lease` | Lease contract linking a property to a tenant with start/end dates, monthly rent, deposit, and status |

## Permissions

| Permission | Description |
|------------|-------------|
| `property_mgmt.view_property` | View properties |
| `property_mgmt.add_property` | Add new properties |
| `property_mgmt.change_property` | Edit property details |
| `property_mgmt.delete_property` | Delete properties |
| `property_mgmt.view_tenant` | View tenant records |
| `property_mgmt.add_tenant` | Add new tenants |
| `property_mgmt.change_tenant` | Edit tenant details |
| `property_mgmt.view_lease` | View lease contracts |
| `property_mgmt.add_lease` | Create new leases |
| `property_mgmt.change_lease` | Edit lease details |
| `property_mgmt.manage_settings` | Access and modify module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
