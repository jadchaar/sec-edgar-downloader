import sys
from typing import Union, Literal
from pathlib import Path
from dataclasses import dataclass
from datetime import date
from ._constants import DEFAULT_AFTER_DATE, DEFAULT_BEFORE_DATE
from enum import Enum


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


# @dataclass
# class FilingMetadata:
#     """Class for representing internal filing metadata."""
#     accession_number: str
#     save_filename: str


@dataclass
class ToDownload:
    raw_filing_uri: str
    primary_doc_uri: str
    accession_number: str
    details_doc_suffix: str


DownloadPath = Union[str, Path]


class DownloadType(Enum):
    API = "EdgarAPI"
    FILING = "EdgarFiling"
