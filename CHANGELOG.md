# Changelog

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