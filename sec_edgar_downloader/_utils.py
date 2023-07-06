from datetime import date
from datetime import datetime as dt

from ._constants import DATE_FORMAT_TOKENS
from ._types import DownloadMetadata


def is_cik(ticker_or_cik: str) -> bool:
    try:
        int(ticker_or_cik)
        return True
    except ValueError:
        return False


def validate_and_parse_date(date_format: str) -> date:
    error_msg_base = "Please enter a date string of the form YYYY-MM-DD."

    if not isinstance(date_format, str):
        raise TypeError(error_msg_base)

    try:
        return dt.strptime(date_format, DATE_FORMAT_TOKENS).date()
    except ValueError as exc:
        # Re-raise with custom error message
        raise ValueError(f"Incorrect date format. {error_msg_base}") from exc


def within_requested_date_range(
    download_metadata: DownloadMetadata,
    filing_date: str,
) -> bool:
    target_date = dt.strptime(filing_date, DATE_FORMAT_TOKENS).date()
    return download_metadata.after <= target_date <= download_metadata.before
