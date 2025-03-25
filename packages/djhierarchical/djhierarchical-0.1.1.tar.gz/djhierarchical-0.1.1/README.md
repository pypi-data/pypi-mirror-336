# Django Hierarchical Configuration

[![PyPI version](https://img.shields.io/pypi/v/djhierarchical.svg)](https://pypi.org/project/djhierarchical/)
[![Python Versions](https://img.shields.io/pypi/pyversions/djhierarchical.svg)](https://pypi.org/project/djhierarchical/)
[![Django Versions](https://img.shields.io/pypi/djversions/djhierarchical.svg)](https://pypi.org/project/djhierarchical/)
[![CI Status](https://github.com/aibin/djhierarchical/workflows/CI/badge.svg)](https://github.com/aibin/djhierarchical/actions)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://aibin.github.io/djhierarchical/)
[![License](https://img.shields.io/github/license/aibin/djhierarchical.svg)](https://github.com/aibin/djhierarchical/blob/main/LICENSE)

A Django app that provides a hierarchical configuration pattern with automatic inheritance between related models at any number of levels deep.

## Documentation

📚 **[Read the full documentation](https://aibin.github.io/djhierarchical/)**

## Features

- 🔄 Automatic inheritance of values from parent models through unlimited hierarchy levels
- 🛠️ Simple API using standard Django model field access 
- 🎯 Override values at any level in the hierarchy
- 📋 Shadow fields with underscore prefix for storing overrides
- ✅ Works with any Django model field type, including ManyToMany relationships
- 📊 Visual indicators of inheritance in admin interface
- 🔄 Unlimited depth of inheritance (not limited to just parent-child relationships)
- 🧩 Easy integration with Django forms using shadow fields
- ⚙️ Configurable via Django settings

## Installation

```bash
pip install djhierarchical
```

Add `hierarchical` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # ...
    'hierarchical',
    # ...
]
```

Note: The package name on PyPI is `djhierarchical`, but the Django app name to use in `INSTALLED_APPS` is `hierarchical`.

## Configuration (Optional)

You can configure the behavior of hierarchical models through Django settings:

```python
# Optional settings for hierarchical models
HIERARCHICAL_MODELS = {
    # Default attribute name to use for the hierarchical parent relationship
    'DEFAULT_PARENT_ATTR': 'hierarchical_parent',
    
    # Enable/disable debug logging
    'DEBUG': False,
}
```

## Quick Start

Create hierarchical models by using the `HierarchicalModelMixin` with your models:

```python
from django.db import models
from hierarchical.models import HierarchicalModelMixin

# Define a base config model
class ConfigBase(models.Model, HierarchicalModelMixin):
    # Regular fields
    name = models.CharField(max_length=100)
    
    # Shadow fields with underscore prefix for hierarchical inheritance
    _tax = models.IntegerField(null=True, blank=True)
    _percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        abstract = True

# Create concrete models in hierarchy - you can create as many levels as needed
class Country(ConfigBase):
    name = models.CharField(max_length=100)
    
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

class District(ConfigBase):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
    @property
    def hierarchical_parent(self):
        return self.city
    
    def __str__(self):
        return self.name

class Building(ConfigBase):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    
    @property
    def hierarchical_parent(self):
        return self.district
    
    def __str__(self):
        return self.name
```

### Using the models

```python
# Create a hierarchy with values at different levels
canada = Country.objects.create(name="Canada", tax=5)
ontario = Province.objects.create(name="Ontario", country=canada, percentage=8.0)
toronto = City.objects.create(name="Toronto", province=ontario)
downtown = District.objects.create(name="Downtown", city=toronto, tax=6)
tower = Building.objects.create(name="CN Tower", district=downtown)

# Access values that traverse multiple levels in the hierarchy
tower.tax  # Returns 6 (from district)
tower.percentage  # Returns 8.0 (from province, skipping city level)

# Deep inheritance is handled automatically
if ontario.tax is None:
    ontario.tax = 7
    ontario.save()

downtown.percentage = 9.0
downtown.save()

tower.tax  # Still returns 6 (from district)
tower.percentage  # Returns 9.0 (from district now)
```

### ManyToMany Fields

You can also use hierarchical ManyToMany fields:

```python
class Tag(models.Model):
    name = models.CharField(max_length=100)

class Organization(models.Model, HierarchicalModelMixin):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    # Hierarchical ManyToMany field (note the underscore prefix)
    _tags = models.ManyToManyField(Tag, blank=True)
    
    @property
    def hierarchical_parent(self):
        return self.parent
```

### Forms Support

The simplest way to work with hierarchical fields in Django forms is to directly use the shadow fields (with underscore prefix):

```python
from django import forms

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'district', '_tax', '_percentage']
        labels = {
            '_tax': 'Tax',
            '_percentage': 'Percentage'
        }
        help_texts = {
            '_tax': 'Enter a value or leave blank to inherit from district',
            '_percentage': 'Enter a value or leave blank to inherit from district'
        }
```

For more complex scenarios, where you want to show inherited values and explicitly handle inheritance, you can use both property fields and shadow fields:

```python
from django import forms

class BuildingForm(forms.ModelForm):
    # Define form fields for visibility
    tax = forms.IntegerField(required=False)
    percentage = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    class Meta:
        model = Building
        fields = ['name', 'district', 'tax', 'percentage', '_tax', '_percentage']
        widgets = {
            '_tax': forms.HiddenInput(),
            '_percentage': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for the form fields
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

For more detailed examples, see the [forms integration documentation](docs/forms-integration.md).

## How It Works

The mixin creates shadow fields for each field in your model, prefixed with an underscore (e.g., `_tax`). 
These shadow fields store the override values. When you access a field, the mixin:

1. Checks if the shadow field has a value
2. If not, traverses up the parent hierarchy (through any number of levels) to find a value
3. If no value is found in the hierarchy, returns None

The recursion happens automatically when accessing properties, so no matter how deep the hierarchy, 
the system will find the nearest ancestor with a value.

## Advanced Usage

### Clearing an Override

To clear an override and fall back to the parent value:

```python
city.clear_override('tax')  # Clear the override, will now inherit from province
```

Or by setting the value to None:

```python
city.tax = None  # Also clears the override
city.save()
```

### Using in Admin

Register your models with the admin site:

```python
from django.contrib import admin
from hierarchical.admin import HierarchicalModelAdmin

@admin.register(City)
class CityAdmin(HierarchicalModelAdmin):
    list_display = ('name', 'province', 'tax', 'percentage')
```

## Development

Clone the repository:

```bash
git clone https://github.com/crewii/djhierarchical.git
cd djhierarchical
pip install -e .
```

Run tests:

```bash
python runtests.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 