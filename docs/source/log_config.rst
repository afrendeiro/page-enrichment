Configuration and logging
*************************************

.. _Configuration:


Gene set libraries and configuration
====================================

``page`` uses gene sets from Enrichr gene set libraries.

Enrichment of a few is performed by default but this can be customizable by the
user.

The user can customize ``page`` in two ways:

* In a YAML file located in ``$HOME/.page.config.yaml``;
* At run time with through the ``gene_set_libraries`` option in the :func:`page.page` function.
* At run time with the ``-g`` or ``--gene-set-libraries`` option if using the command-line interface.

The YAML configuration file is entirely optional, but does allow
more flexibility and ease specically when selecting a large number of gene set
libraries (each with its own gene sets).

To see which gene set libraries are available, go to https://amp.pharm.mssm.edu/Enrichr/#stats.


``page`` does not need any static files with genes, but gets automatically what
is needed and keeps a cache of what has been used in order to save API calls and
greatly improve speed.

.. _Logging:

Logging
=============================

``page`` will log its operations and errors using the Python standard logging library.

This will happen by default to standard output (sys.stdout) but also to a file in ``$HOME/.page.log.txt``.

The location of the log file and the level of events to be reported can be customized in the ``page.setup_logger()`` function.
