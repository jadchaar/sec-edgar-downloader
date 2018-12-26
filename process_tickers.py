from ftplib import FTP
import json
import os

raw_ticker_data_file = "stock_tickers.txt"
ticker_validation_json = "ticker_validation.json"
package_directory = "sec_edgar_downloader"

# Get all NASDAQ-traded tickers here:
# ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt
def get_tickers():
    print("Getting latest stock tickers from NASDAQ...")
    with FTP("ftp.nasdaqtrader.com") as ftp:
        ftp.login()
        ftp.cwd("SymbolDirectory")
        with open(raw_ticker_data_file, "wb") as f:
            ftp.retrbinary("RETR nasdaqtraded.txt", f.write)
    print(f"Stock tickers saved to {raw_ticker_data_file}")

def parse_tickers():
    print(f"Parsing stock tickers...")
    ticker_validation_dict = {}
    with open(raw_ticker_data_file, "r") as f:
        next(f) # ignore header
        for line in f:
            line_components = line.split("|")
            # ignore blank lines and final line (file creation time)
            if len(line_components[0]) != 1:
                continue
            ticker = line_components[1]
            # Value does not matter as we are only using
            # this JSON for validation purposes
            ticker_validation_dict[ticker] = 0

    with open(ticker_validation_json, "w") as f:
        json.dump(ticker_validation_dict, f)
    print(f"Stock tickers parsed successfully into {ticker_validation_json}")

def move_json_and_cleanup():
    print("Moving processed JSON file into the package directory...")
    os.rename(ticker_validation_json, f"{package_directory}/{ticker_validation_json}")

    print("Cleaning up...")
    os.remove(raw_ticker_data_file)


if __name__ == "__main__":
    get_tickers()
    parse_tickers()
    move_json_and_cleanup()
