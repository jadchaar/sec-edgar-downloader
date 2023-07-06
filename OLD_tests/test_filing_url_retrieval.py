"""Tests the filing URLs to download for each filing type."""
from datetime import date

import pytest

from sec_edgar_downloader import Downloader
from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS
from sec_edgar_downloader._utils import EdgarSearchApiError, get_filing_urls_to_download


def test_large_number_of_filings(formatted_earliest_after_date):
    filing_type = "8-K"
    ticker = "AAPL"
    before_date = date(2019, 11, 15).strftime(DATE_FORMAT_TOKENS)
    include_amends = False

    # num_filings_to_download < number of filings available
    num_filings_to_download = 100
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
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
        formatted_earliest_after_date,
        before_date,
        include_amends,
    )
    assert len(filings_to_download) == 150

    # SEC Edgar Search fails to retrieve Apple 8-Ks after 2000 and before 2002
    formatted_earliest_after_date = date(2002, 1, 1).strftime(DATE_FORMAT_TOKENS)

    # num_filings_to_download > number of filings available
    num_filings_to_download = 200
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
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
        formatted_earliest_after_date,
        before_date,
        include_amends,
    )
    # there are 158 AAPL 8-K filings before 2019-11-15
    assert len(filings_to_download) == 158


@pytest.mark.parametrize(
    "filing_type", ["4", "8-K", "10-K", "10-Q", "SC 13G", "SD", "DEF 14A"]
)
def test_common_filings(
    filing_type, formatted_earliest_after_date, formatted_latest_before_date
):
    # AAPL files 4, 8-K, 10-K, 10-Q, SC 13G, SD, DEF 14A
    ticker = "AAPL"
    num_filings_to_download = 1
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
        formatted_latest_before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


@pytest.mark.parametrize("filing_type", ["13F-NT", "13F-HR"])
def test_13f_filings(
    filing_type, formatted_earliest_after_date, formatted_latest_before_date
):
    # Vanguard files 13F-NT, 13F-HR
    ticker = "0000102909"
    num_filings_to_download = 1
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
        formatted_latest_before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


def test_10ksb_filings(formatted_earliest_after_date, formatted_latest_before_date):
    # Ubiquitech files 10KSB
    ticker = "0001411460"
    filing_type = "10KSB"
    num_filings_to_download = 1
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
        formatted_latest_before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


def test_s1_filings(formatted_earliest_after_date, formatted_latest_before_date):
    # Cloudflare filed an S-1 during its IPO
    ticker = "NET"
    filing_type = "S-1"
    num_filings_to_download = 1
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
        formatted_latest_before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


def test_20f_filings(formatted_earliest_after_date, formatted_latest_before_date):
    # Alibaba files 20-F
    ticker = "BABA"
    filing_type = "20-F"
    num_filings_to_download = 1
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
        formatted_latest_before_date,
        include_amends,
    )
    assert len(filings_to_download) == 1


@pytest.mark.parametrize("filing_type", Downloader.supported_filings)
def test_all_supported_filings(
    filing_type, formatted_earliest_after_date, formatted_latest_before_date
):
    ticker = "AAPL"
    num_filings_to_download = 1
    include_amends = False

    try:
        filings_to_download = get_filing_urls_to_download(
            filing_type,
            ticker,
            num_filings_to_download,
            formatted_earliest_after_date,
            formatted_latest_before_date,
            include_amends,
        )
    except EdgarSearchApiError:
        pytest.fail(f"EdgarSearchApiError was raised for {filing_type} filing.")
    else:
        # AAPL may or may not file certain filings
        assert len(filings_to_download) == 0 or len(filings_to_download) == 1


def test_fetch_zero_filings(
    formatted_earliest_after_date, formatted_latest_before_date
):
    ticker = "AAPL"
    filing_type = "8-K"
    num_filings_to_download = 0
    include_amends = False

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        formatted_earliest_after_date,
        formatted_latest_before_date,
        include_amends,
    )
    assert len(filings_to_download) == 0


def test_search_api_error_handling(formatted_latest_before_date):
    ticker = "AAPL"
    filing_type = "8-K"
    num_filings_to_download = 1
    include_amends = False
    # Edgar Search API requires a date in the format YYYY-MM-DD
    invalid_before_date = "20090827"

    with pytest.raises(EdgarSearchApiError):
        get_filing_urls_to_download(
            filing_type,
            ticker,
            num_filings_to_download,
            invalid_before_date,
            formatted_latest_before_date,
            include_amends,
        )
