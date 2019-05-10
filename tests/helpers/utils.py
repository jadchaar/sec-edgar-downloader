import os
from pathlib import Path

def parse_filing_document_header(file_path):
    parsed = {}
    header = extract_header(file_path)
    for line in header:
        components = [l.strip() for l in line.split(":")]
        if components[0] == "ACCESSION NUMBER" or components[0] == "CONFORMED SUBMISSION TYPE":
            parsed[components[0]] = components[1]
    return parsed

def extract_header(file_path):
    header = []
    with open(file_path, "r") as f:
        for line in f:
            # A blank line indicates the end of the header info
            if line == "\n":
                break
            header.append(line)
    # Ignore <SEC-DOCUMENT>, <SEC-HEADER>, and <ACCEPTANCE-DATETIME>
    return header[3:]

def verify_directory_structure(base_dir, ticker_symbol, ticker_cik, filing_type):
    next_level_of_dir = Path.joinpath(base_dir, "sec-edgar-filings")
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == ticker_symbol

    next_level_of_dir = Path.joinpath(next_level_of_dir, ticker_symbol)
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == filing_type

    next_level_of_dir = Path.joinpath(next_level_of_dir, filing_type)
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1

    next_level_of_dir = Path.joinpath(next_level_of_dir, dir_content[0])
    assert next_level_of_dir.is_file()
    assert next_level_of_dir.suffix == ".txt"

    accession_number = next_level_of_dir.stem
    assert accession_number[:len(ticker_cik)] == ticker_cik

    header_contents = parse_filing_document_header(next_level_of_dir)
    assert header_contents["ACCESSION NUMBER"] == accession_number
    assert header_contents["CONFORMED SUBMISSION TYPE"] == filing_type
