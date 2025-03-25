# Documentation for Django Hierarchical Models

This directory contains the documentation for Django Hierarchical Models. The documentation is hosted on GitHub Pages at [https://aibin.github.io/djhierarchical/](https://aibin.github.io/djhierarchical/).

## Table of Contents

1. [Getting Started](getting-started.md) - Installation and basic setup
2. [Core Concepts](core-concepts.md) - Understanding hierarchical inheritance
3. [Basic Usage](basic-usage.md) - Simple examples of hierarchical models
4. [Many-to-Many Fields](many-to-many-fields.md) - How to work with M2M fields in hierarchical models
5. [Many-to-Many with Through Models](many-to-many-through.md) - Using custom through models with M2M fields
6. [Forms Integration](forms-integration.md) - Building forms for hierarchical models
7. [Admin Integration](admin-integration.md) - Configuring the Django admin for hierarchical models
8. [Troubleshooting](troubleshooting.md) - Common issues and solutions
9. [API Reference](api-reference.md) - Detailed reference of all classes and methods

## Guides by Use Case

- [Simple Hierarchical Configuration](use-cases/simple-config.md)
- [Multi-tenant Configurations](use-cases/multi-tenant.md)
- [Permission Inheritance Systems](use-cases/permissions.md)
- [Feature Flag Systems](use-cases/feature-flags.md)
- [Hierarchical Settings](use-cases/settings.md)

## Contributing to Documentation

### Adding a New Page

1. Create a new Markdown file in the `docs` directory
2. Add the following front matter at the top of the file:

```markdown
---
layout: default
title: Your Page Title - Django Hierarchical Models
---

[Home](index.md) | 
[Getting Started](getting-started.md) | 
[Core Concepts](core-concepts.md) | 
[Basic Usage](basic-usage.md) | 
[API Reference](api-reference.md)

# Your Page Title
```

3. Link to your new page from the appropriate place in existing documentation

### Updating Documentation

The documentation is automatically built and deployed when changes are pushed to the `main` branch. To update documentation:

1. Make your changes to the Markdown files
2. Commit and push to the `main` branch
3. GitHub Actions will automatically build and deploy the updated documentation

## Local Development

To preview the documentation locally:

1. Install Jekyll and Bundler:
   ```bash
   gem install jekyll bundler
   ```

2. Navigate to the `docs` directory and run:
   ```bash
   bundle install
   bundle exec jekyll serve
   ```

3. Open your browser to http://localhost:4000