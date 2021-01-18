"""Tests the downloaded file structure."""

from sec_edgar_downloader._constants import (
    FILING_DETAILS_FILENAME_STEM,
    FILING_FULL_SUBMISSION_FILENAME,
    ROOT_SAVE_FOLDER_NAME,
)


def test_file_structure(downloader):
    """Download a number of filings from different companies to ensure
    that the file directory looks as follows, with 9 directories, 7 files:

    sec_edgar_filings
    ├── AAPL
    │   ├── 10-K
    │   │   └── 0000320193-20-000096
    │   │       └── full-submission.txt
    │   └── 8-K
    │       ├── 0000320193-20-000094
    │       │   ├── filing-details.html
    │       │   └── full-submission.txt
    │       └── 0001193125-20-225672
    │           ├── filing-details.html
    │           └── full-submission.txt
    └── IBM
        └── 4
            └── 0001562180-20-006712
                ├── filing-details.xml
                └── full-submission.txt
    """
    dl, dl_path = downloader
    filings_save_path = dl_path / ROOT_SAVE_FOLDER_NAME

    assert len(list(dl_path.glob("**/*"))) == 0

    # Verify AAPL 8-K download
    ticker = "AAPL"
    filing_type = "8-K"
    dl.get(filing_type, ticker, amount=2, download_details=True)
    assert len(list((filings_save_path / ticker).glob("*"))) == 1

    filings_downloaded = (filings_save_path / ticker / filing_type).glob("*")
    assert len(list(filings_downloaded)) == 2
    for filing in filings_downloaded:
        assert len(list(filing.glob("*"))) == 2

        downloaded_filing = filing / FILING_FULL_SUBMISSION_FILENAME
        assert downloaded_filing.exists()
        assert downloaded_filing.is_file()

        downloaded_filing = filing / f"{FILING_DETAILS_FILENAME_STEM}.html"
        assert downloaded_filing.exists()
        assert downloaded_filing.is_file()

    # Verify AAPL 10-K download
    filing_type = "10-K"
    dl.get(filing_type, ticker, amount=1, download_details=False)
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
    dl.get(filing_type, ticker, amount=1, download_details=True)
    assert len(list((filings_save_path / ticker).glob("*"))) == 1

    filings_downloaded = list((filings_save_path / ticker / filing_type).glob("*"))
    assert len(filings_downloaded) == 1
    filing = filings_downloaded[0]
    assert len(list(filing.glob("*"))) == 2

    downloaded_filing = filing / FILING_FULL_SUBMISSION_FILENAME
    assert downloaded_filing.exists()
    assert downloaded_filing.is_file()

    downloaded_filing = filing / f"{FILING_DETAILS_FILENAME_STEM}.xml"
    assert downloaded_filing.exists()
    assert downloaded_filing.is_file()

    # Ensure that two tickers are present after AAPL and IBM downloads
    assert len(list(filings_save_path.glob("*"))) == 2
