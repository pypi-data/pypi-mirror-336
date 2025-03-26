from setuptools import find_packages, setup

with open("README.md") as file:
    desc = file.read()

setup(
    name="python_package_14721",
    version="0.0.2",
    description="A test python package for class assignment",
    long_description=desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)