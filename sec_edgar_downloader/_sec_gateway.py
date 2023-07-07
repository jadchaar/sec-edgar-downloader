from typing import Any

import requests
from pyrate_limiter import Limiter

from ._constants import (
    HOST_DATA_SEC,
    HOST_WWW_SEC,
    SEC_RATE_LIMIT,
    STANDARD_HEADERS,
    URL_CIK_MAPPING,
)

limiter = Limiter(SEC_RATE_LIMIT)


@limiter.ratelimit("sec_global_rate_limit", delay=True)
def _call_sec(uri: str, user_agent: str, host: str) -> Any:
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


def download_filing(uri: str, user_agent: str) -> Any:
    return _call_sec(uri, user_agent, HOST_WWW_SEC).content


def get_list_of_available_filings(uri: str, user_agent: str) -> Any:
    return _call_sec(uri, user_agent, HOST_DATA_SEC).json()


def get_ticker_metadata(user_agent: str) -> Any:
    return _call_sec(URL_CIK_MAPPING, user_agent, HOST_WWW_SEC).json()
