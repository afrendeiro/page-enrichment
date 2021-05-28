#!/usr/bin/env python

import sys
import os
from functools import lru_cache
import requests
import json
from typing import Union

import pandas as pd
from scipy import stats
from joblib import Memory

from page import _LOGGER, _CONFIG


class APIError(Exception):

    """Exception raised for errors communicating with an API."""


class EnrichrAPIError(APIError):

    """Exception raised for errors communicating with the Enrichr API."""


def page(
    parameter_vector: pd.Series, gene_set_libraries: Union[list, str] = None
) -> pd.DataFrame:
    """
    Parametric Analysis of Gene Set Enrichment (PAGE).

    Parameters
    ----------
    parameter_vector : :obj:`~pandas.Series`
        Pandas series with index as genes and values as 'parameters'
        (e.g. fold-changes, expression values)

    gene_set_libraries : :obj:`list`, optional
        Gene set libraries to use.
        Defaults to values in default configuration file or in
        ``~/.page.config.yaml``.
        To see all available values go to
        https://amp.pharm.mssm.edu/Enrichr/#stats

    Returns
    ----------
    :obj:`~pandas.DataFrame`
        Data frame with enrichment statistics for each term in each gene set library.
    """
    if gene_set_libraries is None:
        gene_set_libraries = _CONFIG["gene_set_libraries"]["enrichr"]
    if isinstance(gene_set_libraries, str):
        gene_set_libraries = [gene_set_libraries]

    results = dict()
    for lib in gene_set_libraries:
        gene_sets = get_library_genes(lib)

        _LOGGER.info(
            f"Performing PAGE for gene set library '{lib}' with {len(gene_sets)} gene sets."
        )
        for gs, genes in gene_sets.items():
            μ = parameter_vector.mean()
            δ = parameter_vector.std()
            Sm = parameter_vector.reindex(genes).mean()
            m = parameter_vector.shape[0]
            # Get Z-scores
            Z = (Sm - μ) * m ** (1 / 2) / δ
            # Get P-values
            p = stats.norm.sf(abs(Z)) * 2
            results[(lib, gs)] = [μ, δ, Sm, m, Z, p]
    return (
        pd.DataFrame(results, index=["μ", "δ", "Sm", "m", "Z", "p"])
        .T.sort_values("p")
        .rename_axis(index=["database", "term"])
    )


@lru_cache(maxsize=32)
def get_enrichr_libraries() -> list:
    resp = requests.get(f"{_CONFIG['base_enrichr_url']}/datasetStatistics")
    if not resp.ok:
        msg = "Could not get gene set libraries from Enrich!"
        raise EnrichrAPIError(msg)
    libs_json = json.loads(resp.text)
    return [lib["libraryName"] for lib in libs_json["statistics"]]


def _get_library_genes(lib) -> dict:
    resp = requests.get(
        f"{_CONFIG['base_enrichr_url']}/geneSetLibrary?mode=text&libraryName={lib}"
    )
    if not resp.ok:
        msg = f"Could not get gene set library '{lib}' from Enrich!"
        raise EnrichrAPIError(msg)
    terms = resp.text.split("\n")
    gs = dict()
    for t in terms:
        g = t.replace("\t\t", "\t").strip().split("\t")
        gs[g[0]] = g[1:]
    return gs


cache_dir = os.path.join(os.path.expanduser("~"), ".page")
memory = Memory(location=cache_dir, verbose=0)
get_library_genes = memory.cache(_get_library_genes)


def clear_memory() -> None:
    """
    Clear the persistent memory of the function getting gene sets from Enrichr.
    """
    memory.clear()


def main(cli: str = None) -> int:
    """
    Interface for CLI usage of PAGE.

    Parameters
    ----------
    cli : :obj:`str`, optional
        A string representing the CLI call.

    Returns
    ----------
    :obj:`int`
        Return code of whole process.

    """
    from argparse import ArgumentParser

    parser = ArgumentParser()

    _help = (
        "Two-column CSV input file for enrichment. "
        "The first column are gene names and the second the 'parameters' "
        "(e.g. fold-changes). Assumes header."
    )
    parser.add_argument(dest="input_file", help=_help)
    _help = "Output CSV file with enrichment results."
    parser.add_argument(dest="output_file", help=_help)
    _help = (
        "Enrichr gene set libraries to use, comma-delimited. "
        "Check 'http://amp.pharm.mssm.edu/Enrichr/datasetStatistics' to see all"
        "available. Defaults to the app's defaults or to a user-specified "
        "configuration in ~/.page.config.yaml. "
        "See  for example."
    )
    parser.add_argument(
        "-g", "--gene-set-libraries", dest="gene_set_libraries", help=_help
    )
    args = parser.parse_args(cli)

    _LOGGER.info(f"Reading input CSV file '{args.input_file}'.")
    v = pd.read_csv(args.input_file, index_col=0, squeeze=True)
    _LOGGER.info(f"Found file with {v.shape[0]} genes.")

    if args.gene_set_libraries is not None:
        args.gene_set_libraries = args.gene_set_libraries.split(",")
    else:
        _LOGGER.debug(f"No gene set libraries given, using default.")
        args.gene_set_libraries = _CONFIG["gene_set_libraries"]["enrichr"]
    gs = "\n\t- ".join(args.gene_set_libraries)
    _LOGGER.info(f"Using gene set libraries:\n\t- {gs}")

    res = page(v, args.gene_set_libraries)
    _LOGGER.info(f"Completed.")

    _LOGGER.info(f"Saving to output CSV file '{args.output_file}'.")
    res.to_csv(args.output_file)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
