"""Tests the filing URLs to download for each filing type."""

from sec_edgar_downloader._utils import get_filing_urls_to_download


def test_filing_url_retrieval():
    filing_type = "8-K"
    ticker = "AAPL"
    after_date = None
    before_date = "20191115"
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
    # there are 176 AAPL 8-K filings before 20191115
    assert len(filings_to_download) == 176

    # num_filings_to_download == number of filings available
    num_filings_to_download = 176
    filings_to_download = get_filing_urls_to_download(
        filing_type,
        ticker,
        num_filings_to_download,
        after_date,
        before_date,
        include_amends,
    )
    # there are 176 AAPL 8-K filings before 20191115
    assert len(filings_to_download) == 176
