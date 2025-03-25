# Many-to-Many Fields in Hierarchical Models

This document explains how to use Many-to-Many (M2M) fields in the Django Hierarchical Models system.

## Overview

Hierarchical models can include Many-to-Many relationships that inherit from parent models, just like regular fields. This enables powerful patterns for managing related objects across a hierarchy.

Common use cases include:
- Assigning services or features at different organizational levels
- Role-based permissions that inherit down a hierarchy
- Product categories or tags that cascade down product hierarchies

## Basic Setup

### 1. Define a Related Model

First, create a model for the entities you want to relate to:

```python
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name
```

### 2. Create a Hierarchical Model with an M2M Field

Define your hierarchical model with a shadow field for the M2M relationship:

```python
from django.db import models
from hierarchical.models import HierarchicalModelMixin

class Organization(models.Model, HierarchicalModelMixin):
    name = models.CharField(max_length=100)
    
    # Shadow field for hierarchical M2M inheritance - note the underscore prefix
    _roles = models.ManyToManyField(
        Role,
        blank=True,
        # Use a unique related_name to avoid conflicts with auto-generated property
        related_name="%(app_label)s_%(class)s_shadow_roles"
    )
    
    def __str__(self):
        return self.name
```

### 3. Create Hierarchical Relationships

Define your hierarchical structure:

```python
class Company(Organization):
    website = models.URLField(blank=True)
    
    # Top-level organization has no hierarchical parent

class Department(Organization):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='departments'
    )
    
    # Define hierarchical parent
    @property
    def hierarchical_parent(self):
        return self.company
```

## Usage Examples

### Assigning Roles at the Company Level

```python
# Create a company
acme = Company.objects.create(name="Acme Corp")

# Create some roles
admin_role = Role.objects.create(name="Administrator", code="ADMIN")
editor_role = Role.objects.create(name="Editor", code="EDITOR")

# Assign roles to the company
acme.roles = [admin_role, editor_role]  # Using the property (not _roles)
```

### Inheriting Roles at the Department Level

```python
# Create a department
hr_dept = Department.objects.create(name="Human Resources", company=acme)

# Access inherited roles
for role in hr_dept.roles.all():
    print(role.name)  # Will print "Administrator" and "Editor"
```

### Overriding Roles at the Department Level

```python
# Create another role
hr_role = Role.objects.create(name="HR Manager", code="HR_MGR")

# Override roles at department level
hr_dept.roles = [hr_role]  # Replaces inherited roles
```

### Clearing Overrides

```python
# Clear the override to return to inherited values
hr_dept.roles = None  # or hr_dept.roles = []

# Now hr_dept.roles will again inherit from company
```

## Important Details

### Shadow Field Naming Convention

Always use an underscore prefix for shadow M2M fields:

```python
# Correct - shadow field with underscore
_roles = models.ManyToManyField(Role, ...)

# Incorrect - missing underscore prefix
roles = models.ManyToManyField(Role, ...)
```

### Unique Related Names

To avoid conflicts with Django's auto-generated related names, always provide a unique `related_name` for M2M shadow fields:

```python
# Good pattern using Django's name replacement
_roles = models.ManyToManyField(
    Role, 
    related_name="%(app_label)s_%(class)s_shadow_roles"
)

# Alternative with explicit name
_roles = models.ManyToManyField(
    Role, 
    related_name="organization_shadow_roles"
)
```

### Mixing Hierarchical and Regular M2M Fields

You can use both hierarchical and regular M2M fields in the same model:

```python
class Organization(models.Model, HierarchicalModelMixin):
    # Hierarchical M2M field (with shadow field)
    _roles = models.ManyToManyField(
        Role, 
        blank=True,
        related_name="%(app_label)s_%(class)s_shadow_roles"
    )
    
    # Regular M2M field (non-hierarchical)
    direct_members = models.ManyToManyField(
        'User',
        blank=True,
        related_name="%(app_label)s_%(class)s_direct_membership"
    )
```

## Working with Forms

There are two approaches to handle M2M hierarchical fields in forms:

### Simple Approach (Direct Shadow Field)

The simplest approach is to directly use the shadow field in your form:

```python
from django import forms

class SimpleDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'company', '_roles']
        labels = {
            '_roles': 'Roles'
        }
        help_texts = {
            '_roles': 'Select roles or leave blank to inherit from parent company'
        }
```

This approach directly manipulates the shadow field that stores the overrides.

### Advanced Approach (Property + Shadow Fields)

For more complex UIs where you want to show inherited values and explicitly handle inheritance:

```python
from django import forms

class DepartmentForm(forms.ModelForm):
    # Define form field for the M2M property
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,
        help_text="Leave blank to inherit roles from parent"
    )
    
    class Meta:
        model = Department
        fields = ['name', 'company', 'roles', '_roles']
        widgets = {
            '_roles': forms.MultipleHiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for the M2M field
        if self.instance.pk:
            self.fields['roles'].initial = self.instance.roles.all()
            
            # Add inherited value info if there's a parent
            if self.instance.company:
                parent_roles = list(self.instance.company.roles.all())
                if parent_roles:
                    roles_list = ", ".join(str(r) for r in parent_roles[:3])
                    if len(parent_roles) > 3:
                        roles_list += f" and {len(parent_roles) - 3} more"
                    self.fields['roles'].help_text += f" (Inherited: {roles_list})"
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Handle the M2M relationship
            if 'roles' in self.cleaned_data:
                roles = self.cleaned_data['roles']
                
                # If no roles selected, clear the override (inherit from parent)
                if not roles:
                    instance._roles.clear()
                else:
                    # Otherwise set the selected roles
                    instance._roles.set(roles)
                    
        return instance

## Performance Considerations

For best performance with M2M fields:

1. Use `select_related()` when fetching parent objects
2. Use `prefetch_related()` for M2M relationships in querysets
3. Consider indexing frequently queried fields on related models

## Next Steps

- Learn more about [using custom through models](many-to-many-through.md) with Many-to-Many fields
- **Note**: The Generic Many-to-Many functionality that uses `GenericForeignKey` has been deprecated. For reference, documentation on this deprecated functionality is available in the [deprecated directory](deprecated/). 