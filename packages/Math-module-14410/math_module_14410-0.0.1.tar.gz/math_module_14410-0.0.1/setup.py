from setuptools import find_packages, setup

with open("README.md") as file:
    desc = file.read()

setup(
    name="Math_module_14410",
    version="0.0.1",
    description="A test python package for class assignment",
    long_description=desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)