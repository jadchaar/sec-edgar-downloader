import json
import sys
from pathlib import Path
from unittest.mock import patch

from requests.exceptions import RequestException

from sec_edgar_downloader._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE
from sec_edgar_downloader._orchestrator import (
    aggregate_filings_to_download,
    fetch_and_save_filings,
    get_save_location,
    get_ticker_to_cik_mapping,
    get_to_download,
    save_document,
)
from sec_edgar_downloader._types import DownloadMetadata, ToDownload


def test_get_save_location(user_agent, form_10k, apple_cik):
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=1,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=True,
    )
    accession_number = "0000320193-22-000108"
    save_filename = "foobar.txt"

    result = get_save_location(download_metadata, accession_number, save_filename)

    assert result == Path(
        "./sec-edgar-filings/0000320193/10-K/0000320193-22-000108/foobar.txt"
    )


def test_save_document(tmp_path):
    sample_contents = b"example data to write"
    save_path = tmp_path / "foo" / "bar" / "baz" / "filing.txt"
    assert not save_path.exists()

    save_document(sample_contents, save_path)

    assert save_path.exists()
    assert save_path.stat().st_size > 0


def test_aggregate_filings_to_download_given_multiple_pages_and_no_limit(
    user_agent, form_10k, apple_cik, accession_number_to_metadata
):
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=sys.maxsize,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=True,
    )

    with patch(
        "sec_edgar_downloader._sec_gateway.get_list_of_available_filings"
    ) as mock_get_list_of_available_filings:
        mock_get_list_of_available_filings.side_effect = (
            _mock_sec_api_response_multi_page
        )
        result = aggregate_filings_to_download(download_metadata, user_agent)

    assert len(result) == 27
    for td in result:
        acc_num = td.accession_number
        metadata = accession_number_to_metadata[acc_num]
        assert metadata["form"] == form_10k
        assert metadata["filingDate"] >= DEFAULT_AFTER_DATE
        assert metadata["filingDate"] <= DEFAULT_BEFORE_DATE


def test_aggregate_filings_to_download_given_multiple_pages_and_configured_limit(
    user_agent, form_10k, apple_cik
):
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=3,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=True,
    )

    with patch(
        "sec_edgar_downloader._sec_gateway.get_list_of_available_filings"
    ) as mock_get_list_of_available_filings:
        mock_get_list_of_available_filings.side_effect = (
            _mock_sec_api_response_multi_page
        )
        result = aggregate_filings_to_download(download_metadata, user_agent)

    assert len(result) == 3


# TODO: test date ranges
# TODO: test including amends


# def test_aggregate_filings_to_download_given_multiple_pages():
#     assert False


def test_get_to_download_given_xml(apple_cik, accession_number, form_4_primary_doc):
    result = get_to_download(apple_cik, accession_number, form_4_primary_doc)

    assert result.raw_filing_uri == (
        "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/0000320193-22-000108.txt"
    )
    assert result.primary_doc_uri == (
        "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/xslF345X04/wf-form4_168444912415136.xml"
    )
    assert result.accession_number == "0000320193-22-000108"
    assert result.details_doc_suffix == ".xml"


def test_get_to_download_given_html(apple_cik, accession_number, form_8k_primary_doc):
    result = get_to_download(apple_cik, accession_number, form_8k_primary_doc)

    assert result.raw_filing_uri == (
        "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/0000320193-22-000108.txt"
    )
    assert result.primary_doc_uri == (
        "https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/ny20007635x4_8k.htm"
    )
    assert result.accession_number == "0000320193-22-000108"
    assert result.details_doc_suffix == ".html"


def test_fetch_and_save_filings_given_download_details(user_agent, form_10k, apple_cik):
    limit = 2
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=limit,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=True,
    )

    to_download_list = [
        ToDownload(
            raw_filing_uri=f"raw_{i}",
            primary_doc_uri=f"pd_{i}",
            accession_number=f"acc_num_{i}",
            details_doc_suffix=".xml",
        )
        for i in range(limit)
    ]

    with patch(
        "sec_edgar_downloader._orchestrator.aggregate_filings_to_download",
        new=lambda x, y: to_download_list,
    ), patch(
        "sec_edgar_downloader._orchestrator.download_filing",
    ) as mock_download_filing, patch(
        "sec_edgar_downloader._orchestrator.save_document",
    ) as mock_save_document:
        num_downloaded = fetch_and_save_filings(download_metadata, user_agent)

    assert num_downloaded == 2
    assert mock_download_filing.call_count == 4
    assert mock_save_document.call_count == 4

    # Assert URIs
    expected_uris = {td.raw_filing_uri for td in to_download_list} | {
        td.primary_doc_uri for td in to_download_list
    }
    actual_uris = {c.args[0] for c in mock_download_filing.call_args_list}
    assert len(expected_uris) == len(actual_uris) == 4
    assert expected_uris == actual_uris

    # Assert user-agent
    actual_user_agent = {c.args[1] for c in mock_download_filing.call_args_list}
    assert len(actual_user_agent) == 1
    assert actual_user_agent.pop() == user_agent

    # Assert save locations
    expected_acc_nums = {td.accession_number for td in to_download_list}
    paths = [c.args[1] for c in mock_save_document.call_args_list]
    actual_acc_nums = {p.parts[3] for p in paths}
    assert len(actual_acc_nums) == 2
    assert expected_acc_nums == actual_acc_nums

    # Assert filenames
    actual_filenames = [p.name for p in paths]
    assert actual_filenames.count("primary-document.xml") == 2
    assert actual_filenames.count("full-submission.txt") == 2


def test_fetch_and_save_filings_skip_download_details(user_agent, form_10k, apple_cik):
    limit = 2
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=limit,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=False,
    )

    to_download_list = [
        ToDownload(
            raw_filing_uri=f"raw_{i}",
            primary_doc_uri=f"pd_{i}",
            accession_number=f"acc_num_{i}",
            details_doc_suffix=".xml",
        )
        for i in range(limit)
    ]

    with patch(
        "sec_edgar_downloader._orchestrator.aggregate_filings_to_download",
        new=lambda x, y: to_download_list,
    ), patch(
        "sec_edgar_downloader._orchestrator.download_filing",
    ) as mock_download_filing, patch(
        "sec_edgar_downloader._orchestrator.save_document",
    ) as mock_save_document:
        num_downloaded = fetch_and_save_filings(download_metadata, user_agent)

    assert num_downloaded == 2
    assert mock_download_filing.call_count == 2
    assert mock_save_document.call_count == 2


def test_fetch_and_save_filings_given_paths_that_already_exist(
    user_agent, form_10k, apple_cik
):
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=1,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=False,
    )

    with patch.object(Path, "exists") as mock_exists, patch(
        "sec_edgar_downloader._orchestrator.download_filing",
    ) as mock_download_filing, patch(
        "sec_edgar_downloader._orchestrator.save_document",
    ) as mock_save_document:
        mock_exists.return_value = True
        fetch_and_save_filings(download_metadata, user_agent)

    assert mock_download_filing.call_count == 0
    assert mock_save_document.call_count == 0


def test_fetch_and_save_filings_given_exception(user_agent, form_10k, apple_cik):
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=1,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=False,
    )

    with patch(
        "sec_edgar_downloader._orchestrator.download_filing",
    ) as mock_download_filing, patch(
        "sec_edgar_downloader._orchestrator.save_document",
    ) as mock_save_document:
        mock_download_filing.side_effect = RequestException("Error")
        fetch_and_save_filings(download_metadata, user_agent)

    assert mock_save_document.call_count == 0


def test_get_ticker_to_cik_mapping(user_agent, sample_cik_ticker_payload):
    with patch(
        "sec_edgar_downloader._orchestrator.get_ticker_metadata",
        new=lambda x: sample_cik_ticker_payload,
    ):
        result = get_ticker_to_cik_mapping(user_agent)

    assert result == {
        "AAPL": "0000320193",
        "MSFT": "0000789019",
        "GOOGL": "0001652044",
        "AMZN": "0001018724",
    }


def _mock_sec_api_response_multi_page(submissions_uri, _):
    json_path = Path("test_data") / submissions_uri.split("/")[-1]
    assert json_path.exists()
    with json_path.open() as f:
        return json.load(f)
