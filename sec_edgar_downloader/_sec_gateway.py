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

# In v4.x, blocking=True (default) will wait until a permit is available.
# buffer_ms adds a small delay buffer to account for timing variations (default: 50ms).
limiter = Limiter(SEC_THROTTLE_LIMIT_RATE)


@limiter.as_decorator(name="sec_global_rate_limit", weight=1)
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
