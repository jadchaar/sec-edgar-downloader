"""Shared utility functions for testing suite."""

import os
import string
from datetime import datetime


def parse_filing_document_header(file_path):
    parsed = {
        "ACCESSION NUMBER": [],
        "CONFORMED SUBMISSION TYPE": [],
        "COMPANY CONFORMED NAME": [],
        "FILED AS OF DATE": [],
    }
    header = extract_header(file_path)
    for line in header:
        components = [l.strip() for l in line.split(":")]
        if (
            components[0] == "ACCESSION NUMBER"
            or components[0] == "CONFORMED SUBMISSION TYPE"
            or components[0] == "COMPANY CONFORMED NAME"
            or components[0] == "FILED AS OF DATE"
        ):
            # Strip punctuation from company name and normalize case
            # Useful for company names that may be inconsistent
            # such as APPLE INC and Apple Inc.
            if components[0] == "COMPANY CONFORMED NAME":
                # https://stackoverflow.com/q/265960
                components[1] = (
                    components[1]
                    .translate(str.maketrans("", "", string.punctuation))
                    .lower()
                )
            parsed[components[0]].append(components[1])
    return parsed


def extract_header(file_path):
    header = []
    with open(file_path, "r", encoding="ascii") as f:
        for line in f:
            # </SEC-HEADER> indicates the end of the header info
            if line == "</SEC-HEADER>\n":
                break
            header.append(line)
    return header


def verify_directory_structure(
    base_dir,
    filing_types,
    num_downloaded,
    symbol,
    full_cik,
    company_name,
    before_date=None,
    amends_included=False,
):
    # no ticker symbol available (only CIK)
    if symbol is None:
        symbol = strip_cik(full_cik)

    dir_content = os.listdir(base_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == "sec_edgar_filings"

    next_level_of_dir = base_dir.joinpath("sec_edgar_filings")
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == 1
    assert dir_content[0] == symbol

    next_level_of_dir = next_level_of_dir.joinpath(symbol)
    assert next_level_of_dir.is_dir()
    dir_content = os.listdir(next_level_of_dir)
    assert len(dir_content) == len(filing_types)

    for i in range(len(filing_types)):
        assert filing_types[i] in dir_content

    for ft in filing_types:
        next_level_of_dir_tmp = next_level_of_dir.joinpath(ft)
        assert next_level_of_dir_tmp.is_dir()
        dir_content = os.listdir(next_level_of_dir_tmp)
        assert len(dir_content) == num_downloaded

        next_level_of_dir_tmp = next_level_of_dir_tmp.joinpath(dir_content[0])
        assert next_level_of_dir_tmp.is_file()
        assert next_level_of_dir_tmp.suffix == ".txt"

        accession_number = next_level_of_dir_tmp.stem
        # assert accession_number[:len(full_cik)] == full_cik

        header_contents = parse_filing_document_header(next_level_of_dir_tmp)
        assert (
            len(header_contents["ACCESSION NUMBER"]) == 1
            and len(header_contents["CONFORMED SUBMISSION TYPE"]) == 1
        )
        assert header_contents["ACCESSION NUMBER"][0] == accession_number
        header_submission = header_contents["CONFORMED SUBMISSION TYPE"][0]
        if amends_included:
            assert header_submission == ft or header_submission == f"{ft}/A"
        else:
            assert header_submission == ft
        # lack of standard SEC-HEADER format makes it hard to exact match the company name
        # without more advanced edge-case parsing, so this is a good estimate of the check
        assert company_name.lower() in header_contents["COMPANY CONFORMED NAME"]

        if before_date is not None:
            filing_date = datetime.strptime(
                header_contents["FILED AS OF DATE"][0], "%Y%m%d"
            )
            assert filing_date <= datetime.strptime(before_date, "%Y%m%d")


def strip_cik(full_cik):
    return full_cik.lstrip("0")
