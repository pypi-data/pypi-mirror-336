from setuptools import setup, find_packages

setup(
    name="SPEARS",                  
    version="2.0.0",              
    packages=find_packages(),      
    include_package_data=True,    
    package_data={
        "SPEARS": ["data/*.json"],
    },
    # Optional additional metadata
    author="Justin Domagala-Tang",
    url="https://pypi.org/project/SPEARS/",  # Example
)
