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

**sec-edgar-downloader** is a Python package for downloading `company filings <https://en.wikipedia.org/wiki/SEC_filing>`_ from the `SEC EDGAR database <https://www.sec.gov/edgar/searchedgar/companysearch.html>`_.
Searches can be conducted either by `stock ticker <https://en.wikipedia.org/wiki/Ticker_symbol>`_ or `Central Index Key (CIK) <https://en.wikipedia.org/wiki/Central_Index_Key>`_.
You can use the `SEC CIK lookup tool <https://www.sec.gov/edgar/searchedgar/cik.htm>`_ if you cannot find an appropriate ticker.

Quick Start
-----------

Installation
^^^^^^^^^^^^

Install and update this package using `pip <https://pip.pypa.io/en/stable/quickstart/>`_:

.. code-block:: console

    $ pip install -U sec-edgar-downloader

Basic Usage
^^^^^^^^^^^

.. code-block:: python

    from sec_edgar_downloader import Downloader

    # Initialize a downloader instance. If no argument is passed
    # to the constructor, the package will download filings to
    # the current working directory.
    dl = Downloader("/path/to/valid/save/location")

    # Get all 8-K filings for Apple (ticker: AAPL)
    dl.get("8-K", "AAPL")

    # Get all 8-K filings for Apple, including filing amends (8-K/A)
    dl.get("8-K", "AAPL", include_amends=True)

    # Get all 8-K filings for Apple after January 1, 2017 and before March 25, 2017
    # Note: after and before strings must be in the form "YYYY-MM-DD"
    dl.get("8-K", "AAPL", after="2017-01-01", before="2017-03-25")

    # Get the five most recent 8-K filings for Apple
    dl.get("8-K", "AAPL", amount=5)

    # Get all 10-K filings for Microsoft
    dl.get("10-K", "MSFT")

    # Get the latest 10-K filing for Microsoft
    dl.get("10-K", "MSFT", amount=1)

    # Get all 10-Q filings for Visa
    dl.get("10-Q", "V")

    # Get all 13F-NT filings for the Vanguard Group
    dl.get("13F-NT", "0000102909")

    # Get all 13F-HR filings for the Vanguard Group
    dl.get("13F-HR", "0000102909")

    # Get all SC 13G filings for Apple
    dl.get("SC 13G", "AAPL")

    # Get all SD filings for Apple
    dl.get("SD", "AAPL")

Advanced Usage
^^^^^^^^^^^^^^

.. code-block:: python

    from sec_edgar_downloader import Downloader

    # Download filings to the current working directory
    dl = Downloader()

    # Get all Apple proxy statements that contain the term "antitrust"
    dl.get("DEF 14A", "AAPL", query="antitrust")

    # Get all 10-K filings for Microsoft without the filing details
    dl.get("10-K", "MSFT", download_details=False)

    # Get the latest supported filings, if available, for Apple
    for filing_type in dl.supported_filings:
        dl.get(filing_type, "AAPL", amount=1)

    # Get the latest supported filings, if available, for a
    # specified list of tickers and CIKs
    equity_ids = ["AAPL", "MSFT", "0000102909", "V", "FB"]
    for equity_id in equity_ids:
        for filing_type in dl.supported_filings:
            dl.get(filing_type, equity_id, amount=1)

Supported SEC Filing Types
--------------------------

This package supports downloading all SEC filing types (6-K, 8-K, 10-K, DEF 14A, S-1, and many others).
You can learn more about the different SEC filing types `here <https://www.investopedia.com/articles/fundamental-analysis/08/sec-forms.asp>`_).
Below is an exhaustive list of all filings types that can be downloaded by this package:

- 1
- 1-A
- 1-A POS
- 1-A-W
- 1-E
- 1-E AD
- 1-K
- 1-SA
- 1-U
- 1-Z
- 1-Z-W
- 10-12B
- 10-12G
- 10-D
- 10-K
- 10-KT
- 10-Q
- 10-QT
- 11-K
- 11-KT
- 13F-HR
- 13F-NT
- 13FCONP
- 144
- 15-12B
- 15-12G
- 15-15D
- 15F-12B
- 15F-12G
- 15F-15D
- 18-12B
- 18-K
- 19B-4E
- 2-A
- 2-AF
- 2-E
- 20-F
- 20FR12B
- 20FR12G
- 24F-2NT
- 25
- 25-NSE
- 253G1
- 253G2
- 253G3
- 253G4
- 3
- 305B2
- 34-12H
- 4
- 40-17F1
- 40-17F2
- 40-17G
- 40-17GCS
- 40-202A
- 40-203A
- 40-206A
- 40-24B2
- 40-33
- 40-6B
- 40-8B25
- 40-8F-2
- 40-APP
- 40-F
- 40-OIP
- 40FR12B
- 40FR12G
- 424A
- 424B1
- 424B2
- 424B3
- 424B4
- 424B5
- 424B7
- 424B8
- 424H
- 425
- 485APOS
- 485BPOS
- 485BXT
- 486APOS
- 486BPOS
- 486BXT
- 487
- 497
- 497AD
- 497H2
- 497J
- 497K
- 5
- 6-K
- 6B NTC
- 6B ORDR
- 8-A12B
- 8-A12G
- 8-K
- 8-K12B
- 8-K12G3
- 8-K15D5
- 8-M
- 8F-2 NTC
- 8F-2 ORDR
- 9-M
- ABS-15G
- ABS-EE
- ADN-MTL
- ADV-E
- ADV-H-C
- ADV-H-T
- ADV-NR
- ANNLRPT
- APP NTC
- APP ORDR
- APP WD
- APP WDG
- ARS
- ATS-N
- ATS-N-C
- ATS-N/UA
- AW
- AW WD
- C
- C-AR
- C-AR-W
- C-TR
- C-TR-W
- C-U
- C-U-W
- C-W
- CB
- CERT
- CERTARCA
- CERTBATS
- CERTCBO
- CERTNAS
- CERTNYS
- CERTPAC
- CFPORTAL
- CFPORTAL-W
- CORRESP
- CT ORDER
- D
- DEF 14A
- DEF 14C
- DEFA14A
- DEFA14C
- DEFC14A
- DEFC14C
- DEFM14A
- DEFM14C
- DEFN14A
- DEFR14A
- DEFR14C
- DEL AM
- DFAN14A
- DFRN14A
- DOS
- DOSLTR
- DRS
- DRSLTR
- DSTRBRPT
- EFFECT
- F-1
- F-10
- F-10EF
- F-10POS
- F-1MEF
- F-3
- F-3ASR
- F-3D
- F-3DPOS
- F-3MEF
- F-4
- F-4 POS
- F-4MEF
- F-6
- F-6 POS
- F-6EF
- F-7
- F-7 POS
- F-8
- F-8 POS
- F-80
- F-80POS
- F-9
- F-9 POS
- F-N
- F-X
- FOCUSN
- FWP
- G-405
- G-405N
- G-FIN
- G-FINW
- IRANNOTICE
- MA
- MA-A
- MA-I
- MA-W
- MSD
- MSDCO
- MSDW
- N-1
- N-14
- N-14 8C
- N-14MEF
- N-18F1
- N-1A
- N-2
- N-23C-2
- N-23C3A
- N-23C3B
- N-23C3C
- N-2MEF
- N-30B-2
- N-30D
- N-4
- N-5
- N-54A
- N-54C
- N-6
- N-6F
- N-8A
- N-8B-2
- N-8F
- N-8F NTC
- N-8F ORDR
- N-CEN
- N-CR
- N-CSR
- N-CSRS
- N-MFP
- N-MFP1
- N-MFP2
- N-PX
- N-Q
- NO ACT
- NPORT-EX
- NPORT-NP
- NPORT-P
- NRSRO-CE
- NRSRO-UPD
- NSAR-A
- NSAR-AT
- NSAR-B
- NSAR-BT
- NSAR-U
- NT 10-D
- NT 10-K
- NT 10-Q
- NT 11-K
- NT 20-F
- NT N-CEN
- NT N-MFP
- NT N-MFP1
- NT N-MFP2
- NT NPORT-EX
- NT NPORT-P
- NT-NCEN
- NT-NCSR
- NT-NSAR
- NTFNCEN
- NTFNCSR
- NTFNSAR
- NTN 10D
- NTN 10K
- NTN 10Q
- NTN 20F
- OIP NTC
- OIP ORDR
- POS 8C
- POS AM
- POS AMI
- POS EX
- POS462B
- POS462C
- POSASR
- PRE 14A
- PRE 14C
- PREC14A
- PREC14C
- PREM14A
- PREM14C
- PREN14A
- PRER14A
- PRER14C
- PRRN14A
- PX14A6G
- PX14A6N
- QRTLYRPT
- QUALIF
- REG-NR
- REVOKED
- RW
- RW WD
- S-1
- S-11
- S-11MEF
- S-1MEF
- S-20
- S-3
- S-3ASR
- S-3D
- S-3DPOS
- S-3MEF
- S-4
- S-4 POS
- S-4EF
- S-4MEF
- S-6
- S-8
- S-8 POS
- S-B
- S-BMEF
- SC 13D
- SC 13E1
- SC 13E3
- SC 13G
- SC 14D9
- SC 14F1
- SC 14N
- SC TO-C
- SC TO-I
- SC TO-T
- SC13E4F
- SC14D1F
- SC14D9C
- SC14D9F
- SD
- SDR
- SE
- SEC ACTION
- SEC STAFF ACTION
- SEC STAFF LETTER
- SF-1
- SF-3
- SL
- SP 15D2
- STOP ORDER
- SUPPL
- T-3
- TA-1
- TA-2
- TA-W
- TACO
- TH
- TTW
- UNDER
- UPLOAD
- WDL-REQ
- X-17A-5

Contributing
------------

If you encounter a bug or would like to see a new company filing or feature added to **sec-edgar-downloader**, please `file an issue <https://github.com/jadchaar/sec-edgar-downloader/issues>`_ or `submit a pull request <https://help.github.com/en/articles/creating-a-pull-request>`_.

Documentation
-------------

For full documentation, please visit `sec-edgar-downloader.readthedocs.io <https://sec-edgar-downloader.readthedocs.io>`_.
