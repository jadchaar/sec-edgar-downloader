"""Provides the :class:`Downloader` class, which is used to download SEC filings."""

from datetime import date
from pathlib import Path

import requests

from ._utils import form_query_string, parse_edgar_rss_feed, validate_before_date


class Downloader:
    """A :class:`Downloader` object.

    :param download_folder: relative or absolute path to download location,
        defaults to the user's ``Downloads`` folder.
    :type download_folder: ``str``, optional
    :param verbose: display download information, defaults to False
    :type verbose: ``bool``, optional

    Usage::

        >>> import sec_edgar_downloader
        >>> dl = sec_edgar_downloader.Downloader()
    """

    def __init__(self, download_folder=None, verbose=False):
        """Constructor for :class:`Downloader` class."""

        if download_folder is None:
            self._download_folder = Path.home().joinpath("Downloads")
        else:
            self._download_folder = Path(download_folder).expanduser().resolve()

        self._verbose_print = print if verbose else lambda *a, **k: None

        self._verbose_print(
            f"Company filings will be saved to: {self._download_folder}"
        )

        self._sec_base_url = "https://www.sec.gov"
        self._sec_edgar_base_url = f"{self._sec_base_url}/cgi-bin/browse-edgar?"

    def _download_filings(
        self,
        edgar_search_url,
        filing_type,
        ticker_or_cik,
        num_filings_to_download,
        include_amends,
    ):
        """Downloads filing documents and saves them to disk.

        :param edgar_search_url: URL to the XML containing the list of filings to download
        :type edgar_search_url: ``str``
        :param filing_type: type of filing to download
        :type filing_type: ``str``
        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download
        :type num_filings_to_download: ``int``
        :param include_amends: denotes whether or not to include filing amends (e.g. 8-K/A)
        :type include_amends: ``bool``
        :return: number of filings downloaded
        :rtype: ``int``
        """

        filing_document_info = parse_edgar_rss_feed(
            edgar_search_url, num_filings_to_download, filing_type, include_amends
        )

        # number of filings available may be less than the number requested
        num_filings_to_download = len(filing_document_info)

        if num_filings_to_download == 0:
            self._verbose_print(
                f"No {filing_type} documents available for {ticker_or_cik}."
            )
            return 0

        self._verbose_print(
            f"{num_filings_to_download} {filing_type} documents available for {ticker_or_cik}.",
            "Beginning download...",
        )

        for doc_info in filing_document_info:
            resp = requests.get(doc_info.url)
            resp.raise_for_status()

            save_path = self._download_folder.joinpath(
                "sec_edgar_filings", ticker_or_cik, filing_type, doc_info.filename
            )

            # Create all parent directories as needed. For example, if we have the
            # directory /hello and we want to create /hello/world/my/name/is/bob.txt,
            # this would create all the directories leading up to bob.txt.
            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, "w", encoding="utf-8") as f:
                f.write(resp.text)

        self._verbose_print(
            f"{filing_type} filings for {ticker_or_cik} downloaded successfully."
        )

        return num_filings_to_download

    def _get_filing_wrapper(
        self,
        filing_type,
        ticker_or_cik,
        num_filings_to_download,
        before_date,
        include_amends,
    ):
        """Processes and forms the SEC EDGAR search URL needed to perform filing downloads.

        :param filing_type: type of filing to download
        :type filing_type: ``str``
        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download
        :type num_filings_to_download: ``int``
        :param before_date: date of form YYYYMMDD in which to download filings before
        :type before_date: ``str`` or ``datetime``
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A)
        :type include_amends: ``bool``
        :raises ValueError: when a user passes in an invalid number of filings to download
        :return: number of filings downloaded
        :rtype: ``int``
        """

        if before_date is None:
            before_date = date.today().strftime("%Y%m%d")

        num_filings_to_download = int(num_filings_to_download)
        before_date = str(before_date)
        # Check that date is in required format: YYYYMMDD
        # Throws a ValueError if the date is not in the correct format
        validate_before_date(before_date)
        if num_filings_to_download < 1:
            raise ValueError(
                "Please enter a number greater than 1 for the number of filings to download."
            )
        ticker_or_cik = str(ticker_or_cik).strip().upper().lstrip("0")
        self._verbose_print(f"\nGetting {filing_type} filings for {ticker_or_cik}.")
        qs = form_query_string(ticker_or_cik, filing_type, before_date)
        edgar_search_url = f"{self._sec_edgar_base_url}{qs}"
        return self._download_filings(
            edgar_search_url,
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            include_amends,
        )

    """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Download methods for each supported SEC filing type
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    def get_8k_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads 8-K filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all 8-K filings for Apple
            >>> dl.get_8k_filings("AAPL")

            # Get the past 5 8-K filings for Apple
            >>> dl.get_8k_filings("AAPL", 5)

            # Get all 8-K filings for Apple, including filing amends (8-K/A)
            >>> dl.get_8k_filings("AAPL", include_amends=True)

            # Get all 8-K filings for Apple before March 25, 2017
            >>> dl.get_8k_filings("AAPL", before_date="20170325")
        """

        filing_type = "8-K"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    def get_10k_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads 10-K filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all 10-K filings for Apple
            >>> dl.get_10k_filings("AAPL")

            # Get the past 5 10-K filings for Apple
            >>> dl.get_10k_filings("AAPL", 5)

            # Get all 10-K filings for Apple, including filing amends (10-K/A)
            >>> dl.get_10k_filings("AAPL", include_amends=True)

            # Get all 10-K filings for Apple before March 25, 2017
            >>> dl.get_10k_filings("AAPL", before_date="20170325")
        """

        filing_type = "10-K"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    def get_10ksb_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads 10-KSB filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 10-KSB/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all 10-KSB filings for Ubiquitech Software
            >>> dl.get_10ksb_filings("1411460")

            # Get the past 5 10-KSB filings for Ubiquitech Software
            >>> dl.get_10ksb_filings("1411460", 5)

            # Get all 10-KSB filings for Ubiquitech Software, including filing amends (10-KSB/A)
            >>> dl.get_10ksb_filings("1411460", include_amends=True)

            # Get all 10-KSB filings for Ubiquitech Software before March 25, 2017
            >>> dl.get_10ksb_filings("1411460", before_date="20170325")
        """

        filing_type = "10KSB"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    def get_10q_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads 10-Q filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all 10-Q filings for Apple
            >>> dl.get_10q_filings("AAPL")

            # Get the past 5 10-Q filings for Apple
            >>> dl.get_10q_filings("AAPL", 5)

            # Get all 10-Q filings for Apple, including filing amends (10-Q/A)
            >>> dl.get_10q_filings("AAPL", include_amends=True)

            # Get all 10-Q filings for Apple before March 25, 2017
            >>> dl.get_10q_filings("AAPL", before_date="20170325")
        """

        filing_type = "10-Q"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    # Differences explained here: https://www.sec.gov/divisions/investment/13ffaq.htm
    def get_13f_nt_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads 13F-NT filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all 13F-NT filings for the Vanguard Group
            >>> dl.get_13f_nt_filings("0000102909")

            # Get the past 5 13F-NT filings for the Vanguard Group
            >>> dl.get_13f_nt_filings("0000102909", 5)

            # Get all 13F-NT filings for the Vanguard Group, including filing amends (13F-NT/A)
            >>> dl.get_13f_nt_filings("0000102909", include_amends=True)

            # Get all 13F-NT filings for the Vanguard Group before March 25, 2017
            >>> dl.get_13f_nt_filings("0000102909", before_date="20170325")
        """

        filing_type = "13F-NT"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    def get_13f_hr_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads 13F-HR filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all 13F-HR filings for the Vanguard Group
            >>> dl.get_13f_hr_filings("0000102909")

            # Get the past 5 13F-HR filings for the Vanguard Group
            >>> dl.get_13f_hr_filings("0000102909", 5)

            # Get all 13F-HR filings for the Vanguard Group, including filing amends (13F-HR/A)
            >>> dl.get_13f_hr_filings("0000102909", include_amends=True)

            # Get all 13F-HR filings for the Vanguard Group before March 25, 2017
            >>> dl.get_13f_hr_filings("0000102909", before_date="20170325")
        """

        filing_type = "13F-HR"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    def get_sc_13g_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads SC 13G filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all SC 13G filings for Apple
            >>> dl.get_sc_13g_filings("AAPL")

            # Get the past 5 SC 13G filings for Apple
            >>> dl.get_sc_13g_filings("AAPL", 5)

            # Get all SC 13G filings for Apple, including filing amends (SC 13G/A)
            >>> dl.get_sc_13g_filings("AAPL", include_amends=True)

            # Get all SC 13G filings for Apple before March 25, 2017
            >>> dl.get_sc_13g_filings("AAPL", before_date="20170325")
        """

        filing_type = "SC 13G"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    def get_sd_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads SD filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``

        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get all SD filings for Apple
            >>> dl.get_sd_filings("AAPL")

            # Get the past 5 SD filings for Apple
            >>> dl.get_sd_filings("AAPL", 5)

            # Get all SD filings for Apple, including filing amends (SD/A)
            >>> dl.get_sd_filings("AAPL", include_amends=True)

            # Get all SD filings for Apple before March 25, 2017
            >>> dl.get_sd_filings("AAPL", before_date="20170325")
        """

        filing_type = "SD"
        return self._get_filing_wrapper(
            filing_type,
            ticker_or_cik,
            num_filings_to_download,
            before_date,
            include_amends,
        )

    """
    Bulk download methods
    """

    def get_all_available_filings(
        self,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        include_amends=False,
    ):
        """Downloads all available filings for a specified ticker or CIK.

        :param ticker_or_cik: ticker or CIK to download filings for
        :type ticker_or_cik: ``str``
        :param num_filings_to_download: number of filings to download, defaults to 100
        :type num_filings_to_download: int, optional
        :param before_date: date of form YYYYMMDD in which to download filings before,
            defaults to today
        :type before_date: ``str`` or ``datetime``, optional
        :param include_amends: whether or not to include filing amends (e.g. 8-K/A),
            defaults to False
        :type include_amends: ``bool``, optional
        :return: number of filings downloaded
        :rtype: ``int``


        Usage::

            >>> import sec_edgar_downloader
            >>> dl = sec_edgar_downloader.Downloader()

            # Get the latest filings (8-K, 10-K, 10-Q, 13F, SC 13G, SD), if available, for Apple
            >>> dl.get_all_available_filings("AAPL", 1)

            # Get all filings (8-K, 10-K, 10-Q, 13F, SC 13G, SD), if available, for Apple
            >>> dl.get_all_available_filings("AAPL")
        """

        total_dl = 0
        total_dl += self.get_8k_filings(
            ticker_or_cik, num_filings_to_download, before_date, include_amends
        )
        total_dl += self.get_10k_filings(
            ticker_or_cik, num_filings_to_download, before_date, include_amends
        )
        total_dl += self.get_10q_filings(
            ticker_or_cik, num_filings_to_download, before_date, include_amends
        )
        total_dl += self.get_13f_nt_filings(
            ticker_or_cik, num_filings_to_download, before_date, include_amends
        )
        total_dl += self.get_13f_hr_filings(
            ticker_or_cik, num_filings_to_download, before_date, include_amends
        )
        total_dl += self.get_sc_13g_filings(
            ticker_or_cik, num_filings_to_download, before_date, include_amends
        )
        total_dl += self.get_sd_filings(
            ticker_or_cik, num_filings_to_download, before_date, include_amends
        )
        return total_dl
