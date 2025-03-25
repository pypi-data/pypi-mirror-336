# Getting Started with Django Hierarchical Models

This guide will help you install and set up the Django Hierarchical Models package in your project.

## Installation

Install the package from PyPI:

```bash
pip install hierarchical
```

Add `hierarchical` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'hierarchical',
    
    # Your apps
    'myapp',
]
```

## Basic Configuration

Django Hierarchical Models now supports configuration through Django settings. You can configure the following settings in your Django settings.py file:

```python
# Django settings.py

# Optional settings for hierarchical models
HIERARCHICAL_MODELS = {
    # Default attribute name to use for the hierarchical parent relationship
    # If not specified, defaults to 'hierarchical_parent'
    'DEFAULT_PARENT_ATTR': 'hierarchical_parent',
    
    # Enable/disable debug logging (defaults to False)
    'DEBUG': False,
}
```

The settings control the following behaviors:

- `DEFAULT_PARENT_ATTR`: Defines the default attribute name that will be used to find the parent of each model. This can be overridden on a per-model basis by defining the `HIERARCHICAL_PARENT_ATTR` class attribute on your model.

- `DEBUG`: When enabled, outputs detailed debug logging about hierarchical property access and inheritance, which can be useful for troubleshooting.

These settings are optional - if not provided, the library will use sensible defaults.

## Creating Your First Hierarchical Model

Create hierarchical models by using the `HierarchicalModelMixin` with your models:

```python
from django.db import models
from hierarchical.models import HierarchicalModelMixin

# Define a base config model
class ConfigBase(models.Model, HierarchicalModelMixin):
    # Regular fields
    name = models.CharField(max_length=100)
    
    # Fields with hierarchical inheritance (note the underscore prefix)
    _tax = models.IntegerField(null=True, blank=True)
    _percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        abstract = True

# Create concrete models in hierarchy - you can create as many levels as needed
class Country(ConfigBase):
    country_code = models.CharField(max_length=2)
    
    def __str__(self):
        return self.name

class Province(ConfigBase):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    # Define the hierarchical parent relationship
    @property
    def hierarchical_parent(self):
        return self.country
    
    def __str__(self):
        return self.name

class City(ConfigBase):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    
    @property
    def hierarchical_parent(self):
        return self.province
    
    def __str__(self):
        return self.name
```

## Using the Models

```python
# Create a hierarchy with values at different levels
canada = Country.objects.create(
    name="Canada", 
    country_code="CA",
    tax=5
)
ontario = Province.objects.create(
    name="Ontario", 
    country=canada, 
    percentage=8.0
)
toronto = City.objects.create(
    name="Toronto", 
    province=ontario
)

# Access values that traverse the hierarchy
print(toronto.tax)         # Returns 5 (inherited from country)
print(toronto.percentage)  # Returns 8.0 (inherited from province)

# Override a value at a lower level
toronto.tax = 6
toronto.save()

print(toronto.tax)  # Returns 6 (overridden)

# Clear an override to revert to inherited value
toronto.tax = None
toronto.save()

print(toronto.tax)  # Returns 5 again (inherited from country)
```

## How It Works

The mixin creates shadow fields for each field in your model, prefixed with an underscore (e.g., `_tax`). 
These shadow fields store the override values. When you access a field, the mixin:

1. Checks if the shadow field has a value
2. If not, traverses up the parent hierarchy (through any number of levels) to find a value
3. If no value is found in the hierarchy, returns None

The recursion happens automatically when accessing properties, so no matter how deep the hierarchy, 
the system will find the nearest ancestor with a value.

## Forms Support

You can work with hierarchical fields in forms in two ways:

### Simple Approach (Using Shadow Fields Directly)

The simplest approach is to directly use the shadow fields in your forms:

```python
from django import forms

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'province', '_tax', '_percentage']
        labels = {
            '_tax': 'Tax',
            '_percentage': 'Percentage'
        }
        help_texts = {
            '_tax': 'Leave blank to inherit from province',
            '_percentage': 'Leave blank to inherit from province'
        }
```

This approach is straightforward and directly manipulates the underlying shadow fields.

### Advanced Approach (Property and Shadow Fields)

For more complex UIs where you want to show inherited values and explicitly handle inheritance:

```python
from django import forms

class CityForm(forms.ModelForm):
    # Regular fields for user input
    tax = forms.IntegerField(required=False, 
                            help_text="Leave blank to inherit from province")
    percentage = forms.DecimalField(required=False, max_digits=5, decimal_places=2,
                                  help_text="Leave blank to inherit from province")
    
    class Meta:
        model = City
        fields = ['name', 'province', 'tax', 'percentage', '_tax', '_percentage']
        widgets = {
            # Hide the shadow fields with underscore prefix
            '_tax': forms.HiddenInput(),
            '_percentage': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values from the model properties
        if self.instance.pk:
            self.fields['tax'].initial = self.instance.tax
            self.fields['percentage'].initial = self.instance.percentage
            
    def clean(self):
        cleaned_data = super().clean()
        
        # Map form fields to shadow fields
        if 'tax' in cleaned_data:
            cleaned_data['_tax'] = cleaned_data['tax'] if cleaned_data['tax'] != '' else None
            
        if 'percentage' in cleaned_data:
            cleaned_data['_percentage'] = cleaned_data['percentage'] if cleaned_data['percentage'] != '' else None
            
        return cleaned_data
```

For more detailed examples, see the [Forms Integration](forms-integration.md) documentation.

## Admin Integration

Register your models with the admin site:

```python
from django.contrib import admin
from hierarchical.admin import HierarchicalModelAdmin

@admin.register(City)
class CityAdmin(HierarchicalModelAdmin):
    list_display = ('name', 'province', 'tax', 'percentage')
```

## Requirements

- Python 3.6+
- Django 2.2+

## Next Steps

Now that you have a basic understanding of Django Hierarchical Models, you can:

1. Learn about [Core Concepts](core-concepts.md) to understand how inheritance works
2. See [Basic Usage](basic-usage.md) for more examples
3. Explore [Many-to-Many Fields](many-to-many-fields.md) for handling relationships
4. Check out [Forms Integration](forms-integration.md) for form handling

## Troubleshooting

If you encounter any issues during installation or setup:

- Ensure you're using a compatible version of Django (2.2 or higher)
- Check that 'hierarchical' is properly included in INSTALLED_APPS
- Review your models to confirm shadow fields have underscore prefixes
- Make sure hierarchical_parent properties are correctly defined 