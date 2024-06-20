from collections import deque
from pathlib import Path
from typing import Any, Dict, List

from ._constants import (
    AMENDS_SUFFIX,
    CIK_LENGTH,
    FILING_FULL_SUBMISSION_FILENAME,
    PRIMARY_DOC_FILENAME_STEM,
    ROOT_SAVE_FOLDER_NAME,
    SUBMISSION_FILE_FORMAT,
    URL_FILING,
    URL_SUBMISSIONS,
)
from ._sec_gateway import (
    download_filing,
    get_list_of_available_filings,
    get_ticker_metadata,
)
from ._types import DownloadMetadata, ToDownload
from ._utils import within_requested_date_range


def get_save_location(
    download_metadata: DownloadMetadata,
    accession_number: str,
    save_filename: str,
) -> Path:
    company_identifier = (
        download_metadata.ticker
        if download_metadata.ticker is not None
        else download_metadata.cik
    )
    return (
        download_metadata.download_folder
        / ROOT_SAVE_FOLDER_NAME
        / company_identifier
        / download_metadata.form
        / accession_number
        / save_filename
    )


def save_document(filing_contents: Any, save_path: Path) -> None:
    # TODO: resolve URLs so that images show up in HTML files?
    # Create all parent directories as needed and write content to file
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(filing_contents)


def aggregate_filings_to_download(
    download_metadata: DownloadMetadata, user_agent: str
) -> List[ToDownload]:
    filings_to_download: List[ToDownload] = []
    fetched_count = 0
    submissions_uri = URL_SUBMISSIONS.format(
        submission=SUBMISSION_FILE_FORMAT.format(cik=download_metadata.cik)
    )
    additional_submissions = None

    while fetched_count < download_metadata.limit:
        resp_json = get_list_of_available_filings(submissions_uri, user_agent)
        # First API response is different from further API responses
        if additional_submissions is None:
            filings_json = resp_json["filings"]["recent"]
            additional_submissions = deque(resp_json["filings"]["files"])
        # On second page or more of API response (for companies with >1000 filings)
        else:
            filings_json = resp_json

        accession_numbers = filings_json["accessionNumber"]
        forms = filings_json["form"]
        documents = filings_json["primaryDocument"]
        filing_dates = filings_json["filingDate"]

        for acc_num, form, doc, f_date in zip(  # noqa: B905
            accession_numbers, forms, documents, filing_dates
        ):
            is_amend = form.endswith(AMENDS_SUFFIX)
            form = form[:-2] if is_amend else form
            if (
                form != download_metadata.form
                or (not download_metadata.include_amends and is_amend)
                or not within_requested_date_range(download_metadata, f_date)
            ):
                continue

            filings_to_download.append(
                get_to_download(download_metadata.cik, acc_num, doc)
            )

            fetched_count += 1

            # We have reached the requested download limit, so break inner for loop
            # early and allow the outer while loop to break.
            if fetched_count == download_metadata.limit:
                break

        if len(additional_submissions) == 0:
            break

        next_page = additional_submissions.popleft()["name"]
        submissions_uri = URL_SUBMISSIONS.format(submission=next_page)

    return filings_to_download


def get_to_download(cik: str, acc_num: str, doc: str) -> ToDownload:
    cik = cik.lstrip("0")
    acc_num_no_dash = acc_num.replace("-", "")
    raw_filing_uri = URL_FILING.format(
        cik=cik, acc_num_no_dash=acc_num_no_dash, document=f"{acc_num}.txt"
    )
    # Primary documents are returned with XSL prepended, which inhibits the
    # ability to download raw XMLs. Need to strip away the leading prepended
    # XSL metadata component to obtain the proper file to download.
    primary_doc_uri = URL_FILING.format(
        cik=cik, acc_num_no_dash=acc_num_no_dash, document=doc.rsplit("/")[-1]
    )
    primary_doc_suffix = Path(doc).suffix.replace("htm", "html")

    return ToDownload(
        raw_filing_uri,
        primary_doc_uri,
        acc_num,
        primary_doc_suffix,
    )


def fetch_and_save_filings(download_metadata: DownloadMetadata, user_agent: str) -> int:
    successfully_downloaded = 0
    to_download = aggregate_filings_to_download(download_metadata, user_agent)
    if download_metadata.accession_numbers_to_skip is not None:
        to_download = [
            td
            for td in to_download
            if td.accession_number not in download_metadata.accession_numbers_to_skip
        ]

    for td in to_download:
        try:
            save_location = get_save_location(
                download_metadata, td.accession_number, FILING_FULL_SUBMISSION_FILENAME
            )
            if not save_location.exists():
                raw_filing = download_filing(td.raw_filing_uri, user_agent)
                save_document(raw_filing, save_location)

            if download_metadata.download_details:
                primary_doc_filename = (
                    f"{PRIMARY_DOC_FILENAME_STEM}{td.details_doc_suffix}"
                )
                save_location = get_save_location(
                    download_metadata, td.accession_number, primary_doc_filename
                )
                if not save_location.exists():
                    primary_doc = download_filing(td.primary_doc_uri, user_agent)
                    save_document(primary_doc, save_location)
        except Exception as e:
            print(
                "Error occurred while downloading filing for accession number {}: {}",
                td.accession_number,
                e,
            )
            continue

        successfully_downloaded += 1

    return successfully_downloaded


def get_ticker_to_cik_mapping(user_agent: str) -> Dict[str, str]:
    ticker_metadata = get_ticker_metadata(user_agent)
    fields = ticker_metadata["fields"]
    ticker_data = ticker_metadata["data"]

    # Find index that corresponds with the CIK and ticker fields
    cik_idx = fields.index("cik")
    ticker_idx = fields.index("ticker")

    return {
        str(td[ticker_idx]).upper(): str(td[cik_idx]).zfill(CIK_LENGTH)
        for td in ticker_data
    }
