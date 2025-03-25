# Admin Integration with Django Hierarchical Models

This document explains how to integrate Django Hierarchical Models with the Django Admin interface.

## Basic Admin Integration

The `HierarchicalModelAdmin` class provides special handling for hierarchical fields in the admin:

```python
from django.contrib import admin
from hierarchical.admin import HierarchicalModelAdmin
from .models import Parent, Child

@admin.register(Parent)
class ParentAdmin(HierarchicalModelAdmin):
    list_display = ('name', 'color', 'size')

@admin.register(Child)
class ChildAdmin(HierarchicalModelAdmin):
    list_display = ('name', 'parent', 'color', 'size')
    list_filter = ('parent',)
```

## Features of HierarchicalModelAdmin

The HierarchicalModelAdmin provides:

1. Visual indicators for inherited vs. overridden values
2. Proper display of hierarchical fields in list views
3. Automatic handling of shadow fields in edit forms
4. Custom fieldsets for better organization of hierarchical fields

## Customizing the Admin

You can customize how hierarchical fields are displayed in the admin:

```python
@admin.register(Child)
class ChildAdmin(HierarchicalModelAdmin):
    list_display = ('name', 'parent', 'color_with_inheritance', 'size_with_inheritance')
    list_filter = ('parent',)
    
    def color_with_inheritance(self, obj):
        value = obj.color
        if obj._color is None:
            return f"{value} (inherited)"
        return value
    
    color_with_inheritance.short_description = "Color"
    
    # Similar method for size...
```

## Advanced Admin Integration

*More advanced admin integration examples will be added here.*

## Best Practices

*Best practices for admin integration will be added here.* 