#!/usr/bin/env python


import os
import pandas as pd

# import numpy as np
import pytest

from page import page, get_enrichr_libraries
from page import APIError
from page import get_library_genes
from .conftest import file_exists_and_not_empty


class TestPAGE:
    def test_analysis_representation(self, diff_expression_vector):
        r = page(diff_expression_vector, ["KEGG_2016"])
        assert r.shape == (294, 6)
        assert r.dropna().shape == (247, 6)
        # assert r.query('p < 0.001').shape[0] == 77
        # assert np.allclose(r.sort_values(list(r.columns[::-1].values)).iloc[0]['Z'], 8.316086)

    def test_get_wrong_gene_set(self):
        with pytest.raises(APIError):
            get_library_genes("WRONG_GENE_SET_NAME")

    def test_get_enrichr_libraries(self):
        libs = get_enrichr_libraries()
        assert len(libs) > 150

    def test_cli(self):
        os.system("page-get-test-data input.csv")
        assert file_exists_and_not_empty("input.csv")
        os.system("page -g KEGG_2016 input.csv output.csv")
        assert file_exists_and_not_empty("output.csv")

        r = pd.read_csv("output.csv", index_col=[0, 1])
        assert r.shape == (294, 6)
        assert r.dropna().shape == (247, 6)
