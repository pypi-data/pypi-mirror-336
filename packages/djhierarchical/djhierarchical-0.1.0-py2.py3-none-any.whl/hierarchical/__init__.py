"""
Django Hierarchical Configuration.

A Django app that provides a hierarchical configuration pattern with 
automatic inheritance between related models.
"""

__version__ = '0.1.0'

# Import main components for ease of use
from .models import (
    HierarchicalModelMixin,
    HierarchicalManager,
    HierarchicalManagerMixin,
    has_hierarchical_field
) 