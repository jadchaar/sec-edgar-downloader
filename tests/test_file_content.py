"""Tests the contents of downloaded files."""

from datetime import date
from pathlib import Path

import pytest

from sec_edgar_downloader._constants import (
    DATE_FORMAT_TOKENS,
    FILING_DETAILS_FILENAME_STEM,
    FILING_FULL_SUBMISSION_FILENAME,
    ROOT_SAVE_FOLDER_NAME,
)


@pytest.mark.skipif(
    not Path("tests/sample-filings").exists(), reason="sample filings are required"
)
@pytest.mark.parametrize(
    "filing_type,ticker,before_date,downloaded_filename",
    [
        (
            "8-K",
            "AAPL",
            date(2019, 11, 15).strftime(DATE_FORMAT_TOKENS),
            FILING_FULL_SUBMISSION_FILENAME,
        ),
        (
            "4",
            "AAPL",
            date(2020, 10, 13).strftime(DATE_FORMAT_TOKENS),
            f"{FILING_DETAILS_FILENAME_STEM}.xml",
        ),
    ],
)
def test_file_contents(
    downloader, filing_type, ticker, before_date, downloaded_filename
):
    """Only run this test when the sample filings folder exists.

    This check is required since the distributed python package will
    not contain the sample filings test data due to size constraints.
    """
    dl, dl_path = downloader
    downloaded_filename = Path(downloaded_filename)
    extension = downloaded_filename.suffix

    num_downloaded = dl.get(
        filing_type, ticker, amount=1, before=before_date, download_details=True
    )
    assert num_downloaded == 1

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / ticker / filing_type
    assert len(list(downloaded_file_path.glob("*"))) == 1
    accession_number = list(downloaded_file_path.glob("*"))[0]
    downloaded_file_path /= accession_number
    downloaded_filings = list(downloaded_file_path.glob("*"))
    assert len(downloaded_filings) == 2

    sample_filings = Path("tests/sample-filings")
    filename_parts = [
        ticker,
        filing_type.replace("-", ""),
        f"{before_date.replace('-', '')}{extension}",
    ]

    filename = "-".join(filename_parts).lower()
    expected = sample_filings / filename
    downloaded = downloaded_file_path / downloaded_filename

    with expected.open() as expected_file:
        with downloaded.open() as downloaded_file:
            assert expected_file.readlines() == downloaded_file.readlines()
