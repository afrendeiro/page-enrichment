Configuration, logging and versioning
*************************************

.. _Configuration:


Configuration of gene set libraries
===================================

``page`` uses a YAML configuration file.

While entirely optional, this allows the user to easily specify their preferences.

The user can provide its own configuration in two ways:

* In a YAML file located in ``$HOME/.page.config.yaml``;
* At run time with through the ``gene_set_libraries`` option in the :func:`page.page` function.
* At run time with the ``-g`` or ``--gene-set-libraries`` option if using the command-line interface.

To see how to structure the YAML file, see section below.

.. _Logging:

Logging
=============================

``page`` will log its operations and errors using the Python standard logging library.

This will happen by default to standard output (sys.stdout) but also to a file in ``$HOME/.page.log.txt``.

The location of the log file and the level of events to be reported can be customized in the ``page.setup_logger()`` function.
