"""Test filing retrieval with keyword search query."""

import sys

from sec_edgar_downloader._utils import (
    get_filing_urls_to_download,
    get_number_of_unique_filings,
)


def test_simple_query(formatted_earliest_after_date):
    # Search for "antitrust" in all AAPL proxy statements
    filing_type = "DEF 14A"
    ticker = "AAPL"
    before = "2021-01-10"
    include_amends = False
    query = "antitrust"

    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        sys.maxsize,
        formatted_earliest_after_date,
        before,
        include_amends,
        query,
    )
    # Proxy statements are published in both HTML and PDF form and the EDGAR
    # search API provides each one as its own hit.
    assert len(filings_to_download) == 6
    assert get_number_of_unique_filings(filings_to_download) == 3
