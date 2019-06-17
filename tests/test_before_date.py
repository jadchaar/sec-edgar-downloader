from ._testing_utils import verify_directory_structure


def test_before_date_filing_retrieval(downloader, apple_filing_metadata_pre_2007):
    # 12/13/1994 is the date of Apple's first filing
    dl, download_folder_base = downloader

    num_downloaded = dl.get_10k_filings(
        apple_filing_metadata_pre_2007["symbol"], 100, "19941213"
    )
    assert num_downloaded == 1

    num_downloaded = dl.get_10k_filings(
        apple_filing_metadata_pre_2007["symbol"], 100, "19941212"
    )
    assert num_downloaded == 0

    verify_directory_structure(
        download_folder_base,
        ["10-K"],
        1,
        **apple_filing_metadata_pre_2007,
        before_date="19941213",
    )
