from datetime import date
from datetime import datetime
from datetime import datetime as dt
from typing import Dict

from ._constants import CIK_LENGTH, DATE_FORMAT_TOKENS
from ._types import Date, DownloadMetadata


def is_cik(ticker_or_cik: str) -> bool:
    try:
        int(ticker_or_cik)
        return True
    except ValueError:
        return False


def validate_and_convert_ticker_or_cik(
    ticker_or_cik: str, ticker_to_cik_mapping: Dict[str, str]
) -> str:
    ticker_or_cik = str(ticker_or_cik).strip().upper()

    # Check for blank tickers or CIKs
    if not ticker_or_cik:
        raise ValueError("Invalid ticker or CIK. Please enter a non-blank value.")

    # Detect CIKs and ensure that they are properly zero-padded
    if is_cik(ticker_or_cik):
        if len(ticker_or_cik) > CIK_LENGTH:
            raise ValueError("Invalid CIK. CIKs must be at most 10 digits long.")
        # SEC Edgar APIs require zero-padded CIKs, so we must pad CIK with 0s
        # to ensure that it is exactly 10 digits long
        return ticker_or_cik.zfill(CIK_LENGTH)

    cik = ticker_to_cik_mapping.get(ticker_or_cik)

    if cik is None:
        raise ValueError(
            f"Ticker {repr(ticker_or_cik)} is invalid and cannot be mapped to a CIK. "
            "Please enter a valid ticker or CIK."
        )

    return cik


def validate_and_parse_date(input_date: Date) -> date:
    if isinstance(input_date, datetime):
        return input_date.date()
    elif isinstance(input_date, date):
        return input_date
    elif isinstance(input_date, str):
        try:
            return dt.strptime(input_date, DATE_FORMAT_TOKENS).date()
        except ValueError as exc:
            # Re-raise with custom error message
            raise ValueError(
                "Incorrect date format. Please enter a date string of the form YYYY-MM-DD."
            ) from exc
    else:
        raise TypeError(
            "Incorrect date input. Must be of type string, date, or datetime."
        )


def within_requested_date_range(
    download_metadata: DownloadMetadata,
    filing_date: str,
) -> bool:
    target_date = dt.strptime(filing_date, DATE_FORMAT_TOKENS).date()
    return download_metadata.after <= target_date <= download_metadata.before
