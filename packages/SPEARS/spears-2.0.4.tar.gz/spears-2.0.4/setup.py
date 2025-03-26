from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SPEARS",
    version="2.0.4",
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
    install_requires=[
        "requests",                  # likely required by sparcl
        "sparclclient",                    # your custom or external dependency
        "specutils>=1.0",            # for Spectrum1D and find_lines_derivative
        "astropy>=5.0",              # for units, table, fits, etc.
        "scipy>=1.7",                # for median_filter
        "numpy>=1.21",               # for numerical operations
        "alive-progress",           # for alive_bar
        "matplotlib>=3.0",          # for plotting
    ],
    python_requires=">=3.7",
)