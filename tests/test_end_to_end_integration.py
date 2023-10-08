"""End-to-end integration tests."""
from datetime import date
from pathlib import Path

import pytest

from sec_edgar_downloader._constants import (
    FILING_FULL_SUBMISSION_FILENAME,
    PRIMARY_DOC_FILENAME_STEM,
    ROOT_SAVE_FOLDER_NAME,
)


def directory_is_empty(directory):
    return not any(Path(directory).iterdir())


def test_integration_apple_10_k_given_ticker_and_limit(
    network_downloader, form_10k, apple_ticker
):
    dl, dl_path = network_downloader
    assert directory_is_empty(dl_path)

    dl.get(form_10k, apple_ticker, limit=1)

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / apple_ticker / form_10k
    downloaded_acc_nums = downloaded_file_path.glob("*")
    forms = downloaded_file_path.glob("*/*.txt")

    assert len(list(downloaded_acc_nums)) == len(list(forms)) == 1
    assert all(form.stat() > 0 for form in forms)


def test_integration_apple_10_k_given_cik_and_limit(
    network_downloader, form_10k, apple_cik
):
    dl, dl_path = network_downloader
    assert directory_is_empty(dl_path)

    dl.get(form_10k, apple_cik, limit=1)

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / apple_cik / form_10k
    downloaded_acc_nums = downloaded_file_path.glob("*")
    forms = downloaded_file_path.glob("*/*.txt")

    assert len(list(downloaded_acc_nums)) == len(list(forms)) == 1
    assert all(form.stat() > 0 for form in forms)


def test_integration_apple_10_k_given_before_and_after(
    network_downloader, form_10k, apple_cik
):
    dl, dl_path = network_downloader
    assert directory_is_empty(dl_path)

    dl.get(form_10k, apple_cik, before=date(2022, 1, 1), after=date(2018, 1, 1))

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / apple_cik / form_10k
    downloaded_acc_nums = downloaded_file_path.glob("*")
    forms = downloaded_file_path.glob("*/*.txt")

    assert len(list(downloaded_acc_nums)) == len(list(forms)) == 4
    assert all(form.stat() > 0 for form in forms)


def test_integration_apple_10_k_given_include_amends(
    network_downloader, form_10k, apple_cik
):
    dl, dl_path = network_downloader
    assert directory_is_empty(dl_path)

    dl.get(form_10k, apple_cik, before=date(2023, 9, 1), include_amends=True)

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / apple_cik / form_10k
    downloaded_acc_nums = downloaded_file_path.glob("*")
    forms = downloaded_file_path.glob("*/*.txt")

    assert len(list(downloaded_acc_nums)) == len(list(forms)) == 29
    assert all(form.stat() > 0 for form in forms)


# Integration test for issue #129
def test_integration_apple_def_14a_given_include_amends(
    network_downloader, form_def_14a, apple_cik
):
    dl, dl_path = network_downloader
    assert directory_is_empty(dl_path)

    dl.get(form_def_14a, apple_cik, before=date(2023, 10, 7), include_amends=True)

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / apple_cik / form_def_14a
    downloaded_acc_nums = downloaded_file_path.glob("*")
    forms = downloaded_file_path.glob("*/*.txt")

    assert len(list(downloaded_acc_nums)) == len(list(forms)) == 29
    assert all(form.stat() > 0 for form in forms)


@pytest.mark.skipif(
    not (Path(__file__).parent / "test_data").exists(), reason="test data is required"
)
@pytest.mark.parametrize(
    "filing_type,ticker,before_date,downloaded_filename",
    [
        (
            "8-K",
            "AAPL",
            date(2019, 11, 15),
            FILING_FULL_SUBMISSION_FILENAME,
        ),
        (
            "4",
            "AAPL",
            date(2020, 10, 13),
            f"{PRIMARY_DOC_FILENAME_STEM}.xml",
        ),
    ],
)
def test_integration_verify_file_contents(
    network_downloader, filing_type, ticker, before_date, downloaded_filename
):
    """Only run this test when the sample filings folder exists.

    This check is required since the distributed python package will
    not contain the sample filings test data due to size constraints.
    """
    dl, dl_path = network_downloader
    assert directory_is_empty(dl_path)

    downloaded_filename = Path(downloaded_filename)
    extension = downloaded_filename.suffix

    num_downloaded = dl.get(
        filing_type, ticker, limit=1, before=before_date, download_details=True
    )
    assert num_downloaded == 1

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / ticker / filing_type
    assert len(list(downloaded_file_path.glob("*"))) == 1
    accession_number = list(downloaded_file_path.glob("*"))[0]
    downloaded_file_path /= accession_number
    downloaded_filings = list(downloaded_file_path.glob("*"))
    assert len(downloaded_filings) == 2

    sample_filings = Path(__file__).parent / "test_data" / "sample_filings"
    filename_parts = [
        ticker,
        filing_type.replace("-", ""),
        f"{before_date.strftime('%Y%m%d')}{extension}",
    ]

    filename = "-".join(filename_parts).lower()
    expected = sample_filings / filename
    downloaded = downloaded_file_path / downloaded_filename

    with expected.open() as expected_file:
        with downloaded.open() as downloaded_file:
            assert expected_file.readlines() == downloaded_file.readlines()


def test_integration_verify_folder_structure(network_downloader):
    """Download a number of filings from different companies to ensure
    that the file directory looks as follows, with 9 directories, 7 files:

    sec_edgar_filings
    ├── AAPL
    │   ├── 10-K
    │   │   └── 0000320193-20-000096
    │   │       └── full-submission.txt
    │   └── 8-K
    │       ├── 0000320193-20-000094
    │       │   ├── primary-document.html
    │       │   └── full-submission.txt
    │       └── 0001193125-20-225672
    │           ├── primary-document.html
    │           └── full-submission.txt
    └── IBM
        └── 4
            └── 0001562180-20-006712
                ├── primary-document.xml
                └── full-submission.txt
    """
    dl, dl_path = network_downloader
    assert directory_is_empty(dl_path)

    filings_save_path = dl_path / ROOT_SAVE_FOLDER_NAME

    # Verify AAPL 8-K download
    ticker = "AAPL"
    filing_type = "8-K"
    dl.get(filing_type, ticker, limit=2, download_details=True)
    assert len(list((filings_save_path / ticker).glob("*"))) == 1

    filings_downloaded = (filings_save_path / ticker / filing_type).glob("*")
    assert len(list(filings_downloaded)) == 2
    for filing in filings_downloaded:
        assert len(list(filing.glob("*"))) == 2

        downloaded_filing = filing / FILING_FULL_SUBMISSION_FILENAME
        assert downloaded_filing.exists()
        assert downloaded_filing.is_file()

        downloaded_filing = filing / f"{PRIMARY_DOC_FILENAME_STEM}.html"
        assert downloaded_filing.exists()
        assert downloaded_filing.is_file()

    # Verify AAPL 10-K download
    filing_type = "10-K"
    dl.get(filing_type, ticker, limit=1, download_details=False)
    assert len(list((filings_save_path / ticker).glob("*"))) == 2

    filings_downloaded = list((filings_save_path / ticker / filing_type).glob("*"))
    assert len(filings_downloaded) == 1
    filing = filings_downloaded[0]
    assert len(list(filing.glob("*"))) == 1

    downloaded_filing = filing / FILING_FULL_SUBMISSION_FILENAME
    assert downloaded_filing.exists()
    assert downloaded_filing.is_file()

    # Ensure that only one ticker is present after AAPL downloads
    assert len(list(filings_save_path.glob("*"))) == 1

    # Verify IBM Form 4 download
    ticker = "IBM"
    filing_type = "4"
    dl.get(filing_type, ticker, limit=1, download_details=True)
    assert len(list((filings_save_path / ticker).glob("*"))) == 1

    filings_downloaded = list((filings_save_path / ticker / filing_type).glob("*"))
    assert len(filings_downloaded) == 1
    filing = filings_downloaded[0]
    assert len(list(filing.glob("*"))) == 2

    downloaded_filing = filing / FILING_FULL_SUBMISSION_FILENAME
    assert downloaded_filing.exists()
    assert downloaded_filing.is_file()

    downloaded_filing = filing / f"{PRIMARY_DOC_FILENAME_STEM}.xml"
    assert downloaded_filing.exists()
    assert downloaded_filing.is_file()

    # Ensure that two tickers are present after AAPL and IBM downloads
    assert len(list(filings_save_path.glob("*"))) == 2
