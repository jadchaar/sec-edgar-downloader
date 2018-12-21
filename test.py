# import sec_edgar_downloader

# downloader = sec_edgar_downloader.Downloader()

# downloader.get_10k_filing_for_ticker("AAPL")

from sec_edgar_downloader import Downloader

downloader = Downloader()

# downloader.get_10k_filing_for_ticker("AAPL")
downloader.get_13f_filing_for_ticker("0000102909")
