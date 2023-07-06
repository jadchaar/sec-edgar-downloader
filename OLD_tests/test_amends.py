"""Tests downloading filings in presence of filing amends (e.g. 8-K/A)."""
from datetime import date

from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS
from sec_edgar_downloader._utils import get_filing_urls_to_download


def test_include_amends():
    ticker = "AAPL"
    filing_type = "10-K"
    num_filings_to_download = 100
    # AAPL has 10-K/A amends before this date
    before_date = date(2019, 12, 1).strftime(DATE_FORMAT_TOKENS)
    after_date = None

    filing_urls_without_amends = get_filing_urls_to_download(
        filing_type, ticker, num_filings_to_download, after_date, before_date, False
    )
    num_filings_without_amends = len(filing_urls_without_amends)

    filing_urls_with_amends = get_filing_urls_to_download(
        filing_type, ticker, num_filings_to_download, after_date, before_date, True
    )
    num_filings_with_amends = len(filing_urls_with_amends)

    num_amends = num_filings_with_amends - num_filings_without_amends
    assert num_amends > 0
