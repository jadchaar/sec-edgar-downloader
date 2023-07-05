import sys
from typing import Optional, Union, Literal
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DownloadMetadata:
    """Class for representing internal download metadata."""
    download_folder: Path
    form: str
    cik: str
    limit: Optional[int] = sys.maxsize
    # TODO: default after (earliest possible date) and before (today)
    after: Optional[str] = None
    before: Optional[str] = None
    include_amends: bool = False


@dataclass
class FilingMetadata:
    """Class for representing internal filing metadata."""
    accession_number: str
    save_filename: str


@dataclass
class ToDownload:
    raw_filing_uri: str
    primary_doc_uri: str


DownloadPath = Union[str, Path]

DownloadType = Literal["EdgarAPI", "EdgarFiling"]
