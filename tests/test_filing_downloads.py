import os
import pytest
from sec_edgar_downloader import Downloader
from utils import verify_directory_structure, strip_cik


def test_8k_filing_retrieval(default_download_folder, apple_filing_metadata, vanguard_filing_metadata):
    dl = Downloader(default_download_folder)

    num_downloaded = dl.get_8k_filings(apple_filing_metadata["ticker_symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group (CIK: 0000102909) does not file 8-K
    vanguard_full_cik = vanguard_filing_metadata["ticker_full_cik"]
    num_downloaded = dl.get_8k_filings(vanguard_full_cik)
    assert num_downloaded == 0
    num_downloaded = dl.get_8k_filings(strip_cik(vanguard_full_cik))
    assert num_downloaded == 0

    verify_directory_structure(default_download_folder, "8-K", **apple_filing_metadata)


def test_13f_hr_filing_retrieval(default_download_folder, apple_filing_metadata, vanguard_filing_metadata):
    dl = Downloader(default_download_folder)

    # Tests trimming of trailing 0s and creation of a single
    # folder for the Vanguard Group
    vanguard_full_cik = vanguard_filing_metadata["ticker_full_cik"]
    num_downloaded = dl.get_13f_hr_filings(vanguard_full_cik, 1)
    assert num_downloaded == 1
    num_downloaded = dl.get_13f_hr_filings(strip_cik(vanguard_full_cik), 1)
    assert num_downloaded == 1

    num_downloaded = dl.get_13f_hr_filings(apple_filing_metadata["ticker_symbol"])
    assert num_downloaded == 0

    verify_directory_structure(default_download_folder, "13F-HR", **vanguard_filing_metadata)


def test_13f_nt_filing_retrieval(default_download_folder, apple_filing_metadata, vanguard_filing_metadata):
    dl = Downloader(default_download_folder)

    # Tests trimming of trailing 0s and creation of a single
    # folder for the Vanguard Group
    vanguard_full_cik = vanguard_filing_metadata["ticker_full_cik"]
    num_downloaded = dl.get_13f_nt_filings(vanguard_full_cik, 1)
    assert num_downloaded == 1
    num_downloaded = dl.get_13f_nt_filings(strip_cik(vanguard_full_cik), 1)
    assert num_downloaded == 1

    num_downloaded = dl.get_13f_nt_filings(apple_filing_metadata["ticker_symbol"])
    assert num_downloaded == 0

    verify_directory_structure(default_download_folder, "13F-NT", **vanguard_filing_metadata)


# ! TODO: test passing in non-int num_filings
# ! TODO: test passing in negative num_filings
# TODO: test passing in CIK and ticker with trailing whitespace and symbols
# TODO: test passing in CIK as number

# TODO: test throwing IO error in ctor

'''
Testing TODO:
10-K
10-Q
13-F
SC-13G
SD
get_all_available_filings
'''
