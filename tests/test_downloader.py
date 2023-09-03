import os
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS, SUPPORTED_FORMS
from sec_edgar_downloader.Downloader import Downloader


def test_downloader_folder_default_path():
    downloader = Downloader("foo", "bar@baz.com")

    assert downloader.download_folder == Path.cwd()


def test_downloader_folder_given_pathlib_path():
    downloader = Downloader("foo", "bar@baz.com", Path("folder-foo"))

    assert downloader.download_folder == Path("folder-foo")


def test_downloader_folder_given_blank_path():
    dl = Downloader("foo", "bar@baz.com", "")
    # pathlib treats blank paths as the current working directory
    expected = Path.cwd()
    assert dl.download_folder == expected


@pytest.mark.skipif(
    os.name == "nt", reason="test should only run on Unix-based systems"
)
def test_downloader_folder_given_relative_path():
    dl = Downloader("foo", "bar@baz.com", "./Downloads")
    expected = Path.cwd() / "Downloads"
    assert dl.download_folder == expected


def test_downloader_folder_given_user_path():
    dl = Downloader("foo", "bar@baz.com", "~/Downloads")
    expected = Path.home() / "Downloads"
    assert dl.download_folder == expected


def test_downloader_folder_given_custom_path():
    custom_path = Path.home() / "Downloads/SEC/EDGAR/Downloader"
    dl = Downloader("foo", "bar@baz.com", custom_path)
    assert dl.download_folder == custom_path


def test_supported_filings(downloader):
    dl, _ = downloader
    expected = sorted(SUPPORTED_FORMS)
    assert dl.supported_forms == expected


def test_invalid_filing_type(downloader, apple_ticker):
    dl, _ = downloader
    invalid_filing_type = "10-INVALID"

    with pytest.raises(ValueError) as exc_info:
        dl.get(invalid_filing_type, apple_ticker)

    assert "'10-INVALID' forms are not supported" in str(exc_info.value)


def test_invalid_ticker(downloader, form_10k):
    dl, dl_path = downloader
    invalid_ticker = "INVALIDTICKER"

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, invalid_ticker)

    assert "Ticker is invalid" in str(exc_info.value)


def test_invalid_cik(downloader, form_10k):
    dl, _ = downloader
    cik = "12345678910"

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, cik)

    assert "Invalid CIK" in str(exc_info.value)


def test_blank_ticker(downloader, form_10k):
    dl, _ = downloader
    expected_msg = "Invalid ticker or CIK. Please enter a non-blank value."
    ticker = ""

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, ticker)

    assert expected_msg in str(exc_info.value)


def test_cik_zero_padding(downloader, form_10k, apple_cik):
    dl, _ = downloader

    with patch(
        "sec_edgar_downloader.Downloader.fetch_and_save_filings"
    ) as mocked_fetch:
        dl.get(form_10k, apple_cik)
        dl.get(form_10k, apple_cik.strip("0"))

    assert mocked_fetch.call_count == 2
    assert (
        mocked_fetch.call_args_list[0].args[0].cik
        == mocked_fetch.call_args_list[1].args[0].cik
        == apple_cik
    )


def test_invalid_num_filings_to_download(downloader, form_10k, apple_cik):
    dl, _ = downloader

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, limit=-1)

    assert "Please enter a number greater than 1." in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, limit=0)

    assert "Please enter a number greater than 1." in str(exc_info.value)


def test_invalid_before_and_after_dates(downloader, form_10k, apple_cik):
    dl, _ = downloader

    dt = datetime(2019, 11, 15).strftime("%Y%m%d")

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, after=dt)

    assert "Please enter a date string of the form YYYY-MM-DD." in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, before=dt)

    assert "Please enter a date string of the form YYYY-MM-DD." in str(exc_info.value)


def test_equal_before_and_after_dates(downloader, form_10k, apple_cik):
    dl, _ = downloader

    dt = datetime(2019, 11, 15).strftime(DATE_FORMAT_TOKENS)

    with patch(
        "sec_edgar_downloader.Downloader.fetch_and_save_filings"
    ) as mocked_fetch:
        dl.get(form_10k, apple_cik, after=dt, before=dt)

    assert mocked_fetch.call_count == 1


def test_invalid_before_and_after_date_combos(downloader, form_10k, apple_cik):
    dl, _ = downloader

    dt = datetime(2019, 11, 15)

    with pytest.raises(ValueError) as exc_info:
        dl.get(
            form_10k,
            apple_cik,
            after=(dt + timedelta(days=3)).strftime(DATE_FORMAT_TOKENS),
            before=dt.strftime(DATE_FORMAT_TOKENS),
        )

    assert "After date cannot be greater than the before date" in str(exc_info.value)


def test_pre_default_after_date(downloader, form_10k, apple_cik):
    dl, _ = downloader

    dt = datetime(1900, 11, 15)

    with patch(
        "sec_edgar_downloader.Downloader.fetch_and_save_filings"
    ) as mocked_fetch:
        dl.get(
            form_10k,
            apple_cik,
            after=(dt - timedelta(days=1)).strftime(DATE_FORMAT_TOKENS),
            limit=1,
        )

    assert mocked_fetch.call_count == 1
    assert mocked_fetch.call_args_list[0].args[0].after == datetime(1994, 1, 1).date()
