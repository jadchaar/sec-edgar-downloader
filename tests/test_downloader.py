from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS


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
        )

    assert mocked_fetch.call_count == 1
    assert mocked_fetch.call_args_list[0].args[0].after == datetime(1994, 1, 1).date()


def test_non_string_date(downloader, form_10k, apple_cik):
    dl, _ = downloader

    dt = datetime(2023, 1, 1)

    with pytest.raises(TypeError):
        dl.get(form_10k, apple_cik, after=dt)
