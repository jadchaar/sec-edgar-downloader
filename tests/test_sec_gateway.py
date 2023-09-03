import time
from unittest import mock

import pytest
from requests.exceptions import RequestException

from sec_edgar_downloader._sec_gateway import (
    _call_sec,
    download_filing,
    get_list_of_available_filings,
    get_ticker_metadata,
)


# Source: https://stackoverflow.com/a/28507806/3820660
def mock_sec_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, byte_content, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.byte_content = byte_content

        def json(self):
            return self.json_data

        @property
        def content(self):
            return self.byte_content

        def raise_for_status(self):
            if self.status_code != 200:
                raise RequestException("Non-2xx status code detected")

    if "sec.gov/files/company_tickers_exchange.json" in args[0]:
        return MockResponse({"key1": "value1"}, None, 200)
    elif "sec.gov/Archives/edgar/data/" in args[0]:
        return MockResponse(None, b"sample file content", 200)
    elif "data.sec.gov/submissions/" in args[0]:
        return MockResponse({"key1": "value1"}, None, 200)
    elif "valid-url" in args[0]:
        return MockResponse(None, None, 200)

    return MockResponse(None, None, 404)


@mock.patch("requests.get", side_effect=mock_sec_request)
def test_download_filing(_):
    download_filing("data.sec.gov/submissions/", "user_agent")


@mock.patch("requests.get", side_effect=mock_sec_request)
def test_get_list_of_available_filings(_):
    get_list_of_available_filings("sec.gov/Archives/edgar/data/", "user_agent")


@mock.patch("requests.get", side_effect=mock_sec_request)
def test_get_ticker_metadata(_):
    get_ticker_metadata("user_agent")


@mock.patch("requests.get", side_effect=mock_sec_request)
def test_call_sec_exception(_):
    with pytest.raises(RequestException):
        _call_sec("non-existent-url", "user_agent", "host")


@mock.patch("requests.get", side_effect=mock_sec_request)
def test_call_sec_rate_limit(_):
    start = time.time()
    # SEC allows up to 10 requests per second before throttling customer requests
    # Therefore, 15 requests should take more than 1 second to complete
    for i in range(15):
        _call_sec(f"valid-url-{i}", "user_agent", "host")
    diff = time.time() - start
    # Occasionally, this measurement is very close to 1, but slightly below.
    # Comparing against .99 will reduce the flakiness of this unit tests.
    assert diff > 0.99
