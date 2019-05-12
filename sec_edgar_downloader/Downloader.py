from collections import namedtuple
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
import requests

FilingInfo = namedtuple("FilingInfo", ["filename", "url"])


class Downloader:
    def __init__(self, download_folder=Path.home().joinpath("Downloads")):
        print("Welcome to the SEC EDGAR Downloader!")

        self._download_folder = Path(download_folder)

        if not self._download_folder.exists():
            raise IOError(f"The folder for saving company filings ({self._download_folder}) does not exist.")

        print(f"Company filings will be saved to: {self._download_folder}")

        # TODO: Allow users to pass this in
        # Will have to handle pagination since only 100 are displayed on a single page.
        # Requires another start query parameter: start=100&count=100
        self._count = 100
        self._base_url = "https://www.sec.gov/cgi-bin/browse-edgar" \
            f"?action=getcompany&owner=exclude&count={self._count}"

    # TODO: allow users to specify before date (by passing in year, month, and day) and format it here
    def _form_url(self, ticker, filing_type):
        # Put into required format: YYYYMMDD
        before_date = date.today().strftime("%Y%m%d")
        return f"{self._base_url}&CIK={ticker}&type={filing_type.replace(' ', '+')}&dateb={before_date}"

    def _download_filings(self, edgar_search_url, filing_type, ticker, num_filings_to_download):
        resp = requests.get(edgar_search_url)
        resp.raise_for_status()
        edgar_results_html = resp.content

        edgar_results_scraper = BeautifulSoup(edgar_results_html, "lxml")

        document_anchor_elements = edgar_results_scraper.find_all(
            id="documentsbutton", href=True)[:num_filings_to_download]

        sec_base_url = "https://www.sec.gov"
        filing_document_info = []
        for anchor_element in document_anchor_elements:
            filing_detail_url = f"{sec_base_url}{anchor_element['href']}"
            # Some entries end with .html, some end with .htm
            if filing_detail_url[-1] != "l":
                filing_detail_url += "l"
            full_filing_url = filing_detail_url.replace("-index.html", ".txt")
            name = full_filing_url.split("/")[-1]
            filing_document_info.append(FilingInfo(filename=name, url=full_filing_url))

        # number of filings available may be less than the number requested
        num_filings_to_download = len(filing_document_info)

        if num_filings_to_download == 0:
            print(f"No {filing_type} documents available for {ticker}.")
            return 0

        print(f"{num_filings_to_download} {filing_type} documents available for {ticker}. Beginning download...")

        for doc_info in filing_document_info:
            resp = requests.get(doc_info.url, stream=True)
            resp.raise_for_status()

            save_path = self._download_folder.joinpath("sec_edgar_filings", ticker, filing_type, doc_info.filename)

            # Create all parent directories as needed. For example, if we have the
            # directory /hello and we want to create /hello/world/my/name/is/bob.txt,
            # this would create all the directories leading up to bob.txt.
            save_path.parent.mkdir(parents=True, exist_ok=True)

            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive chunks
                        f.write(chunk)

        print(f"{filing_type} filings for {ticker} downloaded successfully.")

        return num_filings_to_download

    def _get_filing_wrapper(self, filing_type, ticker_or_cik, num_filings_to_download):
        num_filings_to_download = int(num_filings_to_download)
        if num_filings_to_download < 1:
            raise ValueError("Please enter a number greater than 1 for the number of filings to download.")
        ticker_or_cik = str(ticker_or_cik).strip().upper().lstrip("0")
        print(f"\nGetting {filing_type} filings for {ticker_or_cik}.")
        filing_url = self._form_url(ticker_or_cik, filing_type)
        return self._download_filings(filing_url, filing_type, ticker_or_cik, num_filings_to_download)

    '''
    Generic download methods
    '''

    def get_8k_filings(self, ticker_or_cik, num_filings_to_download=100):
        filing_type = "8-K"
        return self._get_filing_wrapper(filing_type, ticker_or_cik, num_filings_to_download)

    def get_10k_filings(self, ticker_or_cik, num_filings_to_download=100):
        filing_type = "10-K"
        return self._get_filing_wrapper(filing_type, ticker_or_cik, num_filings_to_download)

    def get_10q_filings(self, ticker_or_cik, num_filings_to_download=100):
        filing_type = "10-Q"
        return self._get_filing_wrapper(filing_type, ticker_or_cik, num_filings_to_download)

    # Differences explained here: https://www.sec.gov/divisions/investment/13ffaq.htm
    def get_13f_nt_filings(self, ticker_or_cik, num_filings_to_download=100):
        filing_type = "13F-NT"
        return self._get_filing_wrapper(filing_type, ticker_or_cik, num_filings_to_download)

    def get_13f_hr_filings(self, ticker_or_cik, num_filings_to_download=100):
        filing_type = "13F-HR"
        return self._get_filing_wrapper(filing_type, ticker_or_cik, num_filings_to_download)

    def get_sc_13g_filings(self, ticker_or_cik, num_filings_to_download=100):
        filing_type = "SC 13G"
        return self._get_filing_wrapper(filing_type, ticker_or_cik, num_filings_to_download)

    def get_sd_filings(self, ticker_or_cik, num_filings_to_download=100):
        filing_type = "SD"
        return self._get_filing_wrapper(filing_type, ticker_or_cik, num_filings_to_download)

    '''
    Bulk download methods
    '''

    def get_all_available_filings(self, ticker_or_cik, num_filings_to_download=100):
        total_dl = 0
        total_dl += self.get_8k_filings(ticker_or_cik, num_filings_to_download)
        total_dl += self.get_10k_filings(ticker_or_cik, num_filings_to_download)
        total_dl += self.get_10q_filings(ticker_or_cik, num_filings_to_download)
        total_dl += self.get_13f_nt_filings(ticker_or_cik, num_filings_to_download)
        total_dl += self.get_13f_hr_filings(ticker_or_cik, num_filings_to_download)
        total_dl += self.get_sc_13g_filings(ticker_or_cik, num_filings_to_download)
        total_dl += self.get_sd_filings(ticker_or_cik, num_filings_to_download)
        return total_dl


"""
* 2.0.0 release goals
! TODO: distinguish filing amendments (e.g. 8-K/A) - allow user to pass in argument for whether or not to include them.
        If we do distinguish amendments, remember to update tests with new arguments
! TODO: add Sphinx docstrings to functions
! TODO: host documentation on readthedocs
! TODO: allow users to pass in before dates
! TODO: ability to mute print statements
! TODO: investigate running tests on Windows as well to ensure file system works properly
        https://docs.travis-ci.com/user/languages/python/#running-python-tests-on-multiple-operating-systems

* Stretch goals
TODO: add coloring to the terminal output (e.g. red for errors)

* Backlog
TODO: counts beyond 100 (e.g. if a company has more than 100 filings of a particular type)
TODO: add "caching" to prevent overriding previous downloads (if already downloaded, skip)
TODO: spawn a thread for each download. I/O will block so just thread downloads to run in parallel
"""
