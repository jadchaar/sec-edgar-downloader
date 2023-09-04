from datetime import date

from sec_edgar_downloader import Downloader

downloader = Downloader("Jad Chaar", "jad.chaar@gmail.com")

# downloader.get("10-K", "320193", limit=1)
# downloader.get("10-K", "320193")
#
# # downloader.get("10-K", "34088")
#
# downloader.get("10-K", "34088", limit=3)

# downloader.get("10-K", "AMZN", limit=1)
# downloader.get("10-K", "AAPL", limit=1, download_details=True)

# downloader.get(
#     "SC 13G", "0000102909", include_amends=True, limit=30, download_details=True
# )


downloader.get("4", "AAPL", limit=1, before=date(2020, 10, 13), download_details=True)

downloader.get("8-K", "AAPL", limit=1, before=date(2019, 11, 15), download_details=True)
