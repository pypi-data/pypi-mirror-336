# API Reference for Django Hierarchical Models

This document provides a detailed reference of all classes, methods, and attributes in the Django Hierarchical Models package.

## Models

### HierarchicalModelMixin

The core mixin that provides hierarchical inheritance capabilities to Django models.

#### Attributes

- `HIERARCHICAL_PARENT_ATTR`: (str, default: 'hierarchical_parent') - The attribute name used to access the parent object
- `SKIP_AUTO_PROPERTIES`: (list) - List of fields to exclude from automatic property creation

#### Methods

- `_get_hierarchical_value(field_name, visited_objects=None)`: Retrieves a value from the hierarchy for a given field
- `_set_hierarchical_value(field_name, value)`: Sets an override value for a field
- `clear_override(field_name)`: Clears an override to revert to inherited value
- `has_hierarchical_field(field_name)`: Checks if the model has a hierarchical field with the given name
- `_ensure_property_accessors()`: Creates property accessors for shadow fields
- `_get_shadow_fields()`: Gets all shadow fields defined on this model

### HierarchicalManagerMixin

A mixin for model managers that adds support for hierarchical property fields.

#### Methods

- `create(**kwargs)`: Creates a new instance with handling for hierarchical fields

### HierarchicalManager

A ready-to-use manager for hierarchical models that extends `HierarchicalManagerMixin` and Django's default `models.Manager`.

## Forms

The forms module has been simplified. Standard Django forms should be used with hierarchical models by directly handling the shadow fields (prefixed with underscore).

See the [Forms Integration](forms-integration.md) document for examples and best practices.

## Admin

### HierarchicalModelAdmin

A custom ModelAdmin for Django admin integration.

#### Methods

- `formfield_for_dbfield(db_field, request, **kwargs)`: Customizes form fields for hierarchical fields
- Additional methods will be documented here...

## Utility Functions

### has_hierarchical_field(model_class, field_name)

Checks if a model class has a hierarchical field with the given name.

#### Parameters

- `model_class`: The model class to check
- `field_name`: The name of the field without underscore prefix

#### Returns

- `True` if the model has the hierarchical field, `False` otherwise

### get_hierarchical_setting(key, default=None)

Gets a setting from the HIERARCHICAL_MODELS settings dictionary.

#### Parameters

- `key`: The key to look up in HIERARCHICAL_MODELS
- `default`: Default value if the key is not found

#### Returns

- The setting value or the default 