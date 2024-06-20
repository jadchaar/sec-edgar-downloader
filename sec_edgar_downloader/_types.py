import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Set, Union

from ._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE


@dataclass
class DownloadMetadata:
    """Class for representing internal download metadata."""

    download_folder: Path
    form: str
    cik: str
    limit: int = sys.maxsize
    after: date = DEFAULT_AFTER_DATE
    before: date = DEFAULT_BEFORE_DATE
    include_amends: bool = False
    download_details: bool = False
    ticker: Optional[str] = None
    accession_numbers_to_skip: Optional[Set[str]] = None


@dataclass
class ToDownload:
    raw_filing_uri: str
    primary_doc_uri: str
    accession_number: str
    details_doc_suffix: str


DownloadPath = Union[str, Path]

Date = Union[str, date, datetime]
