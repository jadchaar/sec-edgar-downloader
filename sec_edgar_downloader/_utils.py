"""Utility functions for the downloader class."""
import time
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from faker import Faker
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ._constants import (
    DATE_FORMAT_TOKENS,
    FILING_DETAILS_FILENAME_STEM,
    FILING_FULL_SUBMISSION_FILENAME,
    MAX_RETRIES,
    ROOT_SAVE_FOLDER_NAME,
    SEC_EDGAR_ARCHIVES_BASE_URL,
    SEC_EDGAR_RATE_LIMIT_SLEEP_INTERVAL,
    SEC_EDGAR_SEARCH_API_ENDPOINT,
)


class EdgarSearchApiError(Exception):
    """Error raised when Edgar Search API encounters a problem."""


# Object for storing metadata about filings that will be downloaded.
FilingMetadata = namedtuple(
    "FilingMetadata",
    [
        "accession_number",
        "full_submission_url",
        "filing_details_url",
        "filing_details_filename",
    ],
)

# Object for generating fake user-agent strings
fake = Faker()

# Specify max number of request retries
# https://stackoverflow.com/a/35504626/3820660
retries = Retry(
    total=MAX_RETRIES,
    backoff_factor=SEC_EDGAR_RATE_LIMIT_SLEEP_INTERVAL,
    status_forcelist=[403, 500, 502, 503, 504],
)


def validate_date_format(date_format: str) -> None:
    error_msg_base = "Please enter a date string of the form YYYY-MM-DD."

    if not isinstance(date_format, str):
        raise TypeError(error_msg_base)

    try:
        datetime.strptime(date_format, DATE_FORMAT_TOKENS)
    except ValueError as exc:
        # Re-raise with custom error message
        raise ValueError(f"Incorrect date format. {error_msg_base}") from exc


def form_request_payload(
    ticker_or_cik: str,
    filing_types: List[str],
    start_date: str,
    end_date: str,
    start_index: int,
    query: str,
) -> dict:
    payload = {
        "dateRange": "custom",
        "startdt": start_date,
        "enddt": end_date,
        "entityName": ticker_or_cik,
        "forms": filing_types,
        "from": start_index,
        "q": query,
    }
    return payload


def build_filing_metadata_from_hit(hit: dict) -> FilingMetadata:
    accession_number, filing_details_filename = hit["_id"].split(":", 1)
    # Company CIK should be last in the CIK list. This list may also include
    # the CIKs of executives carrying out insider transactions like in form 4.
    cik = hit["_source"]["ciks"][-1]
    accession_number_no_dashes = accession_number.replace("-", "", 2)

    submission_base_url = (
        f"{SEC_EDGAR_ARCHIVES_BASE_URL}/{cik}/{accession_number_no_dashes}"
    )

    full_submission_url = f"{submission_base_url}/{accession_number}.txt"

    # Get XSL if human readable is wanted
    # XSL is required to download the human-readable
    # and styled version of XML documents like form 4
    # SEC_EDGAR_ARCHIVES_BASE_URL + /320193/000032019320000066/wf-form4_159839550969947.xml
    # SEC_EDGAR_ARCHIVES_BASE_URL +
    #           /320193/000032019320000066/xslF345X03/wf-form4_159839550969947.xml

    # xsl = hit["_source"]["xsl"]
    # if xsl is not None:
    #     filing_details_url = f"{submission_base_url}/{xsl}/{filing_details_filename}"
    # else:
    #     filing_details_url = f"{submission_base_url}/{filing_details_filename}"

    filing_details_url = f"{submission_base_url}/{filing_details_filename}"

    filing_details_filename_extension = Path(filing_details_filename).suffix.replace(
        "htm", "html"
    )
    filing_details_filename = (
        f"{FILING_DETAILS_FILENAME_STEM}{filing_details_filename_extension}"
    )

    return FilingMetadata(
        accession_number=accession_number,
        full_submission_url=full_submission_url,
        filing_details_url=filing_details_url,
        filing_details_filename=filing_details_filename,
    )


def get_filing_urls_to_download(
    filing_type: str,
    ticker_or_cik: str,
    num_filings_to_download: int,
    after_date: str,
    before_date: str,
    include_amends: bool,
    query: str = "",
) -> List[FilingMetadata]:
    filings_to_fetch: List[FilingMetadata] = []
    start_index = 0

    client = requests.Session()
    client.mount("http://", HTTPAdapter(max_retries=retries))
    client.mount("https://", HTTPAdapter(max_retries=retries))
    try:
        while len(filings_to_fetch) < num_filings_to_download:
            payload = form_request_payload(
                ticker_or_cik,
                [filing_type],
                after_date,
                before_date,
                start_index,
                query,
            )
            headers = {
                "User-Agent": generate_random_user_agent(),
                "Accept-Encoding": "gzip, deflate",
                "Host": "efts.sec.gov",
            }
            resp = client.post(
                SEC_EDGAR_SEARCH_API_ENDPOINT, json=payload, headers=headers
            )
            resp.raise_for_status()
            search_query_results = resp.json()

            if "error" in search_query_results:
                try:
                    root_cause = search_query_results["error"]["root_cause"]
                    if not root_cause:  # pragma: no cover
                        raise ValueError

                    error_reason = root_cause[0]["reason"]
                    raise EdgarSearchApiError(
                        f"Edgar Search API encountered an error: {error_reason}. "
                        f"Request payload:\n{payload}"
                    )
                except (ValueError, KeyError):  # pragma: no cover
                    raise EdgarSearchApiError(
                        "Edgar Search API encountered an unknown error. "
                        f"Request payload:\n{payload}"
                    ) from None

            query_hits = search_query_results["hits"]["hits"]

            # No more results to process
            if not query_hits:
                break

            for hit in query_hits:
                hit_filing_type = hit["_source"]["file_type"]

                is_amend = hit_filing_type[-2:] == "/A"
                if not include_amends and is_amend:
                    continue

                # Work around bug where incorrect filings are sometimes included.
                # For example, AAPL 8-K searches include N-Q entries.
                if not is_amend and hit_filing_type != filing_type:
                    continue

                metadata = build_filing_metadata_from_hit(hit)
                filings_to_fetch.append(metadata)

                if len(filings_to_fetch) == num_filings_to_download:
                    return filings_to_fetch

            # Edgar queries 100 entries at a time, but it is best to set this
            # from the response payload in case it changes in the future
            query_size = search_query_results["query"]["size"]
            start_index += query_size

            # Prevent rate limiting
            time.sleep(SEC_EDGAR_RATE_LIMIT_SLEEP_INTERVAL)
    finally:
        client.close()

    return filings_to_fetch


def resolve_relative_urls_in_filing(filing_text: str, download_url: str) -> str:
    soup = BeautifulSoup(filing_text, "lxml")
    base_url = f"{download_url.rsplit('/', 1)[0]}/"

    for url in soup.find_all("a", href=True):
        # Do not resolve a URL if it is a fragment or it already contains a full URL
        if url["href"].startswith("#") or url["href"].startswith("http"):
            continue
        url["href"] = urljoin(base_url, url["href"])

    for image in soup.find_all("img", src=True):
        image["src"] = urljoin(base_url, image["src"])

    if soup.original_encoding is None:  # pragma: no cover
        return soup

    return soup.encode(soup.original_encoding)


def download_and_save_filing(
    client: requests.Session,
    download_folder: Path,
    ticker_or_cik: str,
    accession_number: str,
    filing_type: str,
    download_url: str,
    save_filename: str,
    *,
    resolve_urls: bool = False,
) -> None:
    headers = {
        "User-Agent": generate_random_user_agent(),
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov",
    }
    resp = client.get(download_url, headers=headers)
    resp.raise_for_status()
    filing_text = resp.content

    # Only resolve URLs in HTML files
    if resolve_urls and Path(save_filename).suffix == ".html":
        filing_text = resolve_relative_urls_in_filing(filing_text, download_url)

    # Create all parent directories as needed and write content to file
    save_path = (
        download_folder
        / ROOT_SAVE_FOLDER_NAME
        / ticker_or_cik
        / filing_type
        / accession_number
        / save_filename
    )
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(filing_text)

    # Prevent rate limiting
    time.sleep(SEC_EDGAR_RATE_LIMIT_SLEEP_INTERVAL)


def download_filings(
    download_folder: Path,
    ticker_or_cik: str,
    filing_type: str,
    filings_to_fetch: List[FilingMetadata],
    include_filing_details: bool,
) -> None:
    client = requests.Session()
    client.mount("http://", HTTPAdapter(max_retries=retries))
    client.mount("https://", HTTPAdapter(max_retries=retries))
    try:
        for filing in filings_to_fetch:
            try:
                download_and_save_filing(
                    client,
                    download_folder,
                    ticker_or_cik,
                    filing.accession_number,
                    filing_type,
                    filing.full_submission_url,
                    FILING_FULL_SUBMISSION_FILENAME,
                )
            except requests.exceptions.HTTPError as e:  # pragma: no cover
                print(
                    "Skipping full submission download for "
                    f"'{filing.accession_number}' due to network error: {e}."
                )

            if include_filing_details:
                try:
                    download_and_save_filing(
                        client,
                        download_folder,
                        ticker_or_cik,
                        filing.accession_number,
                        filing_type,
                        filing.filing_details_url,
                        filing.filing_details_filename,
                        resolve_urls=True,
                    )
                except requests.exceptions.HTTPError as e:  # pragma: no cover
                    print(
                        f"Skipping filing detail download for "
                        f"'{filing.accession_number}' due to network error: {e}."
                    )
    finally:
        client.close()


def get_number_of_unique_filings(filings: List[FilingMetadata]) -> int:
    return len({metadata.accession_number for metadata in filings})


def generate_random_user_agent() -> str:
    return f"{fake.first_name()} {fake.last_name()} {fake.email()}"


def is_cik(ticker_or_cik: str) -> bool:
    try:
        int(ticker_or_cik)
        return True
    except ValueError:
        return False
