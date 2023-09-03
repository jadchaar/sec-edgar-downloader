from typing import Any

import requests
from pyrate_limiter import Duration, Limiter, Rate
from requests import Response

from ._constants import (
    HOST_DATA_SEC,
    HOST_WWW_SEC,
    SEC_REQUESTS_PER_SEC_MAX,
    STANDARD_HEADERS,
    URL_CIK_MAPPING,
)

# 10 requests per second rate limit set by SEC:
# https://www.sec.gov/os/webmaster-faq#developers
SEC_THROTTLE_LIMIT_RATE = Rate(SEC_REQUESTS_PER_SEC_MAX, Duration.SECOND)

# Wait up to 60 seconds for the rate-limiter bucket to refill.
# If the bucket does NOT refill, an exception will be raised.
limiter = Limiter(
    SEC_THROTTLE_LIMIT_RATE, raise_when_fail=True, max_delay=60_000
).as_decorator()


def limiter_mapping(*args):
    return "sec_global_rate_limit", 1


@limiter(limiter_mapping)
def _call_sec(uri: str, user_agent: str, host: str) -> Response:
    resp = requests.get(
        uri,
        headers={
            **STANDARD_HEADERS,
            "User-Agent": user_agent,
            "Host": host,
        },
    )
    resp.raise_for_status()
    return resp


def download_filing(uri: str, user_agent: str) -> bytes:
    return _call_sec(uri, user_agent, HOST_WWW_SEC).content


def get_list_of_available_filings(uri: str, user_agent: str) -> Any:
    return _call_sec(uri, user_agent, HOST_DATA_SEC).json()


def get_ticker_metadata(user_agent: str) -> Any:
    return _call_sec(URL_CIK_MAPPING, user_agent, HOST_WWW_SEC).json()
