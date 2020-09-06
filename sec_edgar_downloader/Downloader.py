"""Provides a :class:`Downloader` class for downloading SEC EDGAR filings."""

import sys
from pathlib import Path
from typing import List, Optional, Union

from ._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE, SUPPORTED_FILINGS
from ._utils import download_filings, get_filing_urls_to_download, validate_date_format


class Downloader:
    """A :class:`Downloader` object.

    :param download_folder: relative or absolute path to download location.
        Defaults to the current working directory.

    Usage::

        >>> from sec_edgar_downloader import Downloader
        >>> dl = Downloader()
    """

    def __init__(self, download_folder: Union[str, Path, None] = None) -> None:
        """Constructor for the :class:`Downloader` class."""
        if download_folder is None:
            self.download_folder = Path.cwd()
        elif isinstance(download_folder, Path):
            self.download_folder = download_folder
        else:
            self.download_folder = Path(download_folder).expanduser().resolve()

    @property
    def supported_filings(self) -> List[str]:
        """Get a sorted list of all supported filings.

        :return: sorted list of all supported filings.

        Usage::

            >>> from sec_edgar_downloader import Downloader
            >>> dl = Downloader()
            >>> dl.supported_filings
            ['1', ..., '10-K', '10-KT', '10-Q', ..., '13F-HR', '13F-NT', ..., 'X-17A-5'']
        """
        return sorted(SUPPORTED_FILINGS)

    # TODO: add new arguments to docstring
    def get(
        self,
        filings: Union[str, List[str]],
        ticker_or_cik: str,
        amount: Optional[int] = None,
        *,
        after: Optional[str] = None,
        before: Optional[str] = None,
        include_amends: bool = False,
        download_details: bool = True,
    ) -> int:
        """Download filings and save them to disk.

        :param filings: filing types to download. Can either be a single filing type or
            a list of filing types (e.g. "8-K" or ["8-K", "10-K"]).
        :param ticker_or_cik: ticker or CIK to download filings for.
        :param amount: number of filings to download.
            Defaults to all available filings.
        :param after: date of form YYYY-MM-DD after which to download filings.
            Defaults to 2000-01-01, the earliest date supported by EDGAR full text search.
        :param before: date of form YYYY-MM-DD before which to download filings.
            Defaults to today.
        :param include_amends: denotes whether or not to include filing amends (e.g. 8-K/A).
            Defaults to False.
        :param download_details: denotes whether or not to download filing detail documents
            (e.g. form 4 XML, 8-K HTML). Defaults to True.
        :return: number of filings downloaded.

        Usage::

            >>> from sec_edgar_downloader import Downloader
            >>> dl = Downloader()

            # Get all 8-K filings for Apple
            >>> dl.get("8-K", "AAPL")

            # Get all 8-K filings for Apple, including filing amends (8-K/A)
            >>> dl.get("8-K", "AAPL", include_amends=True)

            # Get all 8-K filings for Apple after January 1, 2017 and before March 25, 2017
            >>> dl.get("8-K", "AAPL", after_date="2017-01-01", before_date="2017-03-25")

            # Get the five most recent 10-K filings for Apple
            >>> dl.get("10-K", "AAPL", 5)

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
        if isinstance(filings, str):
            filings = [filings]

        ticker_or_cik = str(ticker_or_cik).strip().upper().lstrip("0")

        # TODO: all filings should rely on after_date being 2000-01-01
        #  maxsize makes me uncomfortable
        if amount is None:
            # obtain all available filings, so we simply
            # need a large number to denote this
            amount = sys.maxsize
        else:
            amount = int(amount)
            if amount < 1:
                raise ValueError(
                    "Please enter a number greater than 1 "
                    "for the number of filings to download."
                )

        # SEC allows for filing searches from 2000 onwards
        if after is None:
            after = DEFAULT_AFTER_DATE
        else:
            after = str(after)
            validate_date_format(after)

            # TODO: test this!
            if after < DEFAULT_AFTER_DATE:
                raise ValueError(
                    "Filings cannot be downloaded prior to 2000. "
                    f"Please enter a date on or after {DEFAULT_AFTER_DATE}."
                )

        if before is None:
            before = DEFAULT_BEFORE_DATE
        else:
            before = str(before)
            validate_date_format(before)

        if after is not None and after > before:
            raise ValueError(
                "Invalid after_date and before_date. "
                "Please enter an after_date that is less than the before_date."
            )

        num_downloaded = 0
        for filing in filings:
            if filing not in SUPPORTED_FILINGS:
                filing_options = ", ".join(sorted(SUPPORTED_FILINGS))
                raise ValueError(
                    f"'{filing}' filings are not supported. "
                    f"Please choose from the following: {filing_options}."
                )

            # TODO: add try/except for keyerror with link
            # to issue reporting (SEC API may change)
            filings_to_fetch = get_filing_urls_to_download(
                filing,
                ticker_or_cik,
                amount,
                after,
                before,
                include_amends,
            )

            download_filings(
                self.download_folder,
                filing,
                ticker_or_cik,
                filings_to_fetch,
                download_details,
            )

            num_downloaded += len(filings_to_fetch)

        return num_downloaded
