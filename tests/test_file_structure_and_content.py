"""Tests the file structure and contents of downloaded files."""

import filecmp
from datetime import date
from pathlib import Path

import pytest

from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS, ROOT_SAVE_FOLDER_NAME

# def test_file_structure(downloader):
#     """Download a number of filings from different companies to ensure
#     that the file directory looks as follows, with 9 directories, 7 files:

#     sec_edgar_filings
#     ├── AAPL
#     │   ├── 10-K
#     │   │   └── 0000320193-20-000096
#     │   │       └── full_submission.txt
#     │   └── 8-K
#     │       ├── 0000320193-20-000094
#     │       │   ├── filing_details.html
#     │       │   └── full_submission.txt
#     │       └── 0001193125-20-225672
#     │           ├── filing_details.html
#     │           └── full_submission.txt
#     └── IBM
#         └── 4
#             └── 0001562180-20-006712
#                 ├── filing_details.xml
#                 └── full_submission.txt
#     """
#     dl, dl_path = downloader

#     assert len(list(dl_path.glob("**/*"))) == 0

#     filing_type = "8-K"
#     ticker = "AAPL"

#     # TODO: use glob patterns and check length
#     dl.get(filing_type, ticker, 2, download_details=True)

#     filing_type = "10-K"
#     dl.get(filing_type, ticker, 1, download_details=False)

#     filing_type = "8-K"
#     ticker = "IBM"
#     dl.get(filing_type, ticker, 1, download_details=True)

#     breakpoint()

# # Get the two latest 8-Ks for AAPL
# num_downloaded = dl.get(filing_type, ticker, 2, download_details=False)
# assert num_downloaded == 2

# filings_save_path = dl_path / ROOT_SAVE_FOLDER_NAME
# assert filings_save_path.exists()
# assert filings_save_path.is_dir()
# assert len(list(filings_save_path.glob("*"))) == 1

# ticker_save_path = filings_save_path / ticker
# assert ticker_save_path.exists()
# assert ticker_save_path.is_dir()
# assert len(list(ticker_save_path.glob("*"))) == 1

# filing_type_save_path = ticker_save_path / filing_type
# assert filing_type_save_path.exists()
# assert filing_type_save_path.is_dir()

# downloaded_accession_numbers = list(filing_type_save_path.glob("*"))
# assert len(downloaded_accession_numbers) == 2

# for accession_number in downloaded_accession_numbers:
#     full_submission_files = list(accession_number.glob("*.txt"))
#     assert len(full_submission_files) == 1
#     full_submission_files = list(accession_number.glob("*.txt"))
#     assert len(full_submission_files) == 1
#     assert len(filing_details) == 2
#     for detail_file in filing_details:
#         assert detail_file.is_file()

# # downloaded_filings = list(filing_type_save_path.glob("*"))
# # assert len(downloaded_filings) == 2
# # assert downloaded_filings[0].is_file()

# # get the latest 10-K for AAPL, including the detail HTML file
# filing_type = "10-K"
# num_downloaded = dl.get(filing_type, ticker, 1, download_details=True)
# assert num_downloaded == 1

# # ensure that the 10-K was added to the existing AAPL dir
# assert len(list(ticker_save_path.glob("*"))) == 2

# filing_type_save_path = ticker_save_path / filing_type
# assert filing_type_save_path.exists()
# assert filing_type_save_path.is_dir()

# downloaded_filings = list(filing_type_save_path.glob("*"))
# assert len(downloaded_filings) == 2
# assert downloaded_filings[0].is_file()
# assert downloaded_filings[1].is_file()
# assert len(list(filing_type_save_path.glob(FILING_FULL_SUBMISSION_FILENAME))) == 1
# assert (
#     len(list(filing_type_save_path.glob(f"{FILING_DETAILS_FILENAME_STEM}.html")))
#     == 1
# )


@pytest.mark.parametrize(
    "filing_type,ticker,before_date,downloaded_filename",
    [
        (
            "8-K",
            "AAPL",
            date(2019, 11, 15).strftime(DATE_FORMAT_TOKENS),
            "full_submission.txt",
        ),
        (
            "4",
            "AAPL",
            date(2020, 10, 13).strftime(DATE_FORMAT_TOKENS),
            "filing_details.xml",
        ),
    ],
)
def test_file_contents(
    downloader, filing_type, ticker, before_date, downloaded_filename
):
    dl, dl_path = downloader
    downloaded_filename = Path(downloaded_filename)
    extension = downloaded_filename.suffix

    num_downloaded = dl.get(
        filing_type, ticker, 1, before=before_date, download_details=True
    )
    assert num_downloaded == 1

    downloaded_file_path = dl_path / ROOT_SAVE_FOLDER_NAME / ticker / filing_type
    assert len(list(downloaded_file_path.glob("*"))) == 1
    accession_number = list(downloaded_file_path.glob("*"))[0]
    downloaded_file_path /= accession_number
    downloaded_filings = list(downloaded_file_path.glob("*"))
    assert len(downloaded_filings) == 2

    sample_filings = Path("tests/sample_filings")
    if sample_filings.exists():
        # Only run this check if the sample filing exists
        # This check is required since the distributed python package will not
        # contain the sample filings test data due to size constraints
        filename = f"{ticker}_{filing_type}_{before_date}{extension}".lower().replace(
            "-", ""
        )
        expected_filing = sample_filings / filename
        downloaded_filing = downloaded_file_path / downloaded_filename
        assert filecmp.cmp(expected_filing, downloaded_filing, shallow=False)
