#!/usr/bin/env python


import os
import requests

import pandas as pd
import pytest

from page import APIError


# Environment-specific
CI: bool = ("TRAVIS" in os.environ) or ("GITHUB_WORKFLOW" in os.environ)
CI_NAME = None
BUILD_DIR: str = os.path.abspath(os.path.curdir)
DEV: bool

if CI:
    if "TRAVIS" in os.environ:
        CI_NAME = "TRAVIS"
        BUILD_DIR = os.environ['TRAVIS_BUILD_DIR']
    elif "GITHUB_WORKFLOW" in os.environ:
        CI_NAME = "GITHUB"
        BUILD_DIR = os.path.join(
            "home", "runner", "work", "toolkit", "toolkit")

try:
    DEV = os.environ['TRAVIS_BRANCH'] == 'dev'
except KeyError:
    pass
try:
    DEV = os.environ['GITHUB_REF'] == 'dev'
except KeyError:
    import subprocess
    o = subprocess.check_output("git status".split(" "))
    DEV = "dev" in o.decode().split("\n")[0]


def is_internet_connected(hostname="www.google.com"):
    import socket
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except OSError:
        pass
    return False


def has_module(module):
    import importlib
    try:
        importlib.import_module(module)
        return True
    except ModuleNotFoundError:
        return False


def file_exists(file):
    from page.utils import get_this_file_or_timestamped

    return os.path.exists(get_this_file_or_timestamped(file))


def file_not_empty(file):
    from page.utils import get_this_file_or_timestamped

    return os.stat(get_this_file_or_timestamped(file)).st_size > 0


def file_exists_and_not_empty(file):
    from page.utils import get_this_file_or_timestamped

    f = get_this_file_or_timestamped(file)

    return os.path.exists(f) and (
        os.stat(f).st_size > 0)


@pytest.fixture
def diff_expression_vector():
    url = (
        "https://amp.pharm.mssm.edu/Harmonizome/"
        "api/1.0/gene_set/"
        "Androgen+insensitivity+syndrome_Fibroblast_GSE3871/"
        "GEO+Signatures+of+Differentially+Expressed+Genes+for+Diseases")
    resp = requests.get(url)
    if not resp.ok:
        raise APIError("Could not get test differential expression vector.")

    vect = dict()
    for gene in resp.json()['associations']:
        vect[gene['gene']['symbol']] = gene['standardizedValue']
    return pd.Series(vect).sort_values()
