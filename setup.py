'''
Typical installation is via:

    python setup.py develop

For further information, see the README.
'''

import os
import runpy
from setuptools import setup, find_packages

# Get version
cwd = os.path.abspath(os.path.dirname(__file__))
versionpath = os.path.join(cwd, 'datathief', 'version.py')
version = runpy.run_path(versionpath)['__version__']

# Get the documentation
with open(os.path.join(os.getcwd(), 'README.rst'), "r") as fh:
    long_description = fh.read()

CLASSIFIERS = [
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3.8",
]

setup(
    name="datathief",
    version=version,
    author="Cliff Kerr",
    author_email="info@sciris.org",
    description="Simple utility for extracting data from images",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/sciris/datathief',
    keywords=['data', 'image' 'extraction', 'thievery'],
    platforms=["OS Independent"],
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'matplotlib',
        'sciris',
        ]
)

