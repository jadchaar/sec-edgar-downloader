"""Tests the filing URLs to download for each filing type."""
from datetime import date

import pytest

from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS
from sec_edgar_downloader._utils import get_filing_urls_to_download


def test_large_number_of_filings():
    filing_type = "8-K"
    ticker = "AAPL"
    after_date = None
    before_date = date(2019, 11, 15).strftime(DATE_FORMAT_TOKENS)
    include_amends = False

    # num_filings_to_download < number of filings available
    num_filings_to_download = 100
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 100

    # fetch filing URLs over two pages, but retrieve
    # fewer than the total number of filings available
    num_filings_to_download = 150
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 150

    # SEC Edgar Search fails to retrieve Apple 8-Ks after 2000 and before 2002
    after_date = date(2002, 1, 1).strftime(DATE_FORMAT_TOKENS)

    # num_filings_to_download > number of filings available
    num_filings_to_download = 200
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    # there are 158 AAPL 8-K filings before 2019-11-15 and after 2002-01-01
    assert len(filings_to_download) == 158

    # num_filings_to_download == number of filings available
    num_filings_to_download = 158
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    # there are 158 AAPL 8-K filings before 2019-11-15
    assert len(filings_to_download) == 158


@pytest.mark.parametrize(
    "filing_type", ["4", "8-K", "10-K", "10-Q", "SC 13G", "SD", "DEF 14A"]
)
def test_common_filings(filing_type):
    # AAPL files 4, 8-K, 10-K, 10-Q, SC 13G, SD, DEF 14A
    ticker = "AAPL"
    num_filings_to_download = 1
    after_date = None
    before_date = None
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


@pytest.mark.parametrize("filing_type", ["13F-NT", "13F-HR"])
def test_13f_filings(filing_type):
    # Vanguard files 13F-NT, 13F-HR
    ticker = "0000102909"
    num_filings_to_download = 1
    after_date = None
    before_date = None
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


def test_10ksb_filings():
    # Ubiquitech files 10KSB
    ticker = "0001411460"
    filing_type = "10KSB"
    num_filings_to_download = 1
    after_date = None
    before_date = None
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


def test_s1_filings():
    # Cloudflare filed an S-1 during its IPO
    ticker = "NET"
    filing_type = "S-1"
    num_filings_to_download = 1
    after_date = None
    before_date = None
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


def test_20f_filings():
    # Alibaba files 20-F
    ticker = "BABA"
    filing_type = "20-F"
    num_filings_to_download = 1
    after_date = None
    before_date = None
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1
