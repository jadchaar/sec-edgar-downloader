import sys
from pathlib import Path
from typing import ClassVar, List, Optional

from ._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE
from ._constants import SUPPORTED_FORMS as _SUPPORTED_FORMS
from ._orchestrator import fetch_and_save_filings, get_ticker_to_cik_mapping
from ._types import DownloadMetadata, DownloadPath
from ._utils import validate_and_convert_ticker_or_cik, validate_and_parse_date


class Downloader:
    supported_forms: ClassVar[List[str]] = sorted(_SUPPORTED_FORMS)

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

        self.ticker_to_cik_mapping = get_ticker_to_cik_mapping(self.user_agent)

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
        # TODO: add validation and defaulting
        # TODO: can we rely on class default values rather than manually checking None?
        cik = validate_and_convert_ticker_or_cik(
            ticker_or_cik, self.ticker_to_cik_mapping
        )

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
            after_date = DEFAULT_AFTER_DATE
        else:
            after_date = validate_and_parse_date(after)

            if after_date < DEFAULT_AFTER_DATE:
                after_date = DEFAULT_AFTER_DATE

        if before is None:
            before_date = DEFAULT_BEFORE_DATE
        else:
            before_date = validate_and_parse_date(before)

        if after_date > before_date:
            raise ValueError("After date cannot be greater than the before date.")

        if form not in _SUPPORTED_FORMS:
            form_options = ", ".join(self.supported_forms)
            raise ValueError(
                f"{form!r} forms are not supported. "
                f"Please choose from the following: {form_options}."
            )

        num_downloaded = fetch_and_save_filings(
            DownloadMetadata(
                self.download_folder,
                form,
                cik,
                limit,
                after_date,
                before_date,
                include_amends,
                download_details,
            ),
            self.user_agent,
        )

        return num_downloaded
