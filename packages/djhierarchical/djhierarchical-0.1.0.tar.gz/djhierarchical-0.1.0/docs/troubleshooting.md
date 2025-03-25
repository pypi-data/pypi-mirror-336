# Troubleshooting Django Hierarchical Models

This document provides solutions to common issues you might encounter when using Django Hierarchical Models.

## Common Issues

### Values Not Inheriting Correctly

**Problem**: Values from parent models are not being inherited as expected.

**Solutions**:

1. **Check field naming**: Ensure shadow fields have underscore prefixes (`_field_name`).
2. **Verify parent relationship**: Make sure the `hierarchical_parent` property returns the correct parent object.
3. **Confirm property access**: Use the property name without underscore (`field_name`) to access inherited values.

```python
# Wrong - accessing shadow field directly
value = obj._color  # This will only return overrides, not inherited values

# Correct - using property accessor
value = obj.color  # This will return inherited value if no override exists
```

### Multiple Inheritance Levels

**Problem**: Inheritance through multiple levels doesn't work as expected.

**Solution**: Verify that each model in the hierarchy correctly implements the `hierarchical_parent` property.

### M2M Field Issues

**Problem**: Many-to-Many fields don't inherit or override properly.

**Solutions**:

1. **Check related_name**: Ensure a unique `related_name` for shadow M2M fields.
2. **Verify field naming**: Confirm that shadow fields have underscore prefixes.
3. **Use correct assignment**: Use the property (not shadow field) for assignment.

### Form Handling Issues

**Problem**: Confusion about how to handle hierarchical fields in forms.

**Solutions**:

1. **Simplest approach**: Use shadow fields directly in your form with appropriate labels:
   ```python
   class MyForm(forms.ModelForm):
       class Meta:
           model = MyModel
           fields = ['name', '_field1', '_field2']
           labels = {
               '_field1': 'Field 1',
               '_field2': 'Field 2'
           }
   ```

2. **Handling BooleanFields**: For boolean fields, you may need special handling to distinguish between "false" and "inherit":
   ```python
   # In your form
   override_active = forms.BooleanField(
       required=False, 
       label="Override Active Status",
       help_text="Check this to override the inherited active status"
   )
   is_active = forms.BooleanField(required=False)
   
   # In clean method
   if cleaned_data.get('override_active'):
       cleaned_data['_is_active'] = cleaned_data.get('is_active', False)
   else:
       cleaned_data['_is_active'] = None  # Inherit
   ```

3. **M2M fields**: For M2M fields, use `None` or empty list to clear overrides and inherit:
   ```python
   # In save method
   if not cleaned_data.get('tags'):  # If empty
       instance._tags.clear()  # Clear overrides (inherit)
   else:
       instance._tags.set(cleaned_data['tags'])  # Set overrides
   ```

## Database Migration Issues

**Problem**: Adding hierarchical fields to existing models causes migration issues.

**Solutions**:

*Detailed solutions for migration issues will be added here.*

## Performance Considerations

**Problem**: Hierarchical lookups causing performance issues.

**Solutions**:

*Performance optimization suggestions will be added here.*

## Getting Help

If you encounter issues not covered in this document:

1. Check the project's GitHub issues: [GitHub Issues](https://github.com/crewii/djhierarchical/issues)
2. Submit a new issue with detailed reproduction steps
3. Include your Django and Python versions 