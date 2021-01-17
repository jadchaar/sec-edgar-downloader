# sec_edgar_downloader v4 Migration Guide

v4 is a complete rewrite of the `sec_edgar_downloader` package. As part of this rewrite, a number of interfaces have changed. The following migration guide outlines the most disruptive changes and how to convert an existing codebase to use v4 of the package.

## Keyword-Only Arguments

`filing` and `ticker_or_cik` are now the only required arguments for calls to `dl.get()`. All other arguments are marked as keyword-only, and must be used as follows:

```python
dl = Downloader()
dl.get(
    "10-K",
    "AAPL",
    # All other arguments must be used with a keyword
    amount=1,
    after="2019-01-01",
    before="2021-01-01",
    include_amends=True,
    download_details=True,
    query="sample query"
)
```

In addition to keyword-only arguments, the `after_date`, `before_date`, `num_filings_to_download` kwargs have been renamed to `after`, `before`, and `amount`, respectively.

## Date Range of Downloads

The package now uses the [SEC Edgar Full Text Search API](https://www.sec.gov/edgar/search/) to fetch filing information, and this API is only capable of fetching filings after December 1, 2000. Thus, this package can only download filings filed after 2000-01-01.

## Folder Structure and Naming Changes

Assume the following sequence of calls:

```python
dl = Downloader()
dl.get("8-K", "AAPL", amount=2, download_details=True)
dl.get("10-K", "AAPL", amount=1, download_details=False)
dl.get("4", "IBM", amount=1, download_details=True)
```

These calls will output the following file structure:

```
    sec_edgar_filings
    ├── AAPL
    │   ├── 10-K
    │   │   └── 0000320193-20-000096
    │   │       └── full-submission.txt
    │   └── 8-K
    │       ├── 0000320193-20-000094
    │       │   ├── filing-details.html
    │       │   └── full-submission.txt
    │       └── 0001193125-20-225672
    │           ├── filing-details.html
    │           └── full-submission.txt
    └── IBM
        └── 4
            └── 0001562180-20-006712
                ├── filing-details.xml
                └── full-submission.txt
```

Filings are now downloaded into folders named after accession numbers.
The full filing is downloaded as a `txt` file named `full-submission.txt` in addition to a human-readable filing called `filing-details.*`, where `*` varies by filing type (e.g. certain submissions may include an `xml`, `pdf`, or `html` file). For example, `Form 4` submissions will include details in an `xml` file and `10-K` submissions will include a human-readable `html` file, to name a few.

## Specifying Download Location

When no path is passed to a `Downloader` object, the package will now default to downloading filings to the current working directory rather than attempting to locate a user's downloads folder.

## Formatting After and Before Dates

After and before dates must now be passed in the form `YYYY-MM-DD` to line up with the Edgar full-text search interface.
