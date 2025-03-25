"""Setup script for the package."""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-doctools",
    version="0.1.0",
    packages=find_packages(exclude=["*_tests", "tests", "tests.*"]),
    include_package_data=True,
    description="A Django app for AI-powered document processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anshuman Saagar",
    author_email="anshuman@mobiux.in",
    url="https://github.com/yourusername/django-doctools",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "Django>=4.0",
        "python-docx>=1.1.2",
        "pydantic>=2.10.6",
        "boto3>=1.37.17",
        "pymupdf>=1.25.4",
        "pillow>=11.1.0",
        "boto3>=1.37.16",
    ],
)
