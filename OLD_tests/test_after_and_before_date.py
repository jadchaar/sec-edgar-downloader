"""Tests after_date and before_date download bounds."""

import sys
from datetime import datetime, timedelta

from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS
from sec_edgar_downloader._utils import get_filing_urls_to_download


def test_date_bounds():
    filing_type = "8-K"
    # get all available filings in the date range
    num_filings_to_download = sys.maxsize
    ticker = "AAPL"
    after_date = datetime(2017, 9, 12)
    before_date = datetime(2019, 11, 15)
    include_amends = False

    # filings available on after_date and before_date
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date.strftime(DATE_FORMAT_TOKENS),
        before_date.strftime(DATE_FORMAT_TOKENS),
        include_amends,
    )
    assert len(filings_to_download) == 20

    after_date += timedelta(days=1)
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date.strftime(DATE_FORMAT_TOKENS),
        before_date.strftime(DATE_FORMAT_TOKENS),
        include_amends,
    )
    assert len(filings_to_download) == 19

    before_date -= timedelta(days=1)
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date.strftime(DATE_FORMAT_TOKENS),
        before_date.strftime(DATE_FORMAT_TOKENS),
        include_amends,
    )
    assert len(filings_to_download) == 18

    # num_filings_to_download < number of filings available
    num_filings_to_download = 5
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date.strftime(DATE_FORMAT_TOKENS),
        before_date.strftime(DATE_FORMAT_TOKENS),
        include_amends,
    )
    assert len(filings_to_download) == 5
