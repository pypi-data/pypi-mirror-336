# Basic Usage of Django Hierarchical Models

This document provides simple examples of using Django Hierarchical Models in your projects.

## Setting Up a Basic Hierarchy

```python
from django.db import models
from hierarchical.models import HierarchicalModelMixin

class BaseConfig(models.Model, HierarchicalModelMixin):
    # Shadow fields with underscore prefix
    _color = models.CharField(max_length=50, null=True, blank=True)
    _size = models.IntegerField(null=True, blank=True)
    
    class Meta:
        abstract = True

class Parent(BaseConfig):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Child(BaseConfig):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    
    @property
    def hierarchical_parent(self):
        return self.parent
    
    def __str__(self):
        return self.name
```

## Creating and Accessing Objects

```python
# Create parent with values
parent = Parent.objects.create(
    name="Parent Object",
    color="blue",  # Sets _color shadow field
    size=10        # Sets _size shadow field
)

# Create child with default inheritance
child1 = Child.objects.create(
    name="Child One",
    parent=parent
    # No color or size specified - will inherit from parent
)

# Verify inheritance
print(child1.color)  # "blue" (inherited from parent)
print(child1.size)   # 10 (inherited from parent)

# Create child with override
child2 = Child.objects.create(
    name="Child Two",
    parent=parent,
    color="red"    # Override parent's value
    # Size will still be inherited
)

# Verify override and inheritance
print(child2.color)  # "red" (overridden)
print(child2.size)   # 10 (inherited from parent)
```

## Modifying Values

```python
# Change parent's value
parent.color = "green"
parent.save()

# Child1 inherits the new value
print(child1.color)  # "green" (inherited from updated parent)

# Child2 keeps its override
print(child2.color)  # "red" (still overridden)

# Clear an override to revert to inherited value
child2.color = None
child2.save()

# Now child2 inherits from parent again
print(child2.color)  # "green" (now inherited after clearing override)
```

## Additional Examples

*More usage examples will be added here.* 