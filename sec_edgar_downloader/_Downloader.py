import sys
from pathlib import Path
from typing import ClassVar, List, Optional, Set

from ._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE
from ._constants import SUPPORTED_FORMS as _SUPPORTED_FORMS
from ._orchestrator import fetch_and_save_filings, get_ticker_to_cik_mapping
from ._types import Date, DownloadMetadata, DownloadPath
from ._utils import is_cik, validate_and_convert_ticker_or_cik, validate_and_parse_date


class Downloader:
    """A :class:`Downloader` object.

    :param company_name: company name to comply with SEC Edgar's programmatic downloading
        fair access policy. All programmatic SEC interactions must declare a header comprised
        of a company name and email address.
        More info: https://www.sec.gov/os/webmaster-faq#code-support.
    :param email_address: email address to comply with SEC Edgar's programmatic downloading
        fair access policy. All programmatic SEC interactions must declare a header comprised
        of a company name and email address.
        More info: https://www.sec.gov/os/webmaster-faq#code-support.
    :param download_folder: relative or absolute path to download location.
        Defaults to the current working directory.

    Usage::

        >>> from sec_edgar_downloader import Downloader

        # Download to current working directory.
        # Must declare company name and email address to comply with SEC Edgar's
        # programmatic downloading fair access policy.
        # More info: https://www.sec.gov/os/webmaster-faq#code-support
        >>> dl = Downloader("MyCompanyName", "my.email@domain.com")

        # Download to relative or absolute path
        >>> dl = Downloader("MyCompanyName", "my.email@domain.com", "/path/to/save/location")
    """

    supported_forms: ClassVar[List[str]] = sorted(_SUPPORTED_FORMS)

    def __init__(
        self,
        company_name: str,
        email_address: str,
        download_folder: Optional[DownloadPath] = None,
    ) -> None:
        """Constructor for the :class:`Downloader` class."""
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
        after: Optional[Date] = None,
        before: Optional[Date] = None,
        include_amends: bool = False,
        download_details: bool = False,
        accession_numbers_to_skip: Optional[Set[str]] = None,
    ) -> int:
        """Download filings and save them to disk.

        :param form: form type to download (e.g. 8-K, 10-K).
        :param ticker_or_cik: ticker or CIK for which to download filings.
        :param limit: max number of filings to download.
            Defaults to all available filings.
        :param after: date of form YYYY-MM-DD after which to download filings.
            Date or datetime objects can also be passed.
            Defaults to 1994-01-01, the earliest date supported by SEC EDGAR.
        :param before: date of form YYYY-MM-DD before which to download filings.
            Date or datetime objects can also be passed.
            Defaults to today.
        :param include_amends: denotes whether to include filing amends (e.g. 8-K/A).
            Defaults to False.
        :param download_details: denotes whether to download human-readable and easily
            parseable filing detail documents (e.g. form 4 XML, 8-K HTML). Defaults to False.
        :param accession_numbers_to_skip: Set of accession numbers to skip when downloading.
        :return: number of filings downloaded.

        Usage::

            >>> from sec_edgar_downloader import Downloader
            >>> dl = Downloader("MyCompanyName", "my.email@domain.com")

            # Get all 8-K filings for Apple
            >>> dl.get("8-K", "AAPL")

            # Get all 8-K filings for Apple, including filing amends (8-K/A)
            >>> dl.get("8-K", "AAPL", include_amends=True)

            # Get all 8-K filings for Apple after January 1, 2017 and before March 25, 2017
            >>> dl.get("8-K", "AAPL", after="2017-01-01", before="2017-03-25")

            # Get the five most recent 10-K filings for Apple
            >>> dl.get("10-K", "AAPL", limit=5)

            # Get all 10-K filings for Apple, excluding the filing detail documents
            >>> dl.get("10-K", "AAPL", amount=1, download_details=False)

            # Get all 10-Q filings for Visa
            >>> dl.get("10-Q", "V")

            # Get all 13F-NT filings for the Vanguard Group
            >>> dl.get("13F-NT", "0000102909")

            # Get all 13F-HR filings for the Vanguard Group
            >>> dl.get("13F-HR", "0000102909")

            # Get all SC 13G filings for Apple
            >>> dl.get("SC 13G", "AAPL")

            # Get all SD filings for Apple
            >>> dl.get("SD", "AAPL")
        """
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
                # Save ticker if passed in to form file system path for saving filings
                ticker=ticker_or_cik if not is_cik(ticker_or_cik) else None,
                accession_numbers_to_skip=accession_numbers_to_skip,
            ),
            self.user_agent,
        )

        return num_downloaded
