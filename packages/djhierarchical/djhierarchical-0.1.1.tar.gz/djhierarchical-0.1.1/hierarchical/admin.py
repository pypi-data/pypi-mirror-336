"""
Admin integration for hierarchical models.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import get_hierarchical_setting

# Default parent attribute name from settings
DEFAULT_PARENT_ATTR = get_hierarchical_setting('DEFAULT_PARENT_ATTR', 'hierarchical_parent')

class HierarchicalModelAdmin(admin.ModelAdmin):
    """
    Admin class for models using HierarchicalModelMixin.
    
    Provides enhanced display of hierarchical fields including:
    - Visual indicators for overridden vs inherited values
    - Field-level information about the inheritance
    """
    
    def get_fieldsets(self, request, obj=None):
        """Customize fieldsets to group hierarchical fields together"""
        fieldsets = super().get_fieldsets(request, obj)
        
        if obj:
            # Find hierarchical fields
            hierarchical_fields = []
            for field in obj._meta.fields:
                if not field.name.startswith('_') and hasattr(obj, f'_{field.name}'):
                    hierarchical_fields.append(field.name)
            
            # If we found hierarchical fields, add a special fieldset
            if hierarchical_fields and fieldsets[0][0] is None:
                fieldsets[0][1]['fields'] = [f for f in fieldsets[0][1]['fields'] 
                                           if f not in hierarchical_fields]
                fieldsets.append(('Hierarchical Settings', {'fields': hierarchical_fields,
                                                         'classes': ('collapse',)}))
        
        return fieldsets
    
    def get_readonly_fields(self, request, obj=None):
        """Add dynamic readonly fields to show inheritance info"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        if obj:
            # For each hierarchical field, add an info field
            for field in obj._meta.fields:
                if not field.name.startswith('_') and hasattr(obj, f'_{field.name}'):
                    info_field = f'{field.name}_inheritance_info'
                    if info_field not in readonly_fields:
                        readonly_fields.append(info_field)
                        # Dynamically add method
                        setattr(self, info_field, self._make_inheritance_info_method(field.name))
        
        return readonly_fields
    
    def _make_inheritance_info_method(self, field_name):
        """Create a method that shows inheritance info for a field"""
        def inheritance_info(obj):
            # Get the current override value
            override_value = getattr(obj, f'_{field_name}')
            
            # Temporarily clear the override to get the inherited value
            setattr(obj, f'_{field_name}', None)
            inherited_value = getattr(obj, field_name)
            # Restore the override
            setattr(obj, f'_{field_name}', override_value)
            
            # Build the inheritance chain
            chain_info = self._get_inheritance_chain(obj, field_name)
            
            if override_value is not None:
                # Show that this value is overridden
                return format_html(
                    '<div class="hierarchical-info overridden">'
                    '<span class="badge badge-info">Overridden</span> '
                    'Current value: <strong>{}</strong><br>'
                    'Inherited value would be: {}<br><br>'
                    '{}'
                    '</div>',
                    override_value,
                    inherited_value if inherited_value is not None else '<em>None</em>',
                    chain_info
                )
            else:
                # Show that this value is inherited
                return format_html(
                    '<div class="hierarchical-info inherited">'
                    '<span class="badge badge-secondary">Inherited</span> '
                    'Value: <strong>{}</strong><br><br>'
                    '{}'
                    '</div>',
                    inherited_value if inherited_value is not None else '<em>None</em>',
                    chain_info
                )
        
        # Set the short description
        inheritance_info.short_description = f"{field_name.replace('_', ' ').title()} Inheritance"
        return inheritance_info
    
    def _get_inheritance_chain(self, obj, field_name):
        """Build HTML showing the inheritance chain for a field"""
        result = ['<div class="inheritance-chain"><strong>Inheritance Chain:</strong><ul>']
        
        # Start with this object
        shadow_value = getattr(obj, f'_{field_name}')
        result.append(
            f'<li>{obj._meta.verbose_name.title()}: {obj} - '
            f'{"<strong>Overridden</strong>" if shadow_value is not None else "Inherited"}'
            f'</li>'
        )
        
        # Get the parent attribute name for this model
        parent_attr = getattr(obj.__class__, 'HIERARCHICAL_PARENT_ATTR', DEFAULT_PARENT_ATTR)
        
        # If model has hierarchical parent method, use it directly
        if hasattr(obj, parent_attr):
            parent = getattr(obj, parent_attr)
            if parent and hasattr(parent, field_name):
                parent_shadow_value = getattr(parent, f'_{field_name}', None)
                parent_value = getattr(parent, field_name, None)
                result.append(
                    f'<li>{parent._meta.verbose_name.title()}: {parent} - '
                    f'{"<strong>Overridden</strong>" if parent_shadow_value is not None else "Inherited"}'
                    f' - Value: {parent_value if parent_value is not None else "<em>None</em>"}'
                    f'</li>'
                )
                
                # Recursively add parent's chain if possible
                if hasattr(parent, '_get_inheritance_chain'):
                    parent_chain = parent._get_inheritance_chain(field_name)
                    if parent_chain:
                        result.extend(parent_chain)
        
        result.append('</ul></div>')
        return ''.join(result)
    
    class Media:
        css = {
            'all': ('admin/css/hierarchical.css',)
        } 