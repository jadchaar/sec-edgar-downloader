import sec_edgar_downloader

downloader = sec_edgar_downloader.Downloader()

# downloader.get_all_available_filings_for_ticker("AAPL")
downloader.get_all_available_filings_for_cik("0000102909")

# downloader.get_10k_filing_for_ticker("AAPL")

# AAPL does not have 13Fs, so this should yield nothing
# downloader.get_13f_filing_for_ticker("AAPL")
# downloader.get_sc_13g_filing_for_ticker("AAPL")
# downloader.get_10k_filing_for_ticker("AAPL")
# downloader.get_13f_filing_for_ticker("0000102909")
