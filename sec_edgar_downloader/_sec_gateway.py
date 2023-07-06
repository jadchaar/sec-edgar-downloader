import requests
from ._types import DownloadType
from typing import Any
from pyrate_limiter import Limiter
from ._constants import SEC_RATE_LIMIT, STANDARD_HEADERS

limiter = Limiter(SEC_RATE_LIMIT)


# TODO: improve typing of response (don't use Any)
@limiter.ratelimit('sec_rate_limit', delay=True)
def fetch_from_sec(uri: str, user_agent: str, download_type: DownloadType) -> Any:
    resp = requests.get(uri, headers={
        **STANDARD_HEADERS,
        "User-Agent": user_agent,
        "Host": "data.sec.gov" if download_type == DownloadType.API else "www.sec.gov",
    })
    resp.raise_for_status()
    return resp.json() if download_type == DownloadType.API else resp.content
