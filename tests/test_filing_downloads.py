"""Tests all types of filing downloads to ensure that the filings
are properly downloaded and saved in the correct folder hierarchy.
"""

import filecmp
import os

from ._testing_utils import strip_cik, verify_directory_structure


def test_8k_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_folder_base = downloader

    num_downloaded = dl.get_8k_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file 8-K
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_8k_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(
        download_folder_base, ["8-K"], 1, **apple_filing_metadata
    )


def test_10k_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_folder_base = downloader

    num_downloaded = dl.get_10k_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file 10-K
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_10k_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(
        download_folder_base, ["10-K"], 1, **apple_filing_metadata
    )


def test_10q_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_folder_base = downloader

    num_downloaded = dl.get_10q_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file 10-Q
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_10q_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(
        download_folder_base, ["10-Q"], 1, **apple_filing_metadata
    )


def test_13f_nt_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_folder_base = downloader

    # Tests trimming of trailing 0s and creation of a single
    # folder for the Vanguard Group
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_13f_nt_filings(vanguard_full_cik, 1)
    assert num_downloaded == 1
    num_downloaded = dl.get_13f_nt_filings(strip_cik(vanguard_full_cik), 1)
    assert num_downloaded == 1

    num_downloaded = dl.get_13f_nt_filings(apple_filing_metadata["symbol"])
    assert num_downloaded == 0

    verify_directory_structure(
        download_folder_base, ["13F-NT"], 1, **vanguard_filing_metadata
    )


def test_13f_hr_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_folder_base = downloader

    # Tests trimming of trailing 0s and creation of a single
    # folder for the Vanguard Group
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_13f_hr_filings(vanguard_full_cik, 1)
    assert num_downloaded == 1
    num_downloaded = dl.get_13f_hr_filings(strip_cik(vanguard_full_cik), 1)
    assert num_downloaded == 1

    num_downloaded = dl.get_13f_hr_filings(apple_filing_metadata["symbol"])
    assert num_downloaded == 0

    verify_directory_structure(
        download_folder_base, ["13F-HR"], 1, **vanguard_filing_metadata
    )


def test_sc_13g_filing_retrieval(downloader, apple_filing_metadata):
    dl, download_folder_base = downloader

    num_downloaded = dl.get_sc_13g_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    verify_directory_structure(
        download_folder_base, ["SC 13G"], 1, **apple_filing_metadata
    )


def test_sd_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_folder_base = downloader

    num_downloaded = dl.get_sd_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file SD
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_sd_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(download_folder_base, ["SD"], 1, **apple_filing_metadata)


def test_all_available_filing_retrieval_common_stock(downloader, apple_filing_metadata):
    dl, download_folder_base = downloader

    num_downloaded = dl.get_all_available_filings(apple_filing_metadata["symbol"], 2)
    assert num_downloaded == 10

    expected_filings = ["SD", "10-Q", "10-K", "8-K", "SC 13G"]
    verify_directory_structure(
        download_folder_base, expected_filings, 2, **apple_filing_metadata
    )


def test_all_available_filing_retrieval_institutional_investor(
    downloader, vanguard_filing_metadata
):
    dl, download_folder_base = downloader

    num_downloaded = dl.get_all_available_filings(
        vanguard_filing_metadata["full_cik"], 2
    )
    assert num_downloaded == 6

    expected_filings = ["13F-HR", "13F-NT", "SC 13G"]
    verify_directory_structure(
        download_folder_base, expected_filings, 2, **vanguard_filing_metadata
    )


def test_large_filing_download(downloader):
    """Tests to ensure that filings downloaded with this package
    are identical to those that are downloaded via the web browser.

    The expected data file (visa_8k_20190424.txt) was manually
    downloaded in a web browser from:
    https://www.sec.gov/Archives/edgar/data/1403161/000140316119000014/0001403161-19-000014.txt
    """

    dl, download_folder_base = downloader

    dl.get_8k_filings("V", 1, before_date="20190424")

    filing_8k_download_folder = download_folder_base.joinpath(
        "sec_edgar_filings", "V", "8-K"
    )

    filing_8k_download_folder_contents = os.listdir(filing_8k_download_folder)
    assert len(filing_8k_download_folder_contents) == 1

    downloaded_filename = filing_8k_download_folder_contents[0]
    downloaded_file_path = filing_8k_download_folder.joinpath(downloaded_filename)

    assert downloaded_file_path.exists()
    assert downloaded_file_path.is_file()

    # https://stackoverflow.com/q/1072569
    expected_data_path = "tests/_testing_data/visa_8k_20190424.txt"
    assert filecmp.cmp(expected_data_path, downloaded_file_path, False)
