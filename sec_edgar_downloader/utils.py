import xml.etree.ElementTree as ET
from collections import namedtuple
from datetime import datetime

import requests

FilingInfo = namedtuple("FilingInfo", ["filename", "url"])


def parse_edgar_rss_feed(edgar_search_url, num_filings_to_download):
    resp = requests.get(edgar_search_url)
    resp.raise_for_status()

    # If the Content-Type is text/html, no filings were found
    # for the entered search query (e.g. No matching Ticker Symbol)
    if resp.headers["Content-Type"] != "application/atom+xml":
        return []

    xml_root = ET.ElementTree(ET.fromstring(resp.content))
    xml_ns_map = {"w3": "http://www.w3.org/2005/Atom"}
    filing_href_elts = xml_root.findall(".//w3:filing-href", namespaces=xml_ns_map)[
        :num_filings_to_download
    ]

    # https://docs.python.org/3.7/library/xml.etree.elementtree.html#supported-xpath-syntax
    # [.='10-K'] is not compatible with Python 3.6
    # filing_href_elts = xml_root.findall(
    #     ".//w3:filing-type[.='10-K']/../w3:filing-href", namespaces=xml_ns_map
    # )[:100]

    # works on python 3.6 and up
    # filing_href_elts = xml_root.findall(
    #     ".//w3:content[w3:filing-type='10-K']/w3:filing-href", namespaces=xml_ns_map
    # )[:100]

    filing_info = []
    for elt in filing_href_elts:
        search_result_url = elt.text
        if search_result_url[-1] != "l":  # pragma: no branch
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
            "Incorrect before_date format. Please enter a date of the form YYYYMMDD."
        ) from e
