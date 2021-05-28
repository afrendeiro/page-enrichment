#!/usr/bin/env python

import requests
import pandas as pd

from page import APIError


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
    return (
        pd.Series(vect, name="Androgen_insensitivity_syndrome_Fibroblast_GSE3871")
        .sort_values()
        .rename_axis("gene")
    )


def get_test_data(cli: str = None) -> int:
    from argparse import ArgumentParser

    parser = ArgumentParser()
    _help = "Output CSV file with fold-changes."
    parser.add_argument(dest="output_file", help=_help)
    args = parser.parse_args(cli)

    vect = get_diff_expression_vector()
    vect.to_csv(args.output_file, header=True)
    return 0
