from datetime import date, datetime
from pathlib import Path

from ._constants import SEC_EDGAR_BASE_URL, SUPPORTED_FILINGS
from ._utils import get_filing_urls_to_download, validate_date_format


class Downloader:
    def __init__(self, download_folder=None):
        if download_folder is None:
            self.download_folder = Path.home().joinpath("Downloads")
        else:
            self.download_folder = Path(download_folder).expanduser().resolve()

    # TODO: add methods for getting and setting download_folder

    # TODO: should the default for num_filings_to_download be all?
    def get(
        self,
        filing_type,
        ticker_or_cik,
        num_filings_to_download=100,
        before_date=None,
        after_date=None,
        include_amends=False,
    ):
        if filing_type not in SUPPORTED_FILINGS:
            raise ValueError(
                f"'{filing_type}' filings are not supported. Please choose from the following: {', '.join(sorted(SUPPORTED_FILINGS))}."
            )

        ticker_or_cik = str(ticker_or_cik).strip().upper().lstrip("0")

        num_filings_to_download = int(num_filings_to_download)
        if num_filings_to_download < 1:
            raise ValueError(
                "Please enter a number greater than 1 for the number of filings to download."
            )

        if before_date is None:
            before_date = date.today().strftime("%Y%m%d")
        else:
            before_date = str(before_date)
            validate_date_format(before_date)

        # no sensible default exists for after_date
        if after_date is not None:
            after_date = str(after_date)
            validate_date_format(after_date)

        # TODO: add ability for user to pass in datetime objects?
        # TODO: add validation that after_date is less than before_date

        get_filing_urls_to_download(
            ticker_or_cik,
            filing_type,
            num_filings_to_download,
            before_date,
            after_date,
            include_amends,
        )
