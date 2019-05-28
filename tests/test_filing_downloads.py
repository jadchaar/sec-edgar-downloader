from .utils import strip_cik, verify_directory_structure


def test_8k_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_location = downloader

    num_downloaded = dl.get_8k_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file 8-K
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_8k_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(download_location, ["8-K"], 1, **apple_filing_metadata)


def test_10k_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_location = downloader

    num_downloaded = dl.get_10k_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file 10-K
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_10k_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(download_location, ["10-K"], 1, **apple_filing_metadata)


def test_10q_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_location = downloader

    num_downloaded = dl.get_10q_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file 10-Q
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_10q_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(download_location, ["10-Q"], 1, **apple_filing_metadata)


def test_13f_nt_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_location = downloader

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
        download_location, ["13F-NT"], 1, **vanguard_filing_metadata
    )


def test_13f_hr_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_location = downloader

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
        download_location, ["13F-HR"], 1, **vanguard_filing_metadata
    )


def test_sc_13g_filing_retrieval(downloader, apple_filing_metadata):
    dl, download_location = downloader

    num_downloaded = dl.get_sc_13g_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    verify_directory_structure(
        download_location, ["SC 13G"], 1, **apple_filing_metadata
    )


def test_sd_filing_retrieval(
    downloader, apple_filing_metadata, vanguard_filing_metadata
):
    dl, download_location = downloader

    num_downloaded = dl.get_sd_filings(apple_filing_metadata["symbol"], 1)
    assert num_downloaded == 1

    # Vanguard Group does not file SD
    vanguard_full_cik = vanguard_filing_metadata["full_cik"]
    num_downloaded = dl.get_sd_filings(vanguard_full_cik)
    assert num_downloaded == 0

    verify_directory_structure(download_location, ["SD"], 1, **apple_filing_metadata)


def test_all_available_filing_retrieval_common_stock(downloader, apple_filing_metadata):
    dl, download_location = downloader

    num_downloaded = dl.get_all_available_filings(apple_filing_metadata["symbol"], 2)
    assert num_downloaded == 10

    expected_filings = ["SD", "10-Q", "10-K", "8-K", "SC 13G"]
    verify_directory_structure(
        download_location, expected_filings, 2, **apple_filing_metadata
    )


def test_all_available_filing_retrieval_institutional_investor(
    downloader, vanguard_filing_metadata
):
    dl, download_location = downloader

    num_downloaded = dl.get_all_available_filings(
        vanguard_filing_metadata["full_cik"], 2
    )
    assert num_downloaded == 6

    expected_filings = ["13F-HR", "13F-NT", "SC 13G"]
    verify_directory_structure(
        download_location, expected_filings, 2, **vanguard_filing_metadata
    )
