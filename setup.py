import os
from setuptools import setup, find_packages


def read(*paths):
    """Read the contents of a text file safely.
    >>> read("dundie", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """
    rootpath = os.path.dirname(__file__)
    filepath = os.path.join(rootpath, *paths)
    with open(filepath) as file_:
        return file_.read().strip()


setup(
    name="dataclass_validator",
    version="0.1.0",
    description="Dataclass validation tools",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Bruno Rocha",
    python_requires=">=3.8",
    packages=["dataclass_validator"],
    include_package_data=True,
)
