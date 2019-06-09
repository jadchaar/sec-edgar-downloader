from collections import namedtuple
from datetime import datetime
from urllib.parse import urlencode

import requests
from lxml import etree

FilingInfo = namedtuple("FilingInfo", ["filename", "url"])


# TODO: Allow users to pass in start and count parameters
def form_query_string(ticker, filing_type, before_date):
    query_params = {
        "action": "getcompany",
        "owner": "exclude",
        "start": 0,
        "count": 100,
        "CIK": ticker,
        "type": filing_type,
        "dateb": before_date,
        "output": "atom",
    }
    return urlencode(query_params)


def extract_elements_from_xml(xml_byte_object, xpath_selector):
    xml_root = etree.fromstring(xml_byte_object)
    xml_ns_map = {"w3": "http://www.w3.org/2005/Atom"}
    return xml_root.xpath(xpath_selector, namespaces=xml_ns_map)


def parse_edgar_rss_feed(
    edgar_search_url, num_filings_to_download, filing_type, include_amends
):
    resp = requests.get(edgar_search_url)
    resp.raise_for_status()

    # If the Content-Type is text/html, no filings were found
    # for the entered search query (e.g. No matching Ticker Symbol)
    if resp.headers["Content-Type"] != "application/atom+xml":
        return []

    # Need xpath capabilities of lxml because some entries are mislabeled as
    # 10-K405, for example, which makes an exact match of filing type infeasible
    if include_amends:
        xpath_selector = "//w3:filing-href"
    else:
        xpath_selector = (
            "//w3:filing-type[not(contains(text(), '/A'))]/../w3:filing-href"
        )
    filing_href_elts = extract_elements_from_xml(resp.content, xpath_selector)[
        :num_filings_to_download
    ]

    filing_info = []
    for elt in filing_href_elts:
        search_result_url = elt.text
        if search_result_url[-1] != "l":
            search_result_url += "l"
        filing_url = search_result_url.replace("-index.html", ".txt")
        edgar_filename = filing_url.split("/")[-1]
        filing_info.append(FilingInfo(filename=edgar_filename, url=filing_url))

    return filing_info


def validate_before_date(before_date):
    try:
        datetime.strptime(before_date, "%Y%m%d")
    except ValueError as e:
        raise Exception(
            "Incorrect before_date format. Please enter a date string of the form YYYYMMDD."
        ) from e
