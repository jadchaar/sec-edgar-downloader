"""Utility functions for the downloader class."""

import re
import time
from collections import namedtuple
from datetime import datetime
from urllib.parse import urlencode

import requests
from lxml import etree

from ._constants import SEC_EDGAR_BASE_URL, W3_NAMESPACE

FilingMetadata = namedtuple("FilingMetadata", ["filename", "url"])


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y%m%d")
    except ValueError:
        raise ValueError(
            "Incorrect date format. Please enter a date string of the form YYYYMMDD."
        )


def form_query_string(start, count, ticker_or_cik, filing_type, before_date):
    query_params = {
        "action": "getcompany",
        "owner": "exclude",
        "start": start,
        "count": count,
        "CIK": ticker_or_cik,
        "type": filing_type,
        "dateb": before_date,
        "output": "atom",
    }
    return urlencode(query_params)


def extract_elements_from_xml(xml_byte_object, xpath_selector):
    xml_root = etree.fromstring(xml_byte_object)
    return xml_root.xpath(xpath_selector, namespaces=W3_NAMESPACE)


def get_filing_urls_to_download(
    filing_type,
    ticker_or_cik,
    num_filings_to_download,
    after_date,
    before_date,
    include_amends,
):
    filings_to_fetch = []
    start = 0
    count = 100

    # loop until:
    # (1) we get more filings than num_filings_to_download
    # (2) there are no more filings to fetch
    while len(filings_to_fetch) < num_filings_to_download:
        qs = form_query_string(start, count, ticker_or_cik, filing_type, before_date)
        edgar_search_url = f"{SEC_EDGAR_BASE_URL}{qs}"

        resp = requests.get(edgar_search_url)
        resp.raise_for_status()

        # An HTML page is returned when an invalid ticker is entered
        # Filter out non-XML responses
        if resp.headers["Content-Type"] != "application/atom+xml":
            return []

        # Need xpath capabilities of lxml because some entries are mislabeled as
        # 10-K405, for example, which makes an exact match of filing type infeasible
        if include_amends:
            xpath_selector = "//w3:content"
        else:
            xpath_selector = "//w3:filing-type[not(contains(text(), '/A'))]/.."

        filing_entry_elts = extract_elements_from_xml(resp.content, xpath_selector)

        # no more filings available
        if not filing_entry_elts:
            break

        for elt in filing_entry_elts:
            # after date constraint needs to be checked if it is passed in
            if after_date is not None:
                filing_date = elt.findtext("w3:filing-date", namespaces=W3_NAMESPACE)
                filing_date = filing_date.replace("-", "", 2)
                if filing_date < after_date:
                    return filings_to_fetch[:num_filings_to_download]

            search_result_url = elt.findtext("w3:filing-href", namespaces=W3_NAMESPACE)
            edgar_url = re.sub(r"\-index\.html?", ".txt", search_result_url, 1)
            edgar_filename = edgar_url.split("/")[-1]
            filings_to_fetch.append(
                FilingMetadata(filename=edgar_filename, url=edgar_url)
            )

        start += count

    return filings_to_fetch[:num_filings_to_download]


def download_filings(download_folder, ticker_or_cik, filing_type, filings_to_fetch):
    for filing in filings_to_fetch:
        resp = requests.get(filing.url)
        resp.raise_for_status()

        save_path = download_folder.joinpath(
            "sec_edgar_filings", ticker_or_cik, filing_type, filing.filename
        )

        # Create all parent directories as needed
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(resp.text)

        # SEC limits users to 10 downloads per second
        # Sleep >0.10s between each download to prevent rate-limiting
        # https://github.com/jadchaar/sec-edgar-downloader/issues/24
        time.sleep(0.15)
