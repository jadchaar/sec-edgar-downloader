"""
Tests the behavior and error handling of the Downloader
in the presence of abnormal and malformed user input.
"""

from datetime import datetime, timedelta

import pytest


def test_invalid_filing_type(downloader):
    dl, _ = downloader
    fake_filing_type = "10-FAKE"
    ticker = "AAPL"
    expected_msg = f"'{fake_filing_type}' filings are not supported."

    with pytest.raises(ValueError) as excinfo:
        dl.get(fake_filing_type, ticker)
    assert expected_msg in str(excinfo.value)


def test_invalid_ticker(downloader):
    dl, dl_path = downloader

    filing_type = "10-K"
    ticker = "INVALIDTICKER"
    num_filings_downloaded = dl.get(filing_type, ticker)

    # invalid tickers will result in 0 filings
    # so intermediate folders will not be created
    assert num_filings_downloaded == 0
    assert len(list(dl_path.glob("*"))) == 0

    filings_save_path = dl_path / "sec_edgar_filings"
    assert not filings_save_path.exists()

    ticker_save_path = filings_save_path / ticker
    assert not ticker_save_path.exists()

    filing_type_save_path = ticker_save_path / filing_type
    assert not filing_type_save_path.exists()


def test_invalid_num_filings_to_download(downloader):
    dl, _ = downloader
    expected_msg = (
        "Please enter a number greater than 1 for the number of filings to download."
    )

    filing_type = "10-K"
    ticker = "AAPL"

    with pytest.raises(ValueError) as excinfo:
        dl.get(filing_type, ticker, -1)
    assert expected_msg in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        dl.get(filing_type, ticker, 0)
    assert expected_msg in str(excinfo.value)


def test_invalid_before_and_after_dates(downloader):
    dl, _ = downloader
    expected_msg = (
        "Incorrect date format. Please enter a date string of the form YYYYMMDD."
    )

    filing_type = "8-K"
    ticker = "AAPL"

    # AAPL filed a 8-K on 2019-11-15
    after_date = datetime(2019, 11, 15)
    before_date = datetime(2019, 11, 15)

    with pytest.raises(ValueError) as excinfo:
        dl.get(filing_type, ticker, after_date=after_date.strftime("%Y-%m-%d"))
    assert expected_msg in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        dl.get(filing_type, ticker, before_date=before_date.strftime("%Y-%m-%d"))
    assert expected_msg in str(excinfo.value)

    # after_date == before_date
    num_filings_downloaded = dl.get(
        filing_type,
        ticker,
        after_date=after_date.strftime("%Y%m%d"),
        before_date=before_date.strftime("%Y%m%d"),
    )
    assert num_filings_downloaded == 1

    # after_date < before_date
    after_date -= timedelta(1)
    before_date += timedelta(1)
    num_filings_downloaded = dl.get(
        filing_type,
        ticker,
        after_date=after_date.strftime("%Y%m%d"),
        before_date=before_date.strftime("%Y%m%d"),
    )
    assert num_filings_downloaded == 1

    # after_date > before_date
    after_date += timedelta(3)
    expected_msg = "Invalid after_date and before_date."
    with pytest.raises(ValueError) as excinfo:
        dl.get(
            filing_type,
            ticker,
            after_date=after_date.strftime("%Y%m%d"),
            before_date=before_date.strftime("%Y%m%d"),
        )
    assert expected_msg in str(excinfo.value)
