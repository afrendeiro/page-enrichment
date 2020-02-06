#!/usr/bin/env python


# import numpy as np
import pytest

from page import page
from page import APIError
from page.page import _get_library_genes


class TestPAGE:
    def test_analysis_representation(self, diff_expression_vector):
        r = page(diff_expression_vector, ['KEGG_2016'])
        assert r.shape == (294, 6)
        assert r.dropna().shape == (247, 6)
        # assert r.query('p < 0.001').shape[0] == 77
        # assert np.allclose(r.sort_values(list(r.columns[::-1].values)).iloc[0]['Z'], 8.316086)

    def test_get_wrong_gene_set(self):
        with pytest.raises(APIError):
            _get_library_genes("WRONG_GENE_SET_NAME")
