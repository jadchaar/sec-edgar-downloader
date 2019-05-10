# sec-edgar-downloader

[![Build Status](https://travis-ci.org/jadchaar/sec-edgar-downloader.svg?branch=master)](https://travis-ci.org/jadchaar/sec-edgar-downloader)
[![image](https://img.shields.io/pypi/v/sec-edgar-downloader.svg)](https://python.org/pypi/sec-edgar-downloader)
[![image](https://img.shields.io/pypi/pyversions/sec-edgar-downloader.svg)](https://python.org/pypi/sec-edgar-downloader)
[![image](https://img.shields.io/pypi/l/sec-edgar-downloader.svg)](https://python.org/pypi/sec-edgar-downloader)

Python module for bulk downloading company filings from the [SEC EDGAR database](https://www.sec.gov/edgar/searchedgar/companysearch.html). Searches can be conducted either by [stock ticker](https://en.wikipedia.org/wiki/Ticker_symbol) or Central Index Key (CIK). You can use the SEC [CIK Lookup](https://www.sec.gov/edgar/searchedgar/cik.htm) tool if you cannot find an appropriate ticker. Supported company filings: 8-K, 10-K, 10-Q, 13-F, SC 13G, SD. Learn more about the different types of SEC filings [here](https://www.investopedia.com/articles/fundamental-analysis/08/sec-forms.asp).

## Installation
Install and update this package using [pip](https://pip.pypa.io/en/stable/quickstart/):

`pip install -U sec-edgar-downloader`

## Example usage

```python
import sec_edgar_downloader

# Initialize the downloader object
# If no argument is passed to the constructor, the
# package attempts to find the user's Downloads folder
downloader = sec_edgar_downloader.Downloader("/path/to/download/destination")

# Get all 8-K filings for Apple (Ticker: AAPL)
downloader.get_8k_filing_for_ticker("AAPL")

# Get the past 5 8-K filings for Apple (Ticker: AAPL)
downloader.get_8k_filing_for_ticker("AAPL", 5)

# Get all 10-K filings for Microsoft (Ticker: MSFT)
downloader.get_10k_filing_for_ticker("MSFT")

# Get the latest 10-K filing for Microsoft (Ticker: MSFT)
downloader.get_10k_filing_for_ticker("MSFT", 1)

# Get all 10-Q filings for Visa (Ticker: V)
downloader.get_10q_filing_for_ticker("V")

# Get all 13F filings for Vanguard Group Inc (CIK: 0000102909)
downloader.get_13f_filing_for_cik("0000102909")

# Get all SC 13G filings for Apple (Ticker: AAPL)
downloader.get_sc_13g_filing_for_ticker("AAPL")

# Get all SD filings for Apple (Ticker: AAPL)
downloader.get_sd_filing_for_ticker("AAPL")

# Get all filings (8-K, 10-K, 10-Q, 13F, SC 13G, SD), if available, for Apple (Ticker: AAPL)
downloader.get_all_available_filings_for_ticker("AAPL")

# Get all filings (8-K, 10-K, 10-Q, 13F, SC 13G, SD), if available, for a specified list of tickers
downloader.get_all_available_filings_for_ticker_list(["AAPL", "MSFT", "V", "FB"])
```
