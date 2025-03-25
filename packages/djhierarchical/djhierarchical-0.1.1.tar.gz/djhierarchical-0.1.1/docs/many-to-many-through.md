# Many-to-Many Fields with Through Models

This document explains how to use Many-to-Many (M2M) fields with custom through models in the Django Hierarchical Models system.

## Overview

Django's hierarchical model system fully supports Many-to-Many relationships with custom through models, allowing you to add additional data on the relationship itself while still maintaining hierarchical inheritance.

Using a through model with M2M fields allows you to:
- Store additional data on the relationship (like dates, permissions, or metadata)
- Control how relationships are created and managed
- Implement more complex relationship logic

## Basic Setup

### 1. Define a Related Model

First, create the model you want to relate to:

```python
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
```

### 2. Create a Through Model

Create a through model to manage the relationship:

```python
class ServiceSubscription(models.Model):
    """Through model for organization-service relationship"""
    organization = models.ForeignKey(
        'Organization',  # Your hierarchical model
        on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )
    
    # Additional fields on the relationship
    subscription_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('organization', 'service')
```

### 3. Create a Hierarchical Model with M2M Through Field

Define your hierarchical model:

```python
from django.db import models
from hierarchical.models import HierarchicalModelMixin

class Organization(models.Model, HierarchicalModelMixin):
    name = models.CharField(max_length=100)
    
    # Shadow field for hierarchical inheritance
    _services = models.ManyToManyField(
        Service,
        through=ServiceSubscription,
        related_name="%(app_label)s_%(class)s_shadow_services",
        blank=True
    )
    
    def __str__(self):
        return self.name
```

### 4. Create Hierarchical Relationships

Define your hierarchical structure:

```python
class Enterprise(Organization):
    """Top-level organization"""
    industry = models.CharField(max_length=100)
    
class Division(Organization):
    """Mid-level organization"""
    enterprise = models.ForeignKey(
        Enterprise,
        on_delete=models.CASCADE,
        related_name='divisions'
    )
    
    @property
    def hierarchical_parent(self):
        return self.enterprise
```

## Usage Examples

### Adding Services with Through Model Attributes

When using a through model, you need to create the relationship manually:

```python
# Create an enterprise
acme = Enterprise.objects.create(name="Acme Enterprises", industry="Technology")

# Create some services
cloud_service = Service.objects.create(name="Cloud Storage", code="CLOUD")
email_service = Service.objects.create(name="Email Service", code="EMAIL")

# Create the relationships with additional data
ServiceSubscription.objects.create(
    organization=acme,
    service=cloud_service,
    priority=1
)

ServiceSubscription.objects.create(
    organization=acme,
    service=email_service,
    priority=2
)
```

### Accessing Services and Through Data

You can access both the related models and the through model data:

```python
# Create a division
tech_division = Division.objects.create(
    name="Technology Division",
    enterprise=acme
)

# Access inherited services
for service in tech_division.services.all():
    print(service.name)  # Will list "Cloud Storage" and "Email Service"

# Access through model data (need to query the through model)
subscriptions = ServiceSubscription.objects.filter(
    organization=acme,
    service__in=tech_division.services.all()
)
for sub in subscriptions:
    print(f"{sub.service.name}: Priority {sub.priority}")
```

### Overriding Services

To override services at a lower level, you need to create new through model instances:

```python
# Create another service
analytics = Service.objects.create(name="Analytics", code="ANALYTICS")

# Override at division level
ServiceSubscription.objects.create(
    organization=tech_division,
    service=analytics,
    priority=1
)
```

After this operation, `tech_division.services.all()` will only return "Analytics" because it's explicitly set, not inherited.

### Clearing Overrides

To clear overrides:

```python
# Delete all service relationships for the division
ServiceSubscription.objects.filter(organization=tech_division).delete()
```

After this operation, `tech_division.services.all()` will again inherit from the enterprise and show "Cloud Storage" and "Email Service".

## Working with the Through Model API

### Creating Relationships with Additional Data

```python
# Create a new service
security = Service.objects.create(name="Security Service", code="SEC")

# Add to enterprise with custom through data
subscription = ServiceSubscription(
    organization=acme,
    service=security,
    priority=0,  # High priority
    is_active=True
)
subscription.save()
```

### Updating Relationship Data

```python
# Update priority of an existing subscription
subscription = ServiceSubscription.objects.get(
    organization=acme,
    service=security
)
subscription.priority = 1
subscription.save()
```

### Querying Based on Through Model Fields

```python
# Find all active high-priority services
high_priority_services = Service.objects.filter(
    servicesubscription__organization=acme,
    servicesubscription__priority__lte=1,
    servicesubscription__is_active=True
)
```

## Advanced Usage: Bulk Operations

For performance with many relationships:

```python
# Bulk create service subscriptions
subscriptions = []
for service_id in range(1, 101):
    service = Service.objects.get(id=service_id)
    subscriptions.append(
        ServiceSubscription(
            organization=acme,
            service=service,
            priority=service_id % 5  # Distribute priorities
        )
    )
ServiceSubscription.objects.bulk_create(subscriptions)
```

## Forms Integration

When using M2M fields with through models in forms, you have two approaches:

### Simple Approach (Direct Shadow Field)

```python
from django import forms

class SimpleDivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name', 'enterprise', '_services']
        labels = {
            '_services': 'Services'
        }
        help_texts = {
            '_services': 'Select services or leave blank to inherit from enterprise'
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Handle through model if specific services were selected
            if '_services' in self.cleaned_data and self.cleaned_data['_services']:
                # Clear existing relationships
                ServiceSubscription.objects.filter(organization=instance).delete()
                
                # Create new relationships with default values
                for service in self.cleaned_data['_services']:
                    ServiceSubscription.objects.create(
                        organization=instance,
                        service=service,
                        priority=0  # Default priority
                    )
        
        return instance
```

### Advanced Approach (Property + Shadow Fields)

When you want more control and a better user experience:

```python
from django import forms

class DivisionForm(forms.ModelForm):
    # Basic selection of services
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        required=False,
        help_text="Select services or leave blank to inherit"
    )
    
    class Meta:
        model = Division
        fields = ['name', 'enterprise', 'services', '_services']
        widgets = {
            '_services': forms.MultipleHiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values
        if self.instance.pk:
            # Get current services through the through model
            current_services = Service.objects.filter(
                servicesubscription__organization=self.instance
            )
            self.fields['services'].initial = current_services
    
    def save(self, commit=True):
        # Get the instance
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
        
            # If services were in the form data, handle the through model
            if 'services' in self.cleaned_data:
                services = self.cleaned_data['services']
                
                # Clear existing relationships
                ServiceSubscription.objects.filter(organization=instance).delete()
                
                # If empty, just clear (will inherit from parent)
                if not services:
                    instance._services.clear()
                else:
                    # Create new relationships with default values
                    for service in services:
                        ServiceSubscription.objects.create(
                            organization=instance,
                            service=service,
                            priority=0  # Default priority
                        )
        
        return instance
```

For more advanced forms that handle through model fields, you may need to use formsets or custom form fields.

## Potential Challenges

### Avoiding Duplicate Related Items

When working with through models, be careful about creating duplicate relationships:

```python
# Check if relationship exists before creating
if not ServiceSubscription.objects.filter(
    organization=division,
    service=service
).exists():
    ServiceSubscription.objects.create(
        organization=division,
        service=service
    )
```

### Handling Inheritance with Through Models

When accessing inherited M2M fields, you're getting the related objects, not the through model instances. If you need through model data from parent relationships, you'll need to query it separately:

```python
# Get inherited services
inherited_services = division.services.all()

# Get through model data from parent if no override exists
if not ServiceSubscription.objects.filter(organization=division).exists():
    parent_subscriptions = ServiceSubscription.objects.filter(
        organization=division.hierarchical_parent,
        service__in=inherited_services
    )
```

## Next Steps

- Explore [form handling for M2M fields](forms-integration.md) for more advanced use cases
- **Note**: The Generic Many-to-Many functionality that uses `GenericForeignKey` has been deprecated. For reference, documentation on this deprecated functionality is available in the [deprecated directory](deprecated/).
- See [Admin Integration](admin-integration.md) for configuring the Django admin 