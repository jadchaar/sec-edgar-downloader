import pytest


def test_invalid_filing_type(downloader):
    dl, _ = downloader
    invalid_filing_type = "10-INVALID"
    ticker = "AAPL"

    with pytest.raises(ValueError) as exc_info:
        dl.get(invalid_filing_type, ticker)

    assert "'10-INVALID' forms are not supported" in str(exc_info)


def test_invalid_ticker(downloader):
    dl, dl_path = downloader
    filing_type = "10-K"
    invalid_ticker = "INVALIDTICKER"

    with pytest.raises(ValueError) as exc_info:
        dl.get(filing_type, invalid_ticker)

    assert "Ticker is invalid" in str(exc_info)


# def test_invalid_cik(downloader):
#     dl, _ = downloader
#     expected_msg = "Invalid CIK. CIKs must be at most 10 digits long."
#
#     filing_type = "10-K"
#     cik = "12345678910"
#
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(filing_type, cik, amount=1)
#     assert expected_msg in str(exc_info.value)
#
#
# def test_blank_ticker(downloader):
#     dl, _ = downloader
#     expected_msg = "Invalid ticker or CIK. Please enter a non-blank value."
#
#     filing_type = "10-K"
#     ticker = ""
#
#     with pytest.raises(ValueError) as exc_info:
#         dl.get(filing_type, ticker, amount=1)
#     assert expected_msg in str(exc_info.value)
#
#
# def test_cik_zero_padding(downloader):
#     # Regression test for issue #84
#     dl, dl_path = downloader
#
#     filing_type = "10-K"
#     cik = "0000789019"
#     num_filings_downloaded_full_cik = dl.get(filing_type, cik, amount=1)
#
#     trimmed_cik = "789019"
#     num_filings_downloaded_trimmed_cik = dl.get(filing_type, trimmed_cik, amount=1)
#
#     assert num_filings_downloaded_full_cik == 1
#     assert num_filings_downloaded_trimmed_cik == 1
#
#     # Both filings should be saved under the directory 0000789019
#     # if the CIK is properly padded. If zero-padding was not being done
#     # properly, we would have two parent directories of 789019 and 0000789019.
#     assert len(list(dl_path.glob("*"))) == 1
#
#
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
