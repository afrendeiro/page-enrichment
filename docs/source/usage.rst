Quick usage
=============================

Using the command-line interface (CLI)
--------------------------------------------------

``page`` has a CLI for easy usage:

.. code-block:: bash

    $ page-get-test-data test.csv
    $ page -g KEGG_2016 test.csv output.csv


Interactive usage through the API
---------------------------------

Example usage of the :func:`page.page` function:

.. code-block:: python

    from page import page, get_test_data

    vect = get_test_data()
    results = page(vect, gene_set_libraries=['KEGG_2016'])


The :func:`page.get_test_data` function serves simply the purpose of getting a
vector of fold-changes to use with PAGE.
