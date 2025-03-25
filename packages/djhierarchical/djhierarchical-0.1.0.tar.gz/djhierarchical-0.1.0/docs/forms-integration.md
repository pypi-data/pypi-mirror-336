# Forms Integration with Django Hierarchical Models

This document explains how to use Django forms with hierarchical models to provide a good user experience for editing hierarchical data.

## Basic Form Integration

The simplest approach for working with hierarchical fields in Django forms is to directly use the shadow fields (prefixed with underscore) in your form:

```python
from django import forms

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'parent', '_color', '_size']
        labels = {
            '_color': 'Color',
            '_size': 'Size'
        }
        help_texts = {
            '_color': 'Enter a color or leave blank to inherit from parent',
            '_size': 'Enter a size or leave blank to inherit from parent'
        }
```

This approach is straightforward and directly manipulates the underlying shadow fields that store the override values.

## Advanced Approach: Property and Shadow Fields

For more complex user interfaces where you want to show inherited values and explicitly handle inheritance, you can include both the property fields and their shadow fields:

```python
from django import forms

class RegionForm(forms.ModelForm):
    # Define the visible fields
    tax_rate = forms.DecimalField(max_digits=5, decimal_places=2, required=False,
                                  help_text="Override tax rate or leave blank to inherit")
    is_active = forms.BooleanField(required=False,
                                   help_text="Override active status or leave blank to inherit")
    
    class Meta:
        model = Region
        fields = ['name', 'parent', 'tax_rate', 'is_active', '_tax_rate', '_is_active']
        widgets = {
            '_tax_rate': forms.HiddenInput(),
            '_is_active': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            # Set initial values for the visible fields from the model property
            self.fields['tax_rate'].initial = self.instance.tax_rate
            self.fields['is_active'].initial = self.instance.is_active
            
            # Add inherited value to help text if available
            if hasattr(self.instance, 'hierarchical_parent') and self.instance.hierarchical_parent:
                parent = self.instance.hierarchical_parent
                self.fields['tax_rate'].help_text += f" (Inherited: {parent.tax_rate})"
                self.fields['is_active'].help_text += f" (Inherited: {parent.is_active})"
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Map visible fields to shadow fields
        # If field is empty, set shadow field to None (inherit from parent)
        # Otherwise, set shadow field to the entered value
        if 'tax_rate' in cleaned_data:
            cleaned_data['_tax_rate'] = cleaned_data['tax_rate'] if cleaned_data['tax_rate'] != '' else None
            
        if 'is_active' in cleaned_data:
            cleaned_data['_is_active'] = cleaned_data['is_active'] if cleaned_data['is_active'] != '' else None
            
        return cleaned_data
```

## Handling ManyToMany Fields

For ManyToMany fields, you can use the same approaches:

### Simple Approach (Direct Shadow Field)

```python
from django import forms

class SimpleOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'parent', '_tags']
        labels = {
            '_tags': 'Tags'
        }
        help_texts = {
            '_tags': 'Select tags or leave blank to inherit from parent'
        }
```

### Advanced Approach (Property + Shadow Fields)

```python
from django import forms

class OrganizationForm(forms.ModelForm):
    # Regular fields
    name = forms.CharField(max_length=100)
    parent = forms.ModelChoiceField(queryset=Organization.objects.all(), required=False)
    
    # ManyToMany field
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        help_text="Select tags or leave blank to inherit"
    )
    
    class Meta:
        model = Organization
        fields = ['name', 'parent', 'tags', '_tags']
        widgets = {
            '_tags': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            # Set initial values for the M2M field
            self.fields['tags'].initial = self.instance.tags.all()
            
            # Add inherited value to help text if available
            if hasattr(self.instance, 'hierarchical_parent') and self.instance.hierarchical_parent:
                parent = self.instance.hierarchical_parent
                parent_tags = list(parent.tags.all()[:3])
                
                if parent_tags:
                    tag_names = ", ".join(str(tag) for tag in parent_tags)
                    if parent.tags.count() > 3:
                        tag_names += f" and {parent.tags.count() - 3} more"
                    self.fields['tags'].help_text += f" (Inherited: {tag_names})"
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Handle the M2M relationship
            if 'tags' in self.cleaned_data:
                tags = self.cleaned_data['tags']
                
                # If no tags selected, clear the override (inherit from parent)
                if not tags:
                    instance._tags.clear()
                else:
                    # Otherwise set the selected tags
                    instance._tags.set(tags)
                    
        return instance
```

## Choosing the Right Approach

- **Simple Approach**: Use only shadow fields when you want a straightforward form that directly manipulates the override data.
- **Advanced Approach**: Use both property and shadow fields when you want to show inherited values and provide a more intuitive interface for users.

## JavaScript Enhancements

You might want to enhance the user experience with JavaScript to:
- Toggle between inherited values and overrides
- Show visual indicators for inheritance status
- Provide "reset to inherited" buttons 