"""Tests the behavior and error handling of the Downloader
in the presence of abnormal and malformed user input.
"""

from datetime import datetime

import pytest


def test_num_filings_to_download_argument(downloader, apple_filing_metadata):
    dl, _ = downloader
    expected_msg = (
        "Please enter a number greater than 1 for the number of filings to download."
    )

    with pytest.raises(ValueError) as excinfo:
        num_downloaded = dl.get_8k_filings(apple_filing_metadata["symbol"], -1)
    assert expected_msg in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        num_downloaded = dl.get_8k_filings(apple_filing_metadata["symbol"], "-1")
    assert expected_msg in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        num_downloaded = dl.get_8k_filings(apple_filing_metadata["symbol"], 0)
    assert expected_msg in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        num_downloaded = dl.get_8k_filings(apple_filing_metadata["symbol"], 0.9)
    assert expected_msg in str(excinfo.value)

    num_downloaded = dl.get_8k_filings(apple_filing_metadata["symbol"], 2.9)
    assert num_downloaded == 2


def test_ticker_argument(downloader):
    dl, _ = downloader

    malformed_apple_ticker = "  \n  \t aApL    \t "
    num_downloaded = dl.get_8k_filings(malformed_apple_ticker, 1)
    assert num_downloaded == 1

    cik_num = 102909
    num_downloaded = dl.get_13f_hr_filings(cik_num, 1)
    assert num_downloaded == 1

    invalid_ticker = "INVALIDTICKER"
    num_downloaded = dl.get_all_available_filings(invalid_ticker)
    assert num_downloaded == 0

    # mutual funds do not file SEC forms
    mutual_fund_ticker = "VTSAX"
    num_downloaded = dl.get_all_available_filings(mutual_fund_ticker)
    assert num_downloaded == 0


def test_before_date_argument(downloader, apple_filing_metadata):
    dl, _ = downloader
    expected_msg = "Please enter a date string of the form YYYYMMDD."

    with pytest.raises(Exception) as excinfo:
        dl.get_8k_filings(apple_filing_metadata["symbol"], 1, "January 30, 2019")
    assert expected_msg in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        dl.get_8k_filings(apple_filing_metadata["symbol"], 1, datetime.today())
    assert expected_msg in str(excinfo.value)

    before_date_num = 20190130
    num_downloaded = dl.get_8k_filings(
        apple_filing_metadata["symbol"], 1, before_date_num
    )
    assert num_downloaded == 1
