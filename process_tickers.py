'''
Run script and copy output to clipboard:
python3 process_tickers.py | pbcopy
'''

from ftplib import FTP
import json
import os

raw_ticker_data_file = "stock_tickers.txt"

# Get all NASDAQ-traded tickers here:
# ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt
def get_tickers():
    with FTP("ftp.nasdaqtrader.com") as ftp:
        ftp.login()
        ftp.cwd("SymbolDirectory")
        with open(raw_ticker_data_file, "wb") as f:
            ftp.retrbinary("RETR nasdaqtraded.txt", f.write)

def parse_tickers():
    ticker_validation_set = set()
    with open(raw_ticker_data_file, "r") as f:
        next(f) # ignore header
        for line in f:
            line_components = line.split("|")
            # ignore blank lines and final line (file creation time)
            if len(line_components[0]) != 1:
                continue
            ticker = line_components[1]
            ticker_validation_set.add(ticker)
    print(ticker_validation_set)

if __name__ == "__main__":
    get_tickers()
    parse_tickers()
    os.remove(raw_ticker_data_file)
