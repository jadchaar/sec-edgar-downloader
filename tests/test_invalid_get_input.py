"""
Tests the behavior and error handling of the Downloader
in the presence of abnormal and malformed user input.
"""

import pytest


def test_invalid_filing_type(downloader):
    dl, _ = downloader
    fake_filing_type = "10-FAKE"
    expected_msg = f"'{fake_filing_type}' filings are not supported."

    with pytest.raises(ValueError) as excinfo:
        dl.get(fake_filing_type, "AAPL")
    assert expected_msg in str(excinfo.value)


def test_invalid_ticker(downloader):
    dl, dl_path = downloader

    ticker = "INVALIDTICKER"
    filing_type = "10-K"
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
