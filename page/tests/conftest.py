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


def file_exists_and_not_empty(file):
    return os.path.exists(file) and (os.stat(file).st_size > 0)


def get_diff_expression_vector():
    url = (
        "https://amp.pharm.mssm.edu/Harmonizome/"
        "api/1.0/gene_set/"
        "Androgen+insensitivity+syndrome_Fibroblast_GSE3871/"
        "GEO+Signatures+of+Differentially+Expressed+Genes+for+Diseases"
    )
    resp = requests.get(url)
    if not resp.ok:
        raise APIError("Could not get test differential expression vector.")

    vect = dict()
    for gene in resp.json()["associations"]:
        vect[gene["gene"]["symbol"]] = gene["standardizedValue"]
    return pd.Series(vect).sort_values()


@pytest.fixture
def diff_expression_vector():
    return get_diff_expression_vector()


def get_test_data(cli: str = None) -> int:
    from argparse import ArgumentParser

    parser = ArgumentParser()
    _help = "Output CSV file with fold-changes."
    parser.add_argument(dest="output_file", help=_help)
    args = parser.parse_args(cli)

    vect = get_diff_expression_vector()
    vect.to_csv(args.output_file, header=True)
