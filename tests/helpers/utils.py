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


'''
==============
Example Header
==============

<SEC-DOCUMENT>0000320193-19-000063.txt : 20190430
<SEC-HEADER>0000320193-19-000063.hdr.sgml : 20190430
<ACCEPTANCE-DATETIME>20190430163016
ACCESSION NUMBER:		0000320193-19-000063
CONFORMED SUBMISSION TYPE:	8-K
PUBLIC DOCUMENT COUNT:		3
CONFORMED PERIOD OF REPORT:	20190430
ITEM INFORMATION:		Results of Operations and Financial Condition
ITEM INFORMATION:		Financial Statements and Exhibits
FILED AS OF DATE:		20190430
DATE AS OF CHANGE:		20190430
'''
