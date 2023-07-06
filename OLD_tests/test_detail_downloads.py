# Regression test for issue #60
def test_recursion_error_older_filings(downloader):
    dl, _ = downloader

    filing_type = "10-K"
    ticker = "AIZ"
    # 10-K filing details before 2005 for AIZ cause a RecursionError
    # when resolving relative URLs. This issue can be resolved by
    # using lxml rather than html.parser as the parser for bs4.
    num_downloaded = dl.get(
        filing_type,
        ticker,
        download_details=True,
        include_amends=False,
        before="2005-03-31",
    )
    assert num_downloaded == 2
