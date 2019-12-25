import re
from collections import namedtuple
from datetime import datetime
from urllib.parse import urlencode

import requests
from lxml import etree

from ._constants import SEC_EDGAR_BASE_URL

FilingMetadata = namedtuple("FilingMetadata", ["filename", "url"])


def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y%m%d")
    except ValueError as e:
        raise Exception(
            "Incorrect date format. Please enter a date string of the form YYYYMMDD."
        ) from e


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
    xml_ns_map = {"w3": "http://www.w3.org/2005/Atom"}
    return xml_root.xpath(xpath_selector, namespaces=xml_ns_map)


def get_filing_urls_to_download(
    ticker_or_cik,
    filing_type,
    num_filings_to_download,
    before_date,
    after_date,
    include_amends,
):
    filing_urls = []
    start = 0
    count = 100

    # loop until:
    # (1) we get more filings than num_filings_to_download
    # (2) there are no more filings to fetch
    while len(filing_urls) < num_filings_to_download:
        qs = form_query_string(start, count, ticker_or_cik, filing_type, before_date)
        edgar_search_url = f"{SEC_EDGAR_BASE_URL}{qs}"

        print(edgar_search_url)

        resp = requests.get(edgar_search_url)
        resp.raise_for_status()

        print('resp.headers["Content-Type"]: ', resp.headers["Content-Type"])

        # Need xpath capabilities of lxml because some entries are mislabeled as
        # 10-K405, for example, which makes an exact match of filing type infeasible
        if include_amends:
            xpath_selector = "//w3:filing-href"
        else:
            xpath_selector = (
                "//w3:filing-type[not(contains(text(), '/A'))]/../w3:filing-href"
            )
        filing_href_elts = extract_elements_from_xml(resp.content, xpath_selector)

        # no more filings available
        if not filing_href_elts:
            break

        filing_urls.extend(filing_href_elts)

        start += count

    # TESTING TODO
    # (1) num_filings_to_download < number of filings available
    # (2) num_filings_to_download > number of filings available
    # (3) num_filings_to_download == number of filings available
    # (4) num_filings_to_download over two pages (e.g. download 30 entries, but count = 20)
    #       => it should fetch 40 entries, but truncate to 30
    # (5) no filings available at all

    # TODO: implement logic for after_date
    return get_metadata_from_href_elts(filing_urls[:num_filings_to_download])


def get_metadata_from_href_elts(filing_href_elts):
    filings_to_fetch = []
    for elt in filing_href_elts:
        search_result_url = elt.text
        edgar_url = re.sub(r"\-index\.html?", ".txt", search_result_url, 1)
        edgar_filename = edgar_url.split("/")[-1]
        filings_to_fetch.append(FilingMetadata(filename=edgar_filename, url=edgar_url))
    return filings_to_fetch
