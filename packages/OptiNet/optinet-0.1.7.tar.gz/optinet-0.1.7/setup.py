from setuptools import setup, find_packages


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]
 

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="OptiNet",
    version="0.1.7",
    packages=['optima'], 
    install_requires= [],
    author="Vishwanath Akuthota ,Ganesh thota and Krishna Avula",
    description='OptiNet is a Python library for optimizing traditional machine learning models.',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify Markdown format

)

"""
# Clean up old files
rm -rf build/ dist/ OptiNet.egg-info

# Rebuild the package
python setup.py sdist bdist_wheel

# Upload the new package to PyPI
twine upload dist/*
"""
