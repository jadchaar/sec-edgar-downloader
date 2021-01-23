# Regression test for issue 54
def test_http_error_on_download(downloader, capsys):
    dl, _ = downloader

    filing_type = "8-K"
    cik = "0000101778"
    # Search API outputs an incorrect filename for this filing's detail document,
    # so we must catch the 404 HTTP error and continue execution normally.
    dl.get(
        filing_type,
        cik,
        download_details=True,
        include_amends=True,
        after="2001-02-26",
        before="2001-02-28",
    )

    captured = capsys.readouterr()
    # Full submission should download fine
    assert "skipping full submission download" not in captured.out.lower()
    # Filing detail download should fail
    assert "skipping filing detail download" in captured.out.lower()
