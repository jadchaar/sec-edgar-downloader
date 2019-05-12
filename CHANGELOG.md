# Changelog

## 2.0.0 - ~/~/2019

- The method for obtaining 13F filings has been split up into two methods: one for obtaining 13F-NT filings and another one for obtaining 13F-HR filings.
  - You can read about the differences [here](https://www.sec.gov/divisions/investment/13ffaq.htm).
- You can now specify the number of filings to download in the `get_all_available_filings` method.
- Simplified API by combining ticker and CIK functionality into a single method for each filing type.
  - Available methods: `get_8k_filings`, `get_10k_filings`, `get_10q_filings`, `get_13f_nt_filings`, `get_13f_hr_filings`, `get_sc_13g_filings`, `get_sd_filings`, `get_all_available_filings`.
  - All these methods can be passed either a CIK or ticker string.
- Removed ticker validation to facilitate this simplified API change.
- Added a full suite of unit and integration tests along with an internal Travis CI pipeline for increased reliability.
- Class methods now return the number of filings downloaded.

## 1.2.0 - 2/14/2019

- Added the ability to specify the number of filings to download.
  - For example, you can download the latest 10-K for MSFT with this command: `downloader.get_10k_filing_for_ticker("MSFT", 1)`
  - This is available for all non-bulk methods: `get_8k_filing_for_ticker`, `get_10k_filing_for_ticker`, `get_10q_filing_for_ticker`, `get_13f_filing_for_ticker`, `get_sc_13g_filing_for_ticker`, `get_sd_filing_for_ticker`, and the CIK equivalents

## 1.1.4 - 12/29/2018

- Internal renaming changes.

## 1.1.3 - 12/28/2018

- Reduced size of ticker validation data by changing an internal data structure.

## 1.1.2 - 12/27/2018

- Fixed the "FileNotFoundError" on import.

## 1.1.1 - 12/26/2018

- Tweaked PyPI description.

## 1.1.0 - 12/26/2018

- Filing downloads are now handled in chunks to improve download and save speed.
- Removed get_select_filings_for_ticker() to reduce redundancy.
- Added support for SC 13G filings.
- Separated ticker and CIK class methods for easier use.
- Added ticker symbol validation.

## 1.0.1 - 12/20/2018

- Files now save as ".txt" rather than ".html"

## 1.0.0 - 12/20/2018

- Initial release
