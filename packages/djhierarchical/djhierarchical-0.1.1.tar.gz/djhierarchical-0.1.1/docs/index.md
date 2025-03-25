---
layout: default
title: Django Hierarchical Models
---

# Django Hierarchical Models

[![PyPI version](https://img.shields.io/pypi/v/djhierarchical.svg)](https://pypi.org/project/djhierarchical/)
[![Python Versions](https://img.shields.io/pypi/pyversions/djhierarchical.svg)](https://pypi.org/project/djhierarchical/)
[![Django Versions](https://img.shields.io/pypi/djversions/djhierarchical.svg)](https://pypi.org/project/djhierarchical/)
[![CI Status](https://github.com/aibin/djhierarchical/workflows/CI/badge.svg)](https://github.com/aibin/djhierarchical/actions)
[![License](https://img.shields.io/github/license/aibin/djhierarchical.svg)](https://github.com/aibin/djhierarchical/blob/main/LICENSE)

A Django app that provides a hierarchical configuration pattern with automatic inheritance between related models at any number of levels deep.

## Documentation

- [Getting Started](getting-started.html)
- [Core Concepts](core-concepts.html)
- [Basic Usage](basic-usage.html)
- [Forms Integration](forms-integration.html)
- [Admin Integration](admin-integration.html)
- [ManyToMany Fields](many-to-many-fields.html)
- [ManyToMany Through Relations](many-to-many-through.html)
- [API Reference](api-reference.html)
- [Troubleshooting](troubleshooting.html)

## Use Cases

- [Feature Flags](use-cases/feature-flags.html)
- [Multi-tenant Configuration](use-cases/multi-tenant.html)
- [Hierarchical Permissions](use-cases/permissions.html)
- [Organization Settings](use-cases/settings.html)
- [Simple Configuration](use-cases/simple-config.html)

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

## Links

- [GitHub Repository](https://github.com/aibin/djhierarchical)
- [PyPI Package](https://pypi.org/project/djhierarchical/)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/aibin/djhierarchical/blob/main/LICENSE) file for details. 