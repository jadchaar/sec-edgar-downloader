# Changelog

## 3.0.2 - 3/9/2020

### Added

- Added a 0.15s delay to download logic in order to prevent rate-limiting by SEC Edgar.

## 3.0.1 - 1/6/2020

### Added

- Added support for S-1 filings.

## 3.0.0 - 1/5/2020

### Added

- Added the ability to download more than 100 filings.
- Added the ability to specify an `after_date` argument to the `get` method. Example usage:

```python
from sec_edgar_downloader import Downloader
dl = Downloader()

# Get all 8-K filings for Apple after January 1, 2017 and before March 25, 2017
dl.get("8-K", "AAPL", after_date="20170101", before_date="20170325")
```

- Added a `supported_filings` property to the `Downloader` class, which gets a list of all filings supported by the `sec_edgar_downloader` package. Example usage:

```python
from sec_edgar_downloader import Downloader
dl = Downloader()

dl.supported_filings
```

### Changed

- Package has been completely re-written from the ground up.
- The `Downloader` class now has a single `get` entry point method. This change was made to improve and ease maintainability. Here is the new stub for the `get` method:

```python
class Downloader:
    def get(
        self,
        filing_type,
        ticker_or_cik,
        num_filings_to_download=None,
        after_date=None,
        before_date=None,
        include_amends=False
    )
```

Example usage of the new method:

```python
from sec_edgar_downloader import Downloader
dl = Downloader()

# Get all 8-K filings for Apple
dl.get("8-K", "AAPL")
```

### Removed

- Replaced retrieval methods for each filing type with a single point of entry. The bulk method `get_all_available_filings` has also been removed, so any bulk actions need to be completed manually as follows:

```python
# Get the latest supported filings, if available, for Apple
for filing_type in dl.supported_filings:
    dl.get(filing_type, "AAPL", 1)

# Get the latest supported filings, if available, for a
# specified list of tickers and CIKs
symbols = ["AAPL", "MSFT", "0000102909", "V", "FB"]
for s in symbols:
    for filing_type in dl.supported_filings:
        dl.get(filing_type, s, 1)
```

## 2.2.1 - 9/18/2019

- Added support for [form 10KSB](https://www.vcexperts.com/definition/form-10-ksb).
- Added docs and tests to PyPI distribution package.
- Locked the `requests` dependency to `v2.22.0` or greater to ensure optimal performance and compatibility.

## 2.2.0 - 6/28/2019

- `sec-edgar-downloader` is now fully documented 🎉. You can view the latest documentation at [sec-edgar-downloader.readthedocs.io](https://sec-edgar-downloader.readthedocs.io).
- Changed file encoding for filing downloads from `utf-8` to `ascii`. This switch was made because SEC filings should be [submitted in ASCII format](https://www.sec.gov/info/edgar/quick-reference/create-ascii-files.pdf).
- Locked the `lxml` dependency to `v4.3.4` or greater to fix Python 3.8 install issues.

## 2.1.0 - 6/8/2019

- Added `before_date` parameter to each filing download method. If this value is not specified, it will default to the current date.
- Added `include_amends` parameter to each filing download method. If this value is not specified, it will default to false.
- Added support for passing relative (e.g. `./`, `../`) and user (e.g. `~/`) download paths to the `Downloader` constructor
- An `IOError` is no longer thrown when an invalid download path is passed to the `Downloader` constructor. Instead,`sec_edgar_downloader` will create all the necessary directories in the path if they do not exist.
- Filing documents are no longer downloaded in streamed chunks.
- Downloads are now written to disk with UTF-8 encoding.
- Added `__version__` variable to package.
- Travis CI now uses tox to lint and run tests.
- Added `verbose` flag to `Downloader` constructor to enable information printing (e.g. how many filings are found and downloaded). `verbose` will default to false, meaning that no download information will be printed by default.

## 2.0.1 - 5/13/2019

- Cleaned up README
- Tweaked package naming in setup.py

## 2.0.0 - 5/13/2019

- The method for obtaining 13F filings has been split up into two methods: one for obtaining 13F-NT filings and another one for obtaining 13F-HR filings
  - You can read about the differences [here](https://www.sec.gov/divisions/investment/13ffaq.htm)
- You can now specify the number of filings to download in the `get_all_available_filings` method
- Simplified API by combining ticker and CIK functionality into a single method for each filing type
  - Available methods: `get_8k_filings`, `get_10k_filings`, `get_10q_filings`, `get_13f_nt_filings`, `get_13f_hr_filings`, `get_sc_13g_filings`, `get_sd_filings`, `get_all_available_filings`
  - All these methods can be passed either a CIK or ticker string
- Removed ticker validation to facilitate this simplified API change
- Added a full suite of unit and integration tests along with an internal Travis CI pipeline for increased reliability
- Class methods now return the number of filings downloaded
- Added Python 3.8 support

## 1.2.0 - 2/14/2019

- Added the ability to specify the number of filings to download
  - For example, you can download the latest 10-K for MSFT with this command: `downloader.get_10k_filing_for_ticker("MSFT", 1)`
  - This is available for all non-bulk methods: `get_8k_filing_for_ticker`, `get_10k_filing_for_ticker`, `get_10q_filing_for_ticker`, `get_13f_filing_for_ticker`, `get_sc_13g_filing_for_ticker`, `get_sd_filing_for_ticker`, and the CIK equivalents

## 1.1.4 - 12/29/2018

- Internal renaming changes

## 1.1.3 - 12/28/2018

- Reduced size of ticker validation data by changing an internal data structure

## 1.1.2 - 12/27/2018

- Fixed the "FileNotFoundError" on import

## 1.1.1 - 12/26/2018

- Tweaked PyPI description

## 1.1.0 - 12/26/2018

- Filing downloads are now handled in chunks to improve download and save speed
- Removed get_select_filings_for_ticker() to reduce redundancy
- Added support for SC 13G filings
- Separated ticker and CIK class methods for easier use
- Added ticker symbol validation

## 1.0.1 - 12/20/2018

- Files now save as ".txt" rather than ".html"

## 1.0.0 - 12/20/2018

- Initial release
