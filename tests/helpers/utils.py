import os


def parse_filing_document_header(file_path):
    parsed = {
        "ACCESSION NUMBER": [],
        "CONFORMED SUBMISSION TYPE": [],
        "COMPANY CONFORMED NAME": []
    }
    header = extract_header(file_path)
    for line in header:
        components = [l.strip() for l in line.split(":")]
        if (components[0] == "ACCESSION NUMBER" or components[0] == "CONFORMED SUBMISSION TYPE" or
                components[0] == "COMPANY CONFORMED NAME"):
            parsed[components[0]].append(components[1])
    return parsed


def extract_header(file_path):
    header = []
    with open(file_path, "r") as f:
        for line in f:
            # </SEC-HEADER> indicates the end of the header info
            if line == "</SEC-HEADER>\n":
                break
            header.append(line)
    return header


def verify_directory_structure(base_dir, filing_types, num_downloaded, symbol, full_cik, company_name):
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
        assert len(header_contents["ACCESSION NUMBER"]) == 1 and len(header_contents["CONFORMED SUBMISSION TYPE"]) == 1
        assert header_contents["ACCESSION NUMBER"][0] == accession_number
        header_submission = header_contents["CONFORMED SUBMISSION TYPE"][0]
        assert header_submission == ft or header_submission == f"{ft}/A"
        # lack of standard SEC-HEADER format makes it hard to exact match the company name
        # without more advanced edge-case parsing, so this is a good estimate of the check
        assert company_name in header_contents["COMPANY CONFORMED NAME"]


def strip_cik(full_cik):
    return full_cik.lstrip("0")
