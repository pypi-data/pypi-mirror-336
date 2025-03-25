"""
Django app configuration for hierarchical.
"""

from django.apps import AppConfig


class HierarchicalConfig(AppConfig):
    """
    Django app configuration for hierarchical.
    """
    name = 'hierarchical'
    verbose_name = 'Django Hierarchical Configuration'

    def ready(self):
        """
        Perform any initialization needed for hierarchical models.
        """
        # No initialization needed for non-generic version
        pass 