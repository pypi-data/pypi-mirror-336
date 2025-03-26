from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SPEARS",
    version="2.0.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "SPEARS": ["data/*.json"],
    },
    author="Justin Domagala-Tang",
    url="https://pypi.org/project/SPEARS/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
