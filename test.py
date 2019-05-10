import sec_edgar_downloader

downloader = sec_edgar_downloader.Downloader()

# downloader.get_8k_filing("AAPL", 1)
# downloader.get_10k_filing("AAPL", 1)
# downloader.get_10q_filing("AAPL", 1)

# downloader.get_10k_filing("DANKMEMES", 1)
downloader.get_13f_filing("0000102909", 1)


# downloader.get_all_available_filings("AAPL")
# downloader.get_10k_filing("AAPL", 1)
# downloader.get_all_available_filings("0000102909")

# AAPL does not have 13Fs, so this should yield nothing
# downloader.get_13f_filing("AAPL")
# downloader.get_sc_13g_filing("AAPL")
# downloader.get_10k_filing("AAPL")
# downloader.get_13f_filing("0000102909")
