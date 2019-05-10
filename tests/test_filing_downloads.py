import os
import pytest
from sec_edgar_downloader import Downloader
from utils import verify_directory_structure


def test_8k_filing_retrieval(default_download_folder, apple_filing_metadata):
    dl = Downloader(default_download_folder)

    num_downloaded = dl.get_8k_filings("AAPL", 1)
    assert num_downloaded == 1

    # Vanguard Group (CIK: 0000102909) does not file 8-Ks
    num_downloaded = dl.get_8k_filings("0000102909")
    assert num_downloaded == 0
    num_downloaded = dl.get_8k_filings("102909")
    assert num_downloaded == 0

    verify_directory_structure(default_download_folder, "8-K", **apple_filing_metadata)

# TODO: test throwing IO error in ctor

# ! TODO: test passing in non-int num_filings
# ! TODO: test passing in negative num_filings
# TODO: test passing in CIK and ticker with trailing whitespace and symbols
# TODO: test passing in CIK as number


'''
Testing TODO:
10-K
10-Q
13-F
SC-13G
SD
get_all_available_filings
get_all_available_filings_for_symbol_list
'''
