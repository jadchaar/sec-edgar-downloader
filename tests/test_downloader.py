from unittest.mock import patch

import pytest


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


# def test_invalid_num_filings_to_download(downloader):
#     dl, _ = downloader
#     expected_msg = "Invalid amount. Please enter a number greater than 1."
#
#     filing_type = "10-K"
#     ticker = "AAPL"
#
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(filing_type, ticker, amount=-1)
#     assert expected_msg in str(exc_info.value)
#
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(filing_type, ticker, amount=0)
#     assert expected_msg in str(exc_info.value)
#
#
# def test_invalid_before_and_after_dates(downloader):
#     dl, _ = downloader
#     expected_msg = (
#         "Incorrect date format. Please enter a date string of the form YYYY-MM-DD."
#     )
#
#     filing_type = "8-K"
#     ticker = "AAPL"
#
#     # AAPL filed a 8-K on 2019-11-15
#     after_date = datetime(2019, 11, 15)
#     before_date = datetime(2019, 11, 15)
#     incorrect_date_format = "%Y%m%d"
#
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(filing_type, ticker, after=after_date.strftime(incorrect_date_format))
#     assert expected_msg in str(exc_info.value)
#
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(filing_type, ticker, before=before_date.strftime(incorrect_date_format))
#     assert expected_msg in str(exc_info.value)
#
#
# def test_valid_before_and_after_date_combos(downloader):
#     dl, _ = downloader
#
#     filing_type = "8-K"
#     ticker = "AAPL"
#
#     # AAPL filed a 8-K on 2019-11-15
#     after_date = datetime(2019, 11, 15)
#     before_date = datetime(2019, 11, 15)
#
#     # after_date == before_date
#     num_filings_downloaded = dl.get(
#         filing_type,
#         ticker,
#         after=after_date.strftime(DATE_FORMAT_TOKENS),
#         before=before_date.strftime(DATE_FORMAT_TOKENS),
#     )
#     assert num_filings_downloaded == 1
#
#     # after_date < before_date
#     after_date -= timedelta(days=1)
#     before_date += timedelta(days=1)
#     num_filings_downloaded = dl.get(
#         filing_type,
#         ticker,
#         after=after_date.strftime(DATE_FORMAT_TOKENS),
#         before=before_date.strftime(DATE_FORMAT_TOKENS),
#     )
#     assert num_filings_downloaded == 1
#
#
# def test_invalid_before_and_after_date_combos(downloader):
#     dl, _ = downloader
#
#     filing_type = "8-K"
#     ticker = "AAPL"
#
#     # AAPL filed a 8-K on 2019-11-15
#     after_date = datetime(2019, 11, 15)
#     before_date = datetime(2019, 11, 15)
#
#     # after_date > before_date
#     after_date += timedelta(days=3)
#     expected_msg = "Invalid after and before date combination."
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(
#             filing_type,
#             ticker,
#             after=after_date.strftime(DATE_FORMAT_TOKENS),
#             before=before_date.strftime(DATE_FORMAT_TOKENS),
#         )
#     assert expected_msg in str(exc_info.value)
#
#
# def test_pre_default_after_date(downloader):
#     dl, _ = downloader
#
#     filing_type = "8-K"
#     ticker = "AAPL"
#
#     invalid_date = DEFAULT_AFTER_DATE - timedelta(days=1)
#     expected_msg = f"Filings cannot be downloaded prior to {DEFAULT_AFTER_DATE.year}."
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(filing_type, ticker, after=invalid_date.strftime(DATE_FORMAT_TOKENS))
#     assert expected_msg in str(exc_info.value)
#
#
# def test_non_string_date(downloader):
#     dl, _ = downloader
#
#     filing_type = "8-K"
#     ticker = "AAPL"
#
#     with pytest.raises(TypeError):
#         dl.get(filing_type, ticker, after=DEFAULT_AFTER_DATE)
