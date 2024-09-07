#!/usr/bin/env python
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pallapay-python-sdk",
    version="1.0.0",
    author="Pallapay",
    author_email="info@pallapay.com",
    description="Pallapay Python SDK to accept crypto currency payments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pallapay/pallapay-python-sdk",
    license="MIT",
    keywords='pallapay bitcoin crypto payment gateway client',
    install_requires=[
        'requests==2.28.1',
        'pydantic==1.9.2'
    ],
    project_urls={
        "Bug Tracker": "https://github.com/pallapay/pallapay-python-sdk/issues",
        "Documentation": "https://github.com/pallapay/pallapay-python-sdk",
        "repository": "https://github.com/pallapay/pallapay-python-sdk"
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",

    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
