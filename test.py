from sec_edgar_downloader import Downloader

downloader = Downloader("Jad Chaar", "jad.chaar@gmail.com")

# downloader.get("10-K", "320193", limit=1)
downloader.get("10-K", "320193")
