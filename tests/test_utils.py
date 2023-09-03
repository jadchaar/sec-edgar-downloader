from datetime import date, datetime
from pathlib import Path

import pytest

from sec_edgar_downloader._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE
from sec_edgar_downloader._types import DownloadMetadata
from sec_edgar_downloader._utils import (
    is_cik,
    validate_and_convert_ticker_or_cik,
    validate_and_parse_date,
    within_requested_date_range,
)


def test_is_cik():
    # CIKs are 10 digit identifiers that are zero-padded
    # if they are shorter than 10 digits long
    assert is_cik("0000789019")
    assert is_cik("789019")
    assert is_cik(789019)

    assert not is_cik("AAPL")
    assert not is_cik("")


def test_validate_and_convert_ticker_or_cik_given_blank_ticker(
    sample_ticker_to_cik_mapping,
):
    with pytest.raises(ValueError):
        validate_and_convert_ticker_or_cik("", sample_ticker_to_cik_mapping)


def test_validate_and_convert_ticker_or_cik_given_fake_ticker(
    sample_ticker_to_cik_mapping,
):
    with pytest.raises(ValueError):
        validate_and_convert_ticker_or_cik("FAKE", sample_ticker_to_cik_mapping)


def test_validate_and_convert_ticker_or_cik_given_invalid_cik(
    sample_ticker_to_cik_mapping,
):
    with pytest.raises(ValueError):
        validate_and_convert_ticker_or_cik(
            "000032019311111", sample_ticker_to_cik_mapping
        )


def test_validate_and_convert_ticker_or_cik_given_valid_ticker(
    sample_ticker_to_cik_mapping,
):
    cik = validate_and_convert_ticker_or_cik("AAPL", sample_ticker_to_cik_mapping)

    assert cik == "0000320193"


def test_validate_and_convert_ticker_or_cik_given_valid_cik(
    sample_ticker_to_cik_mapping,
):
    cik = validate_and_convert_ticker_or_cik("320193", sample_ticker_to_cik_mapping)

    assert cik == "0000320193"


def test_validate_and_parse_date_given_valid_inputs():
    result_from_date = validate_and_parse_date(date(2023, 1, 1))
    result_from_datetime = validate_and_parse_date(datetime(2023, 1, 1, 1, 1, 1))
    result_from_str = validate_and_parse_date("2023-1-1")

    assert (
        result_from_date == result_from_datetime == result_from_str == date(2023, 1, 1)
    )


def test_validate_and_parse_date_given_invalid_string_date():
    with pytest.raises(ValueError):
        validate_and_parse_date("2023-08-08T18:30:28.000Z")


def test_validate_and_parse_date_given_invalid_type():
    with pytest.raises(TypeError):
        validate_and_parse_date(2023_1_1)


def test_within_requested_date_range_given_target_date_in_range(form_10k, apple_cik):
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=1,
        after=DEFAULT_AFTER_DATE,
        before=DEFAULT_BEFORE_DATE,
        include_amends=True,
        download_details=True,
    )

    assert within_requested_date_range(download_metadata, "2022-1-1")


def test_within_requested_date_range_given_target_date_out_of_range(
    form_10k, apple_cik
):
    download_metadata = DownloadMetadata(
        download_folder=Path("."),
        form=form_10k,
        cik=apple_cik,
        limit=1,
        after=date(2022, 1, 1),
        before=date(2023, 1, 1),
        include_amends=True,
        download_details=True,
    )

    assert not within_requested_date_range(download_metadata, "2020-1-1")
