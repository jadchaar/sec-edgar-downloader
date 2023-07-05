import requests
from ._types import DownloadMetadata, DownloadType, FilingMetadata, ToDownload
from typing import Any, List
from pathlib import Path
from pyrate_limiter import Duration, RequestRate, Limiter
from collections import deque

# 10 requests per second rate limit set by SEC:
# https://www.sec.gov/os/webmaster-faq#developers
second_rate = RequestRate(10, Duration.SECOND)
limiter = Limiter(second_rate)

FILING_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc_num_no_dash}/{document}"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/{submission}"
SUBMISSION_FILE_FORMAT = "CIK{cik}.json"
STANDARD_HEADERS = {
    "Accept-Encoding": "gzip, deflate",
}


# Save metadata
ROOT_SAVE_FOLDER_NAME = "sec-edgar-filings"
FILING_FULL_SUBMISSION_FILENAME = "full-submission.txt"
PRIMARY_DOC_FILENAME_STEM = "primary-document"

# TODO: improve typing of response (don't use Any)
@limiter.ratelimit('sec_rate_limit', delay=True)
def fetch_from_sec(uri: str, user_agent: str, download_type: DownloadType) -> Any:
    # TODO: add global rate limiting method for submissions + filing downloads
    resp = requests.get(uri, headers={
        **STANDARD_HEADERS,
        "User-Agent": user_agent,
        "Host": "data.sec.gov" if download_type == "EdgarAPI" else "www.sec.gov",
    })
    resp.raise_for_status()
    return resp.json() if download_type == "EdgarAPI" else resp.content


def save_document(
        filing_text: Any,
        download_metadata: DownloadMetadata,
        filing_metadata: FilingMetadata,
) -> None:
    # Create all parent directories as needed and write content to file
    save_path = (
        download_metadata.download_folder
        / ROOT_SAVE_FOLDER_NAME
        / download_metadata.cik
        / download_metadata.form
        / filing_metadata.accession_number
        / filing_metadata.save_filename
    )
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(filing_text)



# def get_filings(download_metadata: DownloadMetadata, user_agent: str) -> None:
#     submissions_uri = SUBMISSIONS_URL.format(submission=SUBMISSION_FILE_FORMAT.format(cik=download_metadata.cik))
#     resp_json = fetch_from_sec(submissions_uri, user_agent, "EdgarAPI")
#     filings_json = resp_json["filings"]['recent']
#
#     accession_numbers = filings_json["accessionNumber"]
#     forms = filings_json["form"]
#     documents = filings_json["primaryDocument"]
#     filing_dates = filings_json["filingDate"]
#
#     fetched_count = 0
#
#     # TODO: handle ignoring amends
#     # TODO: handle date ranges and form types
#
#     for acc_num, form, doc, f_date in zip(accession_numbers, forms, documents, filing_dates):
#         # TODO: need to figure out all cases for date ranges (there should be 4 cases)
#         # both after and before specified
#         # only after specified
#         # only before specified
#         # neither after nor before are specified
#
#         # # Within date range if:
#         # # After and before dates are NOT specified
#         # # OR after date is specified and the filing is after this date (inclusive)
#         # # OR before date is specified and the filing is before this date (inclusive)
#         # within_date_range = (
#         #         (download_metadata.after is None and download_metadata.before is None)
#         #         or (download_metadata.after is not None and f_date >= download_metadata.after)
#         #         or (download_metadata.before is not None and f_date <= download_metadata.before)
#         # )
#         if form != download_metadata.form:
#             continue
#
#         cik = download_metadata.cik.strip("0")
#         acc_num_no_dash = acc_num.replace("-", "")
#         raw_filing_uri = FILING_URL.format(cik=cik, acc_num_no_dash=acc_num_no_dash, document=f"{acc_num}.txt")
#         primary_doc_uri = FILING_URL.format(cik=cik, acc_num_no_dash=acc_num_no_dash, document=doc)
#
#         raw_filing = fetch_from_sec(raw_filing_uri, user_agent, "EdgarFiling")
#         primary_doc = fetch_from_sec(primary_doc_uri, user_agent, "EdgarFiling")
#
#         primary_doc_filename_extension = Path(doc).suffix.replace(
#             "htm", "html"
#         )
#         primary_doc_filename = (
#             f"{PRIMARY_DOC_FILENAME_STEM}{primary_doc_filename_extension}"
#         )
#
#         save_document(
#             raw_filing,
#             download_metadata,
#             FilingMetadata(acc_num, FILING_FULL_SUBMISSION_FILENAME)
#         )
#         save_document(
#             primary_doc,
#             download_metadata,
#             FilingMetadata(acc_num, primary_doc_filename)
#         )
#
#         fetched_count += 1
#
#         if fetched_count == download_metadata.limit:
#             break
#
#         # TODO: add logic for accounting for limits and pagination

def get_filings_to_download(download_metadata: DownloadMetadata, user_agent: str) -> List[ToDownload]:

    filings_to_download: List[ToDownload] = []
    fetched_count = 0
    filings_available = True
    submissions_uri = SUBMISSIONS_URL.format(submission=SUBMISSION_FILE_FORMAT.format(cik=download_metadata.cik))

    # API response changes when querying second route
    on_first_submission_page = True

    additional_submissions = None

    while fetched_count < download_metadata.limit and filings_available:
        resp_json = fetch_from_sec(submissions_uri, user_agent, "EdgarAPI")
        # First API response is different from further API responses
        if additional_submissions is None:
            filings_json = resp_json["filings"]['recent']
            additional_submissions = deque(resp_json["filings"]['files'])
        # On second page or more of API response (for companies with >1000 filings)
        else:
            filings_json = resp_json

        accession_numbers = filings_json["accessionNumber"]
        forms = filings_json["form"]
        documents = filings_json["primaryDocument"]
        filing_dates = filings_json["filingDate"]

        for acc_num, form, doc, f_date in zip(accession_numbers, forms, documents, filing_dates):
            if form != download_metadata.form:
                continue

            cik = download_metadata.cik.strip("0")
            acc_num_no_dash = acc_num.replace("-", "")
            raw_filing_uri = FILING_URL.format(cik=cik, acc_num_no_dash=acc_num_no_dash, document=f"{acc_num}.txt")
            primary_doc_uri = FILING_URL.format(cik=cik, acc_num_no_dash=acc_num_no_dash, document=doc)

            filings_to_download.append(
                ToDownload(
                    raw_filing_uri,
                    primary_doc_uri,
                )
            )

            fetched_count += 1

            # We have reached the requested download limit, so exit early
            if fetched_count == download_metadata.limit:
                return filings_to_download

        if len(additional_submissions) == 0:
            break

        next_page = additional_submissions.popleft()["name"]

        submissions_uri = SUBMISSIONS_URL.format(submission=next_page)

    return filings_to_download
