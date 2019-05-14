# sec-edgar-downloader

[![Build Status](https://travis-ci.org/jadchaar/sec-edgar-downloader.svg?branch=master)](https://travis-ci.org/jadchaar/sec-edgar-downloader)
[![codecov](https://codecov.io/gh/jadchaar/sec-edgar-downloader/branch/master/graph/badge.svg)](https://codecov.io/gh/jadchaar/sec-edgar-downloader)
[![image](https://img.shields.io/pypi/v/sec-edgar-downloader.svg)](https://python.org/pypi/sec-edgar-downloader)
[![image](https://img.shields.io/pypi/pyversions/sec-edgar-downloader.svg)](https://python.org/pypi/sec-edgar-downloader)
[![image](https://img.shields.io/pypi/l/sec-edgar-downloader.svg)](https://python.org/pypi/sec-edgar-downloader)

Python package for downloading company filings from the [SEC EDGAR database](https://www.sec.gov/edgar/searchedgar/companysearch.html). Searches can be conducted either by [stock ticker](https://en.wikipedia.org/wiki/Ticker_symbol) or Central Index Key (CIK). You can use the [SEC CIK lookup tool](https://www.sec.gov/edgar/searchedgar/cik.htm) if you cannot find an appropriate ticker. Supported company filings: 8-K, 10-K, 10-Q, 13F-NT, 13F-HR, SC 13G, SD. Learn more about the different types of SEC filings [here](https://www.investopedia.com/articles/fundamental-analysis/08/sec-forms.asp).

## Installation

Install and update this package using [pip](https://pip.pypa.io/en/stable/quickstart/):

`pip install -U sec-edgar-downloader`

## Example usage

```python
from sec_edgar_downloader import Downloader

# Initialize a downloader instance.
# If no argument is passed to the constructor, the package
# will attempt to locate the user's downloads folder.
dl = Downloader("/path/to/valid/save/location")

# Get all 8-K filings for Apple (ticker: AAPL)
dl.get_8k_filings("AAPL")

# Get the past 5 8-K filings for Apple
dl.get_8k_filings("AAPL", 5)

# Get all 10-K filings for Microsoft (ticker: MSFT)
dl.get_10k_filings("MSFT")

# Get the latest 10-K filing for Microsoft
dl.get_10k_filings("MSFT", 1)

# Get all 10-Q filings for Visa (ticker: V)
dl.get_10q_filings("V")

# Get all 13F-NT filings for Vanguard Group (CIK: 0000102909)
dl.get_13f_nt_filings("0000102909")

# Get all 13F-HR filings for Vanguard Group
dl.get_13f_hr_filings("0000102909")

# Get all SC 13G filings for Apple
dl.get_sc_13g_filings("AAPL")

# Get all SD filings for Apple
dl.get_sd_filings("AAPL")

# Get all the latest filings (8-K, 10-K, 10-Q, 13F, SC 13G, SD), if available, for Apple
dl.get_all_available_filings("AAPL", 1)

# Get all the latest filings (8-K, 10-K, 10-Q, 13F, SC 13G, SD), if available,
# for a specified list of tickers and CIKs
identifiers = ["AAPL", "MSFT", "0000102909", "V", "FB"]
for id in identifiers:
    dl.get_all_available_filings(id, 1)
```
