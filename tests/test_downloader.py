import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from sec_edgar_downloader._constants import DATE_FORMAT_TOKENS, SUPPORTED_FORMS
from sec_edgar_downloader._Downloader import Downloader


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_downloader_folder_default_path(_):
    dl = Downloader("foo", "bar@baz.com")

    assert dl.download_folder == Path.cwd()


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_downloader_folder_given_pathlib_path(_):
    dl = Downloader("foo", "bar@baz.com", Path("folder-foo"))

    assert dl.download_folder == Path("folder-foo")


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_downloader_folder_given_blank_path(_):
    dl = Downloader("foo", "bar@baz.com", "")
    # pathlib treats blank paths as the current working directory
    expected = Path.cwd()
    assert dl.download_folder == expected


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
@pytest.mark.skipif(
    os.name == "nt", reason="test should only run on Unix-based systems"
)
def test_downloader_folder_given_relative_path(_):
    dl = Downloader("foo", "bar@baz.com", "./Downloads")
    expected = Path.cwd() / "Downloads"
    assert dl.download_folder == expected


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_downloader_folder_given_user_path(_):
    dl = Downloader("foo", "bar@baz.com", "~/Downloads")
    expected = Path.home() / "Downloads"
    assert dl.download_folder == expected


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_downloader_folder_given_custom_path(_):
    custom_path = Path.home() / "Downloads/SEC/EDGAR/Downloader"
    dl = Downloader("foo", "bar@baz.com", custom_path)
    assert dl.download_folder == custom_path


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_supported_filings(_):
    dl = Downloader("foo", "bar@baz.com")
    expected = sorted(SUPPORTED_FORMS)
    assert dl.supported_forms == expected


@pytest.mark.skipif(
    not (Path(__file__).parent / "test_data").exists(), reason="test data is required"
)
def test_download_historical_10_k405(tmp_path):
    def get_recorded_filings(uri, _):
        json_path = (
            Path(__file__).parent
            / "test_data"
            / "sample_api_responses"
            / uri.rsplit("/", 1)[-1]
        )
        with json_path.open() as f:
            return json.load(f)

    with patch(
        "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping", return_value={}
    ), patch(
        "sec_edgar_downloader._orchestrator.get_list_of_available_filings",
        side_effect=get_recorded_filings,
    ), patch(
        "sec_edgar_downloader._orchestrator.download_filing",
        return_value=b"historical filing",
    ):
        dl = Downloader("foo", "bar@baz.com", tmp_path)
        assert dl.get("10-K405", "0000320193") == 2

    filings_path = tmp_path / "sec-edgar-filings" / "0000320193" / "10-K405"
    assert sorted(p.name for p in filings_path.iterdir()) == [
        "0000912057-01-544436",
        "0001047469-98-044981",
    ]
    for filing in filings_path.iterdir():
        assert (filing / "full-submission.txt").read_bytes() == b"historical filing"


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_invalid_filing_type(_, apple_ticker):
    dl = Downloader("foo", "bar@baz.com")
    invalid_filing_type = "10-INVALID"

    with pytest.raises(ValueError) as exc_info:
        dl.get(invalid_filing_type, apple_ticker)

    assert "'10-INVALID' forms are not supported" in str(exc_info.value)


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_invalid_ticker(_, form_10k):
    dl = Downloader("foo", "bar@baz.com")
    invalid_ticker = "INVALIDTICKER"

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, invalid_ticker)

    assert "Ticker 'INVALIDTICKER' is invalid" in str(exc_info.value)


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_invalid_cik(_, form_10k):
    dl = Downloader("foo", "bar@baz.com")
    cik = "12345678910"

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, cik)

    assert "Invalid CIK" in str(exc_info.value)


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_blank_ticker(_, form_10k):
    dl = Downloader("foo", "bar@baz.com")
    expected_msg = "Invalid ticker or CIK. Please enter a non-blank value."
    ticker = ""

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, ticker)

    assert expected_msg in str(exc_info.value)


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_cik_zero_padding(_, form_10k, apple_cik):
    dl = Downloader("foo", "bar@baz.com")

    with patch(
        "sec_edgar_downloader._Downloader.fetch_and_save_filings",
    ) as mocked_fetch:
        dl.get(form_10k, apple_cik)
        dl.get(form_10k, apple_cik.strip("0"))

    assert mocked_fetch.call_count == 2
    assert (
        mocked_fetch.call_args_list[0].args[0].cik
        == mocked_fetch.call_args_list[1].args[0].cik
        == apple_cik
    )


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_invalid_num_filings_to_download(_, form_10k, apple_cik):
    dl = Downloader("foo", "bar@baz.com")

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, limit=-1)

    assert "Please enter a number greater than 1." in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, limit=0)

    assert "Please enter a number greater than 1." in str(exc_info.value)


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_invalid_before_and_after_dates(_, form_10k, apple_cik):
    dl = Downloader("foo", "bar@baz.com")

    dt = datetime(2019, 11, 15).strftime("%Y%m%d")

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, after=dt)

    assert "Please enter a date string of the form YYYY-MM-DD." in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        dl.get(form_10k, apple_cik, before=dt)

    assert "Please enter a date string of the form YYYY-MM-DD." in str(exc_info.value)


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_equal_before_and_after_dates(_, form_10k, apple_cik):
    dl = Downloader("foo", "bar@baz.com")

    dt = datetime(2019, 11, 15).strftime(DATE_FORMAT_TOKENS)

    with patch(
        "sec_edgar_downloader._Downloader.fetch_and_save_filings",
    ) as mocked_fetch:
        dl.get(form_10k, apple_cik, after=dt, before=dt)

    assert mocked_fetch.call_count == 1


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_invalid_before_and_after_date_combos(_, form_10k, apple_cik):
    dl = Downloader("foo", "bar@baz.com")

    dt = datetime(2019, 11, 15)

    with pytest.raises(ValueError) as exc_info:
        dl.get(
            form_10k,
            apple_cik,
            after=(dt + timedelta(days=3)).strftime(DATE_FORMAT_TOKENS),
            before=dt.strftime(DATE_FORMAT_TOKENS),
        )

    assert "After date cannot be greater than the before date" in str(exc_info.value)


@patch(
    "sec_edgar_downloader._Downloader.get_ticker_to_cik_mapping",
    return_value={"AAPL": "0000320193"},
)
def test_pre_default_after_date(_, form_10k, apple_cik):
    dl = Downloader("foo", "bar@baz.com")

    dt = datetime(1900, 11, 15)

    with patch(
        "sec_edgar_downloader._Downloader.fetch_and_save_filings",
    ) as mocked_fetch:
        dl.get(
            form_10k,
            apple_cik,
            after=(dt - timedelta(days=1)).strftime(DATE_FORMAT_TOKENS),
            limit=1,
        )

    assert mocked_fetch.call_count == 1
    assert mocked_fetch.call_args_list[0].args[0].after == datetime(1994, 1, 1).date()
