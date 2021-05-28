#!/usr/bin/env python


import os

import pytest
import pandas as pd

from page.tests import get_diff_expression_vector


# Environment-specific
CI: bool = ("TRAVIS" in os.environ) or ("GITHUB_WORKFLOW" in os.environ)
CI_NAME = None
BUILD_DIR: str = os.path.abspath(os.path.curdir)
DEV: bool

if CI:
    if "TRAVIS" in os.environ:
        CI_NAME = "TRAVIS"
        BUILD_DIR = os.environ["TRAVIS_BUILD_DIR"]
    elif "GITHUB_WORKFLOW" in os.environ:
        CI_NAME = "GITHUB"
        BUILD_DIR = os.path.join("home", "runner", "work", "toolkit", "toolkit")

try:
    DEV = os.environ["TRAVIS_BRANCH"] == "dev"
except KeyError:
    pass
try:
    DEV = os.environ["GITHUB_REF"] == "dev"
except KeyError:
    import subprocess

    o = subprocess.check_output("git status".split(" "))
    DEV = "dev" in o.decode().split("\n")[0]


def file_exists_and_not_empty(file: str) -> bool:
    return os.path.exists(file) and (os.stat(file).st_size > 0)


@pytest.fixture
def diff_expression_vector():
    return get_diff_expression_vector()
