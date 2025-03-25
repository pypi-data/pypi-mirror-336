"""
Django Hierarchical Models

This module provides a mixin for enabling hierarchical models in Django, allowing
values to be inherited through unlimited levels of model relationships.

The HierarchicalModelMixin enables a model to have hierarchical fields that can:
1. Inherit values from parent models (at any level in the hierarchy)
2. Override inherited values at any level
3. Clear overrides to revert to the inherited value
"""

from django.db import models
from django.core.exceptions import FieldDoesNotExist
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

__all__ = [
    'HierarchicalModelMixin',
    'HierarchicalManager',
    'HierarchicalManagerMixin', 
    'get_hierarchical_setting',
    'has_hierarchical_field',
]

# Get settings from Django settings if available
def get_hierarchical_setting(key, default=None):
    """
    Get a setting from the HIERARCHICAL_MODELS settings dictionary.
    
    Args:
        key (str): The key to look up in HIERARCHICAL_MODELS
        default: Default value if the key is not found
        
    Returns:
        The setting value or the default
    """
    try:
        hierarchical_settings = getattr(settings, 'HIERARCHICAL_MODELS', {})
        return hierarchical_settings.get(key, default)
    except (AttributeError, TypeError):
        return default

# Default parent attribute name can be configured in settings
DEFAULT_PARENT_ATTR = get_hierarchical_setting('DEFAULT_PARENT_ATTR', 'hierarchical_parent')

# Debug logging can be enabled in settings
DEBUG_ENABLED = get_hierarchical_setting('DEBUG', False)

class HierarchicalManagerMixin:
    """
    Mixin for model managers that adds support for hierarchical property fields.
    
    This mixin can be combined with any custom manager to add support for hierarchical fields.
    It intercepts create() calls and maps property fields to their shadow database fields.
    
    Example usage:
    
    ```python
    class MyCustomManager(HierarchicalManagerMixin, models.Manager):
        # Your custom manager methods...
        def get_active(self):
            return self.filter(active=True)
    
    class MyModel(models.Model, HierarchicalModelMixin):
        _tax = models.IntegerField(null=True, blank=True)
        # ...
        
        # Use your custom manager with hierarchical support
        objects = MyCustomManager()
    ```
    """
    def create(self, **kwargs):
        """
        Handle hierarchical property fields during model creation.
        """
        # Find all shadow fields, including M2M fields
        shadow_fields = {}
        m2m_fields = {}
        
        # Find all fields that start with underscore
        for field in self.model._meta.fields:
            if field.name.startswith('_') and not field.name.startswith('__'):
                field_without_prefix = field.name[1:]
                shadow_fields[field_without_prefix] = field.name
        
        # Find M2M fields separately as they need special handling
        for field in self.model._meta.many_to_many:
            if field.name.startswith('_') and not field.name.startswith('__'):
                field_without_prefix = field.name[1:]
                m2m_fields[field_without_prefix] = field.name
        
        # Extract property fields from kwargs
        property_fields = {}
        m2m_values = {}
        
        # Process regular fields
        for prop_name, shadow_name in shadow_fields.items():
            if prop_name in kwargs:
                property_fields[shadow_name] = kwargs.pop(prop_name)
        
        # Process M2M fields separately
        for prop_name, shadow_name in m2m_fields.items():
            if prop_name in kwargs:
                m2m_values[shadow_name] = kwargs.pop(prop_name)
        
        # Add the shadow field values back to kwargs
        kwargs.update(property_fields)
        
        # Call the standard create method with modified kwargs
        instance = super().create(**kwargs)
        
        # Now handle M2M fields after the instance is created
        for shadow_field, value in m2m_values.items():
            if value is not None:
                manager = getattr(instance, shadow_field)
                # Clear any existing values (should be empty for new instances)
                manager.clear()
                
                # Add new relationships
                if value:
                    if hasattr(value, 'all'):  # If it's a QuerySet or manager
                        manager.add(*value.all())
                    elif isinstance(value, (list, tuple)):  # If it's a list/tuple
                        manager.add(*value)
                    else:  # Single object
                        manager.add(value)
        
        return instance


class HierarchicalManager(HierarchicalManagerMixin, models.Manager):
    """
    Ready-to-use manager for hierarchical models.
    
    This manager handles property fields during create() calls by mapping them to their
    corresponding shadow fields in the database.
    """
    pass


class HierarchicalModelMixin:
    """
    Mixin for enabling value inheritance through unlimited levels of model relationships.
    
    This pattern allows child models to automatically inherit certain field values
    from its parent models, while allowing for overrides at any level. The inheritance
    chain can be any number of levels deep, making it suitable for:
    
    - Geographic hierarchies (Country > Province > City > District > Building)
    - Organizational hierarchies (Company > Division > Department > Team > Employee)
    - Product hierarchies (Category > Subcategory > Product > Variant)
    - Content hierarchies (Site > Section > Page > Component)
    
    Example usage:
    
    ```python
    class Config(models.Model, HierarchicalModelMixin):
        # Config fields to be inherited
        _tax = models.IntegerField(null=True, blank=True)
        _percentage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
        
        # Properties are automatically created for each shadow field (those starting with _)
        # No need to manually define getters and setters
        
        # You can use the built-in HierarchicalManager
        objects = HierarchicalManager()
        
        # Or create your own manager with the HierarchicalManagerMixin
        class CustomManager(HierarchicalManagerMixin, models.Manager):
            def get_special(self):
                return self.filter(special=True)
                
        special_objects = CustomManager()
        
        class Meta:
            abstract = True
            
    class Country(Config):
        name = models.CharField(max_length=100)
    
    class Province(Config):
        name = models.CharField(max_length=100)
        country = models.ForeignKey(Country, on_delete=models.CASCADE)
        
        # Specify the hierarchical parent relationship
        @property
        def hierarchical_parent(self):
            return self.country
        
    class City(Config):
        name = models.CharField(max_length=100)
        province = models.ForeignKey(Province, on_delete=models.CASCADE)
        
        @property
        def hierarchical_parent(self):
            return self.province
        
    class District(Config):
        name = models.CharField(max_length=100)
        city = models.ForeignKey(City, on_delete=models.CASCADE)
        
        # If you need to use a different property name for the parent relationship
        # you can specify it with HIERARCHICAL_PARENT_ATTR
        HIERARCHICAL_PARENT_ATTR = 'custom_parent'
        
        @property
        def custom_parent(self):
            return self.city
        
    # Values cascade through the hierarchy automatically:
    district = District.objects.get(id=1)
    district.tax  # Will check District._tax, then City._tax, then Province._tax, then Country._tax
    
    # Override at any level:
    district.tax = 10  # Sets district._tax to 10
    
    # You can also set override values during creation:
    city = City.objects.create(name="Toronto", province=ontario, tax=14)
    
    IMPORTANT IMPLEMENTATION NOTES:
    - Shadow fields (e.g., '_tax') must be defined in your models to store values in the database
    - Properties are automatically created to access these fields hierarchically
    - When accessing a property, it will follow the inheritance chain if no override exists
    - By default, the mixin will look for a 'hierarchical_parent' property to determine the relationship
    - You can specify a different parent attribute by setting HIERARCHICAL_PARENT_ATTR on your model
    - To prevent automatic property creation for a field, use the SKIP_AUTO_PROPERTIES list
    """
    
    @classmethod
    def _ensure_property_accessors(cls):
        """
        Creates property accessors for all shadow fields if they don't already exist.
        This is a class method called on model initialization.
        """
        # Get fields to skip auto-property creation (if specified)
        skip_fields = getattr(cls, 'SKIP_AUTO_PROPERTIES', [])
        
        # Find all shadow fields in the class dict
        shadow_fields = []
        for field in cls._meta.fields:
            if field.name.startswith('_') and not field.name.startswith('__'):
                field_without_prefix = field.name[1:]
                if field_without_prefix not in skip_fields:
                    shadow_fields.append((field.name, field_without_prefix, False))
        
        # Also check for ManyToManyFields which need special handling
        for field in cls._meta.many_to_many:
            if field.name.startswith('_') and not field.name.startswith('__'):
                field_without_prefix = field.name[1:]
                if field_without_prefix not in skip_fields:
                    shadow_fields.append((field.name, field_without_prefix, True))
        
        # Create properties for each shadow field
        for shadow_field, field_name, is_m2m in shadow_fields:
            # Skip if property already exists
            if hasattr(cls, field_name):
                continue
                
            if is_m2m:
                # Create a getter for ManyToManyField that returns a QuerySet
                def create_m2m_getter(name):
                    def getter(self):
                        try:
                            # Get the shadow field (actual ManyToManyField)
                            shadow_field_name = f'_{name}'
                            
                            # Get the related manager for this instance
                            manager = getattr(self, shadow_field_name)
                            
                            # Check if there are overridden values at this level
                            if manager.exists():
                                return manager
                            
                            # If no overrides, try to get from parent
                            parent_attr_name = getattr(self.__class__, 'HIERARCHICAL_PARENT_ATTR', 'hierarchical_parent')
                            if hasattr(self, parent_attr_name):
                                parent = getattr(self, parent_attr_name)
                                if parent is not None and isinstance(parent, HierarchicalModelMixin):
                                    # Get the parent's property which might be inherited further up
                                    if hasattr(parent, name):
                                        return getattr(parent, name)
                            
                            # If we get here, return an empty queryset of the correct type
                            return manager.none()
                        except Exception as e:
                            logger.error(f"Error in M2M getter for {name}: {e}")
                            # Return an empty queryset for safety
                            return getattr(self, shadow_field_name).none()
                    
                    return getter
                
                # Create a setter for ManyToManyField
                def create_m2m_setter(name):
                    def setter(self, value):
                        try:
                            shadow_field_name = f'_{name}'
                            manager = getattr(self, shadow_field_name)
                            
                            # If value is None or empty collection, clear the field to remove override
                            if value is None or (hasattr(value, '__len__') and len(value) == 0):
                                # Clear the override
                                manager.clear()
                                return
                            
                            # Clear existing relationships
                            manager.clear()
                            
                            # Add new relationships if value is not None or empty
                            if hasattr(value, 'all'):  # If it's a QuerySet or manager
                                manager.add(*value.all())
                            elif isinstance(value, (list, tuple)):  # If it's a list/tuple
                                manager.add(*value)
                            else:  # Single object
                                manager.add(value)
                        except Exception as e:
                            logger.error(f"Error in M2M setter for {name}: {e}")
                    
                    return setter
                
                # Set the property with M2M-specific getter and setter
                setattr(cls, field_name, property(
                    create_m2m_getter(field_name),
                    create_m2m_setter(field_name)
                ))
            else:
                # Regular field handling (not M2M)
                # Create a getter that uses _get_hierarchical_value
                def create_getter(name):
                    def getter(self):
                        return self._get_hierarchical_value(name)
                    return getter
                    
                # Create a setter that uses _set_hierarchical_value
                def create_setter(name):
                    def setter(self, value):
                        self._set_hierarchical_value(name, value)
                    return setter
                    
                # Set the property on the class
                setattr(cls, field_name, property(
                    create_getter(field_name),
                    create_setter(field_name)
                ))
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the model and handle hierarchical field values provided during initialization.
        """
        # Ensure properties exist for this class
        self.__class__._ensure_property_accessors()
        
        # Extract shadow field values from kwargs
        hierarchical_fields = {}
        shadow_fields = self._get_shadow_fields()
        
        # Process kwargs to find hierarchical fields
        for field_name, field_without_prefix in shadow_fields.items():
            # Check for the property name first (without underscore)
            if field_without_prefix in kwargs:
                # Store value and remove from kwargs
                hierarchical_fields[field_name] = kwargs.pop(field_without_prefix)
            # Also check for direct shadow field access (with underscore)
            elif field_name in kwargs:
                # Store value and remove from kwargs
                hierarchical_fields[field_name] = kwargs.pop(field_name)
        
        # Call parent init with remaining kwargs
        super().__init__(*args, **kwargs)
        
        # Set shadow field values
        for shadow_field, value in hierarchical_fields.items():
            setattr(self, shadow_field, value)
    
    def _get_shadow_fields(self):
        """
        Get all shadow fields defined on this model.
        
        Returns a dict mapping shadow field names to their non-prefixed versions.
        """
        shadow_fields = {}
        
        # Include regular fields
        for field in self._meta.fields:
            if field.name.startswith('_') and not field.name.startswith('__'):
                # This is a shadow field
                field_without_prefix = field.name[1:]
                shadow_fields[field.name] = field_without_prefix
        
        # Also include M2M fields
        for field in self._meta.many_to_many:
            if field.name.startswith('_') and not field.name.startswith('__'):
                field_without_prefix = field.name[1:]
                shadow_fields[field.name] = field_without_prefix
                
        return shadow_fields
    
    def _get_hierarchical_value(self, field_name, visited_objects=None):
        """
        Get a value from the hierarchy for a given field.
        
        First checks for an override at current level, then traverses up the
        hierarchy to find a value. Returns None if no value is found.
        
        Args:
            field_name (str): Name of the field/property to get value for
            visited_objects (set, optional): Set of object IDs already visited
                to prevent infinite loops in cyclic references.
                
        Returns:
            The field value from the hierarchy or None if not found
        """
        # Initialize visited_objects if not provided
        if visited_objects is None:
            visited_objects = set()
        
        # Add this object to visited set to prevent cycles
        visited_objects.add(id(self))
        
        # Check for an override at the current level
        shadow_field_name = f'_{field_name}'
        try:
            # Handle M2M fields differently
            if hasattr(self.__class__, '_meta') and shadow_field_name in [f.name for f in self.__class__._meta.many_to_many]:
                # For M2M fields, check if the shadow relationship has any values
                manager = getattr(self, shadow_field_name)
                if manager.exists():
                    # This is an override with values
                    return manager
            else:
                # For regular fields, get the value directly
                override_value = getattr(self, shadow_field_name)
                if override_value is not None:
                    return override_value
        except (AttributeError, ValueError, FieldDoesNotExist):
            # Shadow field can't be accessed, continue to parent lookup
            pass
        
        # Look for the hierarchical parent using the specified attribute name
        # Try class-specific attribute first, then fall back to settings or default
        model_parent_attr = getattr(self.__class__, 'HIERARCHICAL_PARENT_ATTR', None)
        parent_attr_name = model_parent_attr or DEFAULT_PARENT_ATTR
        
        # Log debug info if enabled
        if DEBUG_ENABLED:
            logger.debug(f"Looking for parent via {parent_attr_name} on {self.__class__.__name__}")
        
        # Check if the parent attribute exists and has a value
        if hasattr(self, parent_attr_name):
            try:
                parent = getattr(self, parent_attr_name)
                # Only proceed if parent is not None and is an instance of HierarchicalModelMixin
                if parent is not None and isinstance(parent, HierarchicalModelMixin):
                    # Make sure we're not in a cycle (parent pointing to self or already visited object)
                    parent_id = id(parent)
                    if parent_id not in visited_objects:
                        parent_value = parent._get_hierarchical_value(field_name, visited_objects)
                        if parent_value is not None:
                            return parent_value
            except (AttributeError, ValueError, RecursionError):
                # If hierarchical parent can't be accessed or causes recursion, return None
                pass
        
        # No value found in hierarchy, try getting the field's default value
        try:
            field = self.__class__._meta.get_field(shadow_field_name)
            if field.default != models.NOT_PROVIDED:
                return field.default
        except (FieldDoesNotExist, AttributeError):
            pass
            
        # No value found in hierarchy
        return None
    
    def _set_hierarchical_value(self, field_name, value):
        """
        Set the override value in the shadow field (_field_name).
        
        This allows overriding parent values at any level in the hierarchy.
        """
        shadow_field_name = f'_{field_name}'
        setattr(self, shadow_field_name, value)
        
    def clear_override(self, field_name):
        """
        Clear an override for a field, reverting to the inherited value.
        """
        shadow_field_name = f'_{field_name}'
        
        # Handle regular fields
        try:
            field = self._meta.get_field(shadow_field_name)
            if isinstance(field, models.ManyToManyField):
                # For M2M fields, clear the relationships
                getattr(self, shadow_field_name).clear()
            else:
                # For regular fields, set to None
                setattr(self, shadow_field_name, None)
        except FieldDoesNotExist:
            # If the field doesn't exist, just ignore
            pass
    
    @classmethod
    def has_hierarchical_field(cls, field_name):
        """
        Check if the model has a hierarchical field with the given name.
        
        Args:
            field_name: The name of the field without underscore prefix
            
        Returns:
            True if the model has a shadow field for this field name, False otherwise
        """
        shadow_field_name = f'_{field_name}'
        
        try:
            # Try to get the field from the model's metadata
            cls._meta.get_field(shadow_field_name)
            return True
        except FieldDoesNotExist:
            # Regular field doesn't exist, also check M2M fields
            for field in cls._meta.many_to_many:
                if field.name == shadow_field_name:
                    return True
            
            return False


# Import has_hierarchical_field as a standalone function for convenience
def has_hierarchical_field(model_class, field_name):
    """
    Check if a model class has a hierarchical field.
    
    Args:
        model_class (class): The model class to check
        field_name (str): The name of the field without underscore prefix
        
    Returns:
        bool: True if the model has the hierarchical field, False otherwise
    """
    if hasattr(model_class, 'has_hierarchical_field'):
        return model_class.has_hierarchical_field(field_name)
    return False 