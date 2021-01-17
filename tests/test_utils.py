"""Test miscellaneous utility functions."""

from sec_edgar_downloader._utils import resolve_relative_urls_in_filing


def test_resolve_relative_urls():
    sample_img = "foobar.jpg"
    sample_anchor_fragment = "#anchor_link"
    sample_anchor_html = "external.html"

    sample_filing_html = f"""<html>
        <head>
            <title>aapl-20200926</title>
        </head>
        <body>
            <img src="{sample_img}" />
            <a href="{sample_anchor_fragment}">random anchor link</a>
            <img src="{sample_img}" />
            <a href="{sample_anchor_fragment}">another random anchor link</a>
            <a href="{sample_anchor_html}">yet another random anchor link</a>
        </body>
    </html>
    """

    assert sample_filing_html.count(f'"{sample_img}"') == 2
    assert sample_filing_html.count(f'"{sample_anchor_fragment}"') == 2
    assert sample_filing_html.count(f'"{sample_anchor_html}"') == 1

    # Example base URL for an actual Apple 10-K filing
    base_url = "https://www.sec.gov/Archives/edgar/data/0000320193/000032019320000096/"

    # Must cast to a string since we are not writing bytes to a file
    resolved_filing_html = str(
        resolve_relative_urls_in_filing(sample_filing_html, base_url)
    )

    assert sample_filing_html != resolved_filing_html
    assert resolved_filing_html.count(f'"{base_url}{sample_img}"') == 2
    assert resolved_filing_html.count(f'"{base_url}{sample_anchor_fragment}"') == 2
    assert resolved_filing_html.count(f'"{base_url}{sample_anchor_html}"') == 1
