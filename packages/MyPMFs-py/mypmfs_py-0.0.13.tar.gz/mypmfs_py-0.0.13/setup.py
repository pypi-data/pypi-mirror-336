from setuptools import setup, find_packages
from os import path, chmod

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding = 'utf-8') as f:
    long_description = f.read()

setup(
    name = "MyPMFs_py",
    version = "0.0.13",
    author="Alexander Holden",
    author_email = "alexholden645@gmail.com",
    description = "Python package for mypmfs training(includes batch download from PDB)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    include_package_data=True,
    package_data={"MyPMFs_py" : ["bin/training", "bin/batch_download.sh", "bin/scoring"]},
)