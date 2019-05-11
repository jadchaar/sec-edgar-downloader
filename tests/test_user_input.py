import pytest
import requests
from pathlib import Path

# ! TODO: test passing in non-int num_filings
# ! TODO: test passing in negative num_filings
# TODO: test num_filings_to_obtain > 100
# TODO: test passing in CIK and ticker with trailing whitespace and symbols
# TODO: test passing in CIK as number

# TODO: test throwing IO error in ctor


def test_bad_responses(downloader, apple_filing_metadata):
    dl, _ = downloader

    codes_to_test = [("400", "400 Client Error"), ("500", "500 Server Error")]

    for code in codes_to_test:
        dl._base_url = f"https://httpstat.us/{code[0]}?action=getcompany&owner=exclude&count=100"
        with pytest.raises(requests.exceptions.HTTPError) as excinfo:
            num_downloaded = dl.get_all_available_filings(apple_filing_metadata["ticker_symbol"], 1)
        assert code[1] in str(excinfo.value)
