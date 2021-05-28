#! /usr/bin/env python

import sys


def parse_requirements(req_file):
    requirements = open(req_file).read().strip().split("\n")
    requirements = [r for r in requirements if not r.startswith("#")]
    return [r for r in requirements if "#egg=" not in r]


# take care of extra required modules depending on Python version
extra = {}
try:
    from setuptools import setup, find_packages

    if sys.version_info < (2, 7):
        extra["install_requires"] = ["argparse"]
    if sys.version_info >= (3,):
        extra["use_2to3"] = True
except ImportError:
    from distutils.core import setup

    if sys.version_info < (2, 7):
        extra["dependencies"] = ["argparse"]

# Requirements
requirements = parse_requirements("requirements/requirements.txt")
requirements_test = parse_requirements("requirements/requirements.test.txt")
requirements_docs = parse_requirements("requirements/requirements.docs.txt")

long_description = open("README.md").read()


# setup
setup(
    name="page-enrichment",
    packages=find_packages(),
    use_scm_version={
        "write_to": "page/_version.py",
        "write_to_template": '__version__ = "{version}"\n',
    },
    entry_points={
        "console_scripts": [
            "page = page.enrichment:main",
            "page-get-test-data = page.tests:get_test_data",
        ]
    },
    description="Parametric Analysis of Gene Set Enrichment (PAGE).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: " "GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="bioinformatics, genetics, enrichement analysis",
    url="https://github.com/afrendeiro/page-enrichment",
    project_urls={
        "Bug Tracker": "https://github.com/afrendeiro/page-enrichment/issues",
        "Documentation": "https://page-enrichment.readthedocs.io",
        "Source Code": "https://github.com/afrendeiro/page-enrichment",
    },
    author=u"Andre Rendeiro",
    author_email="andre.rendeiro@pm.me",
    license="GPL3",
    setup_requires=["setuptools_scm"],
    install_requires=requirements,
    tests_require=requirements_test,
    extras_require={"testing": requirements_test, "docs": requirements_docs},
    package_data={"page": ["config/*.yaml", "templates/*.html"]},
    data_files=[
        "requirements/requirements.txt",
        "requirements/requirements.test.txt",
    ],
    **extra
)
