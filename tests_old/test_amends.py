"""Tests downloads with and without the filing amends included."""

import requests

from sec_edgar_downloader._utils import extract_elements_from_xml


def test_include_amends_from_xml(apple_10k_edgar_search_xml_url):
    resp = requests.get(apple_10k_edgar_search_xml_url)
    assert resp.ok

    xpath_selector = "//w3:filing-href"
    filing_href_elts = extract_elements_from_xml(resp.content, xpath_selector)
    assert len(filing_href_elts) == 27

    xpath_selector = "//w3:filing-type"
    filing_types = [
        elt.text for elt in extract_elements_from_xml(resp.content, xpath_selector)
    ]
    assert all("10-K" in ft for ft in filing_types)


def test_exclude_amends_from_xml(apple_10k_edgar_search_xml_url):
    resp = requests.get(apple_10k_edgar_search_xml_url)
    assert resp.ok

    xpath_selector = "//w3:filing-type[not(contains(text(), '/A'))]/../w3:filing-href"
    filing_href_elts = extract_elements_from_xml(resp.content, xpath_selector)
    assert len(filing_href_elts) == 25

    xpath_selector = "//w3:filing-type[not(contains(text(), '/A'))]"
    filing_types = [
        elt.text for elt in extract_elements_from_xml(resp.content, xpath_selector)
    ]
    assert all(("10-K" in ft and "/A" not in ft) for ft in filing_types)


def test_include_amends_filing_retrieval(downloader, apple_filing_metadata):
    dl, download_folder_base = downloader

    # AAPL has 1 SG-13G filing and 2 SG-13G/A before 19940218
    num_downloaded = dl.get_sc_13g_filings(
        apple_filing_metadata["symbol"], 3, "19940218", True
    )
    assert num_downloaded == 3


def test_exclude_amends_filing_retrieval(downloader, apple_filing_metadata):
    dl, download_folder_base = downloader

    # AAPL has 1 SG-13G filing and 2 SG-13G/A before 19940218
    num_downloaded = dl.get_sc_13g_filings(
        apple_filing_metadata["symbol"], 3, "19940218", False
    )
    assert num_downloaded == 1
