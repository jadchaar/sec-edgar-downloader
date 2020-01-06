sec-edgar-downloader
====================

.. image:: https://github.com/jadchaar/sec-edgar-downloader/workflows/tests/badge.svg?branch=master
    :alt: Build Status
    :target: https://github.com/jadchaar/sec-edgar-downloader/actions?query=branch%3Amaster+workflow%3Atests

.. image:: https://codecov.io/gh/jadchaar/sec-edgar-downloader/branch/master/graph/badge.svg
    :alt: Coverage Status
    :target: https://codecov.io/gh/jadchaar/sec-edgar-downloader

.. image:: https://img.shields.io/pypi/v/sec-edgar-downloader.svg
    :alt: PyPI Version
    :target: https://python.org/pypi/sec-edgar-downloader

.. image:: https://img.shields.io/pypi/pyversions/sec-edgar-downloader.svg
    :alt: Supported Python Versions
    :target: https://python.org/pypi/sec-edgar-downloader

.. image:: https://img.shields.io/pypi/l/sec-edgar-downloader.svg
    :alt: License
    :target: https://python.org/pypi/sec-edgar-downloader

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style: Black
    :target: https://github.com/python/black

**sec-edgar-downloader** is a Python package for downloading `company filings <https://en.wikipedia.org/wiki/SEC_filing>`_ from the `SEC EDGAR database <https://www.sec.gov/edgar/searchedgar/companysearch.html>`_. Searches can be conducted either by `stock ticker <https://en.wikipedia.org/wiki/Ticker_symbol>`_ or `Central Index Key (CIK) <https://en.wikipedia.org/wiki/Central_Index_Key>`_. You can use the `SEC CIK lookup tool <https://www.sec.gov/edgar/searchedgar/cik.htm>`_ if you cannot find an appropriate ticker.

Quick Start
-----------

Installation
^^^^^^^^^^^^

Install and update this package using `pip <https://pip.pypa.io/en/stable/quickstart/>`_ or `pipenv <https://docs.pipenv.org/en/latest/>`_:

.. code-block:: console

    $ pip install -U sec-edgar-downloader

Example Usage
^^^^^^^^^^^^^

.. code-block:: python

    from sec_edgar_downloader import Downloader

    # Initialize a downloader instance.
    # If no argument is passed to the constructor, the package
    # will attempt to locate the user's downloads folder.
    dl = Downloader("/path/to/valid/save/location")

    # Get all 8-K filings for Apple (ticker: AAPL)
    dl.get("8-K", "AAPL")

    # Get all 8-K filings for Apple, including filing amends (8-K/A)
    dl.get("8-K", "AAPL", include_amends=True)

    # Get all 8-K filings for Apple after January 1, 2017 and before March 25, 2017
    # Note: before_date and after_date strings must be in the form "YYYYMMDD"
    dl.get("8-K", "AAPL", after_date="20170101", before_date="20170325")

    # Get the five most recent 8-K filings for Apple
    dl.get("8-K", "AAPL", 5)

    # Get all 10-K filings for Microsoft (ticker: MSFT)
    dl.get("10-K", "MSFT")

    # Get the latest 10-K filing for Microsoft
    dl.get("10-K", "MSFT", 1)

    # Get the latest 10KSB filing for Ubiquitech Software
    dl.get("10KSB", "0001411460", 1)

    # Get all 10-Q filings for Visa (ticker: V)
    dl.get("10-Q", "V")

    # Get all 13F-NT filings for the Vanguard Group (CIK: 0000102909)
    dl.get("13F-NT", "0000102909")

    # Get all 13F-HR filings for the Vanguard Group
    dl.get("13F-HR", "0000102909")

    # Get all SC 13G filings for Apple
    dl.get("SC 13G", "AAPL")

    # Get all SD filings for Apple
    dl.get("SD", "AAPL")

    # Get the latest supported filings, if available, for Apple
    for filing_type in dl.supported_filings:
        dl.get(filing_type, "AAPL", 1)

    # Get the latest supported filings, if available, for a
    # specified list of tickers and CIKs
    symbols = ["AAPL", "MSFT", "0000102909", "V", "FB"]
    for s in symbols:
        for filing_type in dl.supported_filings:
            dl.get(filing_type, s, 1)

Supported SEC Filings
---------------------

- 8-K
- 10-K
- 10KSB
- 10-Q
- 13F-NT and 13F-HR
- SC 13G
- SD
- S-1

You can learn more about the different types of SEC filings `here <https://www.investopedia.com/articles/fundamental-analysis/08/sec-forms.asp>`_.

Contributing
------------

If you encounter a bug or would like to see a new company filing or feature added to **sec-edgar-downloader**, please `file an issue <https://github.com/jadchaar/sec-edgar-downloader/issues>`_ or `submit a pull request <https://help.github.com/en/articles/creating-a-pull-request>`_.

Documentation
-------------

For full documentation, please visit `sec-edgar-downloader.readthedocs.io <https://sec-edgar-downloader.readthedocs.io>`_.
