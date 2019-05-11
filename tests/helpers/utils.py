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
            # "FILER:" indicates the end of the useful header info
            if line == "FILER:\n":
                break
            header.append(line)
    return header


def verify_directory_structure(base_dir, filing_types, num_downloaded, ticker_symbol, ticker_full_cik):
    # no ticker symbol available (only CIK)
    if ticker_symbol is None:
        ticker_symbol = strip_cik(ticker_full_cik)

    dir_content = os.listdir(base_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == "sec_edgar_filings"

    next_level_of_dir = base_dir.joinpath("sec_edgar_filings")
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == ticker_symbol

    next_level_of_dir = next_level_of_dir.joinpath(ticker_symbol)
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == len(filing_types)

    for i in range(len(filing_types)):
        assert filing_types[i] in dir_content

    for ft in filing_types:
        next_level_of_dir_tmp = next_level_of_dir.joinpath(ft)
        print(next_level_of_dir_tmp)
        assert next_level_of_dir_tmp.is_dir()
        dir_content = os.listdir(next_level_of_dir_tmp)
        assert len(dir_content) == num_downloaded

        next_level_of_dir_tmp = next_level_of_dir_tmp.joinpath(dir_content[0])
        assert next_level_of_dir_tmp.is_file()
        assert next_level_of_dir_tmp.suffix == ".txt"

        accession_number = next_level_of_dir_tmp.stem
        # assert accession_number[:len(ticker_full_cik)] == ticker_full_cik

        header_contents = parse_filing_document_header(next_level_of_dir_tmp)
        assert header_contents["ACCESSION NUMBER"] == accession_number
        # second condition accounts for amendments
        assert header_contents["CONFORMED SUBMISSION TYPE"] == ft or header_contents[
            "CONFORMED SUBMISSION TYPE"] == f"{ft}/A"


def strip_cik(full_cik):
    return full_cik.lstrip("0")
