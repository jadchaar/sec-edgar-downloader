from datetime import date

from pyrate_limiter import Duration, RequestRate

DATE_FORMAT_TOKENS = "%Y-%m-%d"
DEFAULT_BEFORE_DATE = date.today()
DEFAULT_AFTER_DATE = date(1994, 1, 1)

AMENDS_SUFFIX = "/A"

# 10 requests per second rate limit set by SEC:
# https://www.sec.gov/os/webmaster-faq#developers
SEC_RATE_LIMIT = RequestRate(10, Duration.SECOND)

HOST_WWW_SEC = "www.sec.gov"
HOST_DATA_SEC = "data.sec.gov"

URL_CIK_MAPPING = "https://www.sec.gov/files/company_tickers_exchange.json"
URL_FILING = (
    "https://www.sec.gov/Archives/edgar/data/{cik}/{acc_num_no_dash}/{document}"
)
URL_SUBMISSIONS = "https://data.sec.gov/submissions/{submission}"

SUBMISSION_FILE_FORMAT = "CIK{cik}.json"
STANDARD_HEADERS = {
    "Accept-Encoding": "gzip, deflate",
}

# Save metadata
ROOT_SAVE_FOLDER_NAME = "sec-edgar-filings"
FILING_FULL_SUBMISSION_FILENAME = "full-submission.txt"
PRIMARY_DOC_FILENAME_STEM = "primary-document"

CIK_LENGTH = 10
