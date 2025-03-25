from setuptools import setup, find_packages

# Define packages to include, excluding deprecated functionality
packages = find_packages(exclude=["*.tests.deprecated", "*.tests.deprecated.*"])

setup(
    name="djhierarchical",
    version="0.1.1",
    packages=packages,
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    author="Aibin Varghese",
    description="A Django app for hierarchical configuration models with automatic inheritance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aibin/djhierarchical",
    project_urls={
        "Bug Tracker": "https://github.com/aibin/djhierarchical/issues",
        "Documentation": "https://github.com/aibin/djhierarchical/tree/main/docs",
        "Source Code": "https://github.com/aibin/djhierarchical",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
) 