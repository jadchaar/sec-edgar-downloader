import pytest
import requests


def test_bad_responses(downloader, apple_filing_metadata):
    dl, _ = downloader

    codes_to_test = [("400", "400 Client Error"), ("500", "500 Server Error")]

    for code in codes_to_test:
        dl._base_url = (
            f"https://httpstat.us/{code[0]}?action=getcompany&owner=exclude&count=100"
        )
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            dl.get_all_available_filings(apple_filing_metadata["symbol"], 1)
        assert code[1] in str(excinfo.value)
