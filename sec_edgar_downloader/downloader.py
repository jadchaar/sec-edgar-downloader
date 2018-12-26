# TODO: add docstrings to functions
# TODO: spawn a thread for each download. I/O will block so just thread downloads to run in parallel
# TODO: distinguish filing AMENDS (e.g. 8-K/A)?
# TODO: add coloring to the terminal output (e.g. red for errors)

from datetime import date
from bs4 import BeautifulSoup
from pathlib import Path
from collections import namedtuple

import requests
import os
import errno
import json

FilingInfo = namedtuple('FilingInfo', ['filename', 'url'])

class InvalidTickerException(Exception):
    pass

# Load the JSON containing the mapping of valid tickers to the corresponding security name
ticker_validation_json_path = Path.joinpath(Path(__file__).parent, "ticker_validation.json")
with open(ticker_validation_json_path, "r") as f:
    ticker_validation_dict = json.load(f)

class Downloader:
    def __init__(self, download_folder=str(Path.joinpath(Path.home(), "Downloads"))):
        print("Welcome to the SEC EDGAR Downloader!")

        # TODO: should we delete a folder or overrite it when the same data is requested?
        if not Path(download_folder).exists():
            raise IOError(f"The folder for saving company filings ({download_folder}) does not exist.")

        print(f"Company filings will be saved to: {download_folder}")

        self._download_folder = download_folder

        # TODO: Allow users to pass this in
        # Will have to handle pagination since only 100 are displayed on a single page.
        # Requires another start query parameter: start=100&count=100
        self._count = 100
        self._base_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&owner=exclude&count={self._count}"

    def _validate_ticker(self, ticker):
        if ticker not in ticker_validation_dict:
            raise InvalidTickerException(f"The specified ticker ({ticker}) is invalid. Please correct this or enter the stock's CIK.")

    # TODO: allow users to specify before date (by passing in year, month, and day)
    # and formatting it here
    def _form_url(self, ticker, filing_type):
        # Put into required format: YYYYMMDD
        before_date = date.today().strftime('%Y%m%d')
        return f"{self._base_url}&CIK={ticker}&type={filing_type.replace(' ', '+')}&dateb={before_date}"

    def _download_filings(self, edgar_search_url, filing_type, ticker):
        resp = requests.get(edgar_search_url)
        resp.raise_for_status()
        edgar_results_html = resp.content

        edgar_results_scraper = BeautifulSoup(edgar_results_html, "lxml")

        document_anchor_elements = edgar_results_scraper.find_all(id="documentsbutton", href=True)

        sec_base_url = "https://www.sec.gov"
        filing_document_info = []
        for anchor_element in document_anchor_elements:
            filing_detail_url = f"{sec_base_url}{anchor_element['href']}"
            # Some entries end with .html, some end with .htm
            if filing_detail_url[-1] != "l":
                filing_detail_url += 'l'
            full_filing_url = filing_detail_url.replace("-index.html", ".txt")
            name = full_filing_url.split("/")[-1]
            filing_document_info.append(FilingInfo(filename=name, url=full_filing_url))

        if len(filing_document_info) == 0:
            print(f"No {filing_type} documents available for {ticker}.")
            return

        print(f"{len(filing_document_info)} {filing_type} documents available for {ticker}. Beginning download...")

        for doc_info in filing_document_info:
            resp = requests.get(doc_info.url, stream=True)
            resp.raise_for_status()

            save_path = Path(self._download_folder).joinpath("sec-edgar-filings", ticker, filing_type, doc_info.filename)

            # Create all parent directories as needed.
            # For example: if we have /hello and we want to create
            # /hello/world/my/name/is/john.txt, this would create
            # all the directores leading up to john.txt
            if not Path.exists(Path(save_path).parent):
                try:
                    os.makedirs(Path(save_path).parent)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise

            with open(save_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive chunks
                        f.write(chunk)

        print(f"All {filing_type}s for {ticker} downloaded successfully.")

    def _get_filing_wrapper(self, filing_type, ticker_or_cik, is_cik = False):
        ticker_or_cik = str(ticker_or_cik).upper()
        if is_cik:
            # Strip off leading zeroes
            ticker_or_cik = ticker_or_cik.lstrip("0")
        else:
            try:
                self._validate_ticker(ticker_or_cik)
            except InvalidTickerException as e:
                print(e)
                return
        print(f"\nGetting {filing_type} filings for {ticker_or_cik}.")
        filing_url = self._form_url(ticker_or_cik, filing_type)
        self._download_filings(filing_url, filing_type, ticker_or_cik)

    #########################
    ########## 8-K ##########

    def get_8k_filing_for_ticker(self, ticker):
        filing_type = "8-K"
        self._get_filing_wrapper(filing_type, ticker)

    def get_8k_filing_for_cik(self, cik):
        filing_type = "8-K"
        self._get_filing_wrapper(filing_type, cik, True)

    ########## 8-K ##########
    #########################

    ##########################
    ########## 10-K ##########

    def get_10k_filing_for_ticker(self, ticker):
        filing_type = "10-K"
        self._get_filing_wrapper(filing_type, ticker)

    def get_10k_filing_for_cik(self, cik):
        filing_type = "10-K"
        self._get_filing_wrapper(filing_type, cik, True)

    ########## 10-K ##########
    ##########################

    ##########################
    ########## 10-Q ##########

    def get_10q_filing_for_ticker(self, ticker):
        filing_type = "10-Q"
        self._get_filing_wrapper(filing_type, ticker)

    def get_10q_filing_for_cik(self, cik):
        filing_type = "10-Q"
        self._get_filing_wrapper(filing_type, cik, True)

    ########## 10-Q ##########
    ##########################

    #########################
    ########## 13F ##########

    def get_13f_filing_for_ticker(self, ticker):
        filing_type = "13F"
        self._get_filing_wrapper(filing_type, ticker)

    def get_13f_filing_for_cik(self, cik):
        filing_type = "13F"
        self._get_filing_wrapper(filing_type, cik, True)

    ########## 13F ##########
    #########################

    ############################
    ########## SC 13G ##########

    def get_sc_13g_filing_for_ticker(self, ticker):
        filing_type = "SC 13G"
        self._get_filing_wrapper(filing_type, ticker)

    def get_sc_13g_filing_for_cik(self, cik):
        filing_type = "SC 13G"
        self._get_filing_wrapper(filing_type, cik, True)

    ########## SC 13G ##########
    ############################

    ########################
    ########## SD ##########

    def get_sd_filing_for_ticker(self, ticker):
        filing_type = "SD"
        self._get_filing_wrapper(filing_type, ticker)

    def get_sd_filing_for_cik(self, cik):
        filing_type = "SD"
        self._get_filing_wrapper(filing_type, cik, True)

    ########## SD ##########
    ########################

    def get_all_available_filings_for_ticker(self, ticker):
        # Validation must be done early here to prevent
        # the error message from printing multiple times
        ticker = ticker.upper()
        try:
            self._validate_ticker(ticker)
        except InvalidTickerException as e:
            print(e)
            return
        self.get_8k_filing_for_ticker(ticker)
        self.get_10k_filing_for_ticker(ticker)
        self.get_10q_filing_for_ticker(ticker)
        self.get_13f_filing_for_ticker(ticker)
        self.get_sc_13g_filing_for_ticker(ticker)
        self.get_sd_filing_for_ticker(ticker)

    def get_all_available_filings_for_cik(self, cik):
        self.get_10k_filing_for_cik(cik)
        self.get_10k_filing_for_cik(cik)
        self.get_10q_filing_for_cik(cik)
        self.get_13f_filing_for_cik(cik)
        self.get_sc_13g_filing_for_cik(cik)
        self.get_sd_filing_for_cik(cik)

    def get_all_available_filings_for_ticker_list(self, ticker_list):
        for ticker in ticker_list:
            self.get_all_available_filings_for_ticker(ticker)

    def get_all_available_filings_for_cik_list(self, cik_list):
        for cik in cik_list:
            self.get_all_available_filings_for_cik(cik)
