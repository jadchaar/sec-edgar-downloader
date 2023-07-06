import sys
from pathlib import Path
from typing import Optional

from ._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE
from ._orchestrator import fetch_and_save_filings
from ._types import DownloadMetadata, DownloadPath
from ._utils import is_cik, validate_and_parse_date


class Downloader:
    def __init__(
        self,
        company_name: str,
        email_address: str,
        download_folder: Optional[DownloadPath] = None,
    ) -> None:
        # TODO: add validation for email
        self.user_agent = f"{company_name} {email_address}"

        if download_folder is None:
            self.download_folder = Path.cwd()
        elif isinstance(download_folder, Path):
            self.download_folder = download_folder
        else:
            self.download_folder = Path(download_folder).expanduser().resolve()

    def get(
        self,
        form: str,
        ticker_or_cik: str,
        *,
        limit: Optional[int] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        include_amends: bool = False,
        download_details: bool = True,
    ) -> int:
        # TODO: add conversion from ticker to CIK
        # TODO: add validation and defaulting
        # TODO: can we rely on class default values rather than manually checking None?
        ticker_or_cik = str(ticker_or_cik).strip().upper()

        # Check for blank tickers or CIKs
        if not ticker_or_cik:
            raise ValueError("Invalid ticker or CIK. Please enter a non-blank value.")

        # Detect CIKs and ensure that they are properly zero-padded
        if is_cik(ticker_or_cik):
            if len(ticker_or_cik) > 10:
                raise ValueError("Invalid CIK. CIKs must be at most 10 digits long.")
            # Pad CIK with 0s to ensure that it is exactly 10 digits long
            # The SEC Edgar Search API requires zero-padded CIKs to ensure
            # that search results are accurate. Relates to issue #84.
            ticker_or_cik = ticker_or_cik.zfill(10)

        if limit is None:
            # If amount is not specified, obtain all available filings.
            # We simply need a large number to denote this and the loop
            # responsible for fetching the URLs will break appropriately.
            limit = sys.maxsize
        else:
            limit = int(limit)
            if limit < 1:
                raise ValueError(
                    "Invalid amount. Please enter a number greater than 1."
                )

        # SEC allows for filing searches from 1994 onwards
        if after is None:
            after = DEFAULT_AFTER_DATE
        else:
            after = validate_and_parse_date(after)

            if after < DEFAULT_AFTER_DATE:
                after = DEFAULT_AFTER_DATE

        if before is None:
            before = DEFAULT_BEFORE_DATE
        else:
            before = validate_and_parse_date(before)

        num_downloaded = fetch_and_save_filings(
            DownloadMetadata(
                self.download_folder,
                form,
                ticker_or_cik,
                limit,
                after,
                before,
                include_amends,
                download_details,
            ),
            self.user_agent,
        )

        return num_downloaded
