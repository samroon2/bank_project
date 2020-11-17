import sys
from setuptools import setup, find_packages, find_namespace_packages
from setuptools.command.install import install
import distutils.command.install as dist_inst

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="bank",
    version="0.0.1",
    description="Bank task.",
    packages=find_namespace_packages(),
    python_requires=">=3.6.1",
)
