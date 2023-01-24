#!/usr/bin/env python
import sys

from setuptools import setup, find_packages


def read_file(name):
    """
    Read file content
    """
    f = open(name)
    try:
        return f.read()
    except IOError:
        print("could not read %r" % name)
        f.close()

LONG_DESC = read_file('README.md') + '\n\n' + read_file('HISTORY.md')

EXTRAS = {}

if sys.version_info < (3,):
    EXTRAS['use_2to3'] = True

setup(
    name='pytest-expectdir',
    version='1.1.0',
    description='A pytest plugin to provide initial/expected directories, and check a test transforms the initial directory to the expected one',
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
    author='Léo Falventin Hauchecorne',
    author_email='hl037.prog@gmail.com',
    url='https://github.com/hl037/pytest-expectdir',
    license='MIT',
    packages=find_packages(),
    test_suite=None,
    include_package_data=True,
    zip_safe=False,
    install_requires=['pytest>=5.0'],
    extras_require=None,
    entry_points={
      "pytest11": ["pytest-expectdir = pytest_expectdir.plugin"],
    },
    keywords="pytest test unittest directory file",
    python_requires=">=3.7",
    classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Topic :: Software Development :: Quality Assurance",
      "Topic :: Software Development :: Testing",
    ],
    **EXTRAS
)
