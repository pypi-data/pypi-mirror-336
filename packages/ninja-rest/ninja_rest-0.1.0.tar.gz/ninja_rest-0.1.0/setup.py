from setuptools import setup, find_packages
import os

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ninja_rest",  # Changed to avoid potential name conflicts
    version="0.1.0",
    packages=find_packages(exclude=['examples*', 'tests*']),
    install_requires=[
        "django>=3.2",
        "django-ninja>=0.22.0",
        "pydantic>=2.0.0",
    ],
    author="Pradip Bankar",
    author_email="pradipbankar0097@gmail.com",
    description="A Django REST Framework-like package using Django Ninja",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pradip-v2/ninja_rest",
    project_urls={
        'Documentation': 'https://github.com/pradip-v2/ninja_rest',
        'Bug Reports': 'https://github.com/pradip-v2/ninja_rest/issues',
        'Source Code': 'https://github.com/pradip-v2/ninja_rest',
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='django, rest, api, django-ninja, viewsets',
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
