"""Provides the :class:`Downloader` class, which is used to download SEC filings."""

import sys
from datetime import date
from pathlib import Path

from ._constants import SUPPORTED_FILINGS
from ._utils import download_filings, get_filing_urls_to_download, validate_date_format


class Downloader:
    """A :class:`Downloader` object.

    :param download_folder: relative or absolute path to download location,
        defaulting to the user's ``Downloads`` folder.
    :type download_folder: ``str``, optional

    Usage::
        >>> import sec_edgar_downloader
        >>> dl = sec_edgar_downloader.Downloader()
    """

    def __init__(self, download_folder=None):
        """Constructor for the :class:`Downloader` class."""
        if download_folder is None:
            self.download_folder = Path.home().joinpath("Downloads")
        else:
            self.download_folder = Path(download_folder).expanduser().resolve()

    @property
    def supported_filings(self):
        """Get a sorted list of all supported filings.

        :return: sorted list of all supported filings.
        :rtype: ``list``
        """
        return sorted(SUPPORTED_FILINGS)

    def get(
        self,
        filing_type,
        ticker_or_cik,
        num_filings_to_download=None,
        after_date=None,
        before_date=None,
        include_amends=False,
    ):
        """Downloads filing documents and saves them to disk.

        :param filing_type: type of filing to download
        :type filing_type: ``str``
        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download,
            defaults to all available filings
        :type num_filings_to_download: ``int``, optional
        :param after_date: date of form YYYYMMDD in which to download filings after,
            defaults to None
        :type after_date: ``str``, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str``, optional
        :param include_amends: denotes whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all 8-K filings for Apple (ticker: AAPL)
            >>> dl.get("8-K", "AAPL")

            # Get all 8-K filings for Apple, including filing amends (8-K/A)
            >>> dl.get("8-K", "AAPL", include_amends=True)

            # Get all 8-K filings for Apple after January 1, 2017 and before March 25, 2017
            # Note: before_date and after_date strings must be in the form "YYYYMMDD"
            >>> dl.get("8-K", "AAPL", after_date="20170101", before_date="20170325")

            # Get the five most recent 10-K filings for Apple
            >>> dl.get("10-K", "AAPL", 5)

            # Get all 13F-NT filings for the Vanguard Group (CIK: 0000102909)
            >>> dl.get("13F-NT", "0000102909")

            # Get all 13F-HR filings for the Vanguard Group
            >>> dl.get("13F-HR", "0000102909")
        """
        # TODO: add ability to pass in list of filing types
        # TODO: add ability to pass in datetime objects
        if filing_type not in SUPPORTED_FILINGS:
            filing_options = ", ".join(sorted(SUPPORTED_FILINGS))
            raise ValueError(
                f"'{filing_type}' filings are not supported. "
                f"Please choose from the following: {filing_options}."
            )

        ticker_or_cik = str(ticker_or_cik).strip().upper().lstrip("0")

        if num_filings_to_download is None:
            # obtain all available filings, so we simply
            # need a large number to denote this
            num_filings_to_download = sys.maxsize
        else:
            num_filings_to_download = int(num_filings_to_download)
            if num_filings_to_download < 1:
                raise ValueError(
                    "Please enter a number greater than 1 "
                    "for the number of filings to download."
                )

        # no sensible default exists for after_date
        if after_date is not None:
            after_date = str(after_date)
            validate_date_format(after_date)

        if before_date is None:
            before_date = date.today().strftime("%Y%m%d")
        else:
            before_date = str(before_date)
            validate_date_format(before_date)

        if after_date is not None and after_date > before_date:
            raise ValueError(
                "Invalid after_date and before_date. "
                "Please enter an after_date that is less than the before_date."
            )

        filings_to_fetch = get_filing_urls_to_download(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            after_date,
            before_date,
            include_amends,
        )

        download_filings(
            self.download_folder, ticker_or_cik, filing_type, filings_to_fetch
        )

        return len(filings_to_fetch)
