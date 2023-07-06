from sec_edgar_downloader import Downloader

downloader = Downloader("Jad Chaar", "jad.chaar@gmail.com")

# downloader.get("10-K", "320193", limit=1)
downloader.get("10-K", "320193")

# downloader.get("10-K", "34088")

downloader.get("10-K", "34088", limit=3)
