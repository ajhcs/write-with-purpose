# Source extraction validation

25/25 checks passed.

- cached cole-cs50 hash: PASS
- cached cole-engineering hash: PASS
- cached doctorow hash: PASS
- cached python hash: PASS
- cached python-license hash: PASS
- S01 sha256: PASS
- S01 three unique spans: PASS
- S01 context: PASS
- S01 navigation patterns absent: PASS
- S02 sha256: PASS
- S02 three unique spans: PASS
- S02 context: PASS
- S02 navigation patterns absent: PASS
- S03 sha256: PASS
- S03 three unique spans: PASS
- S03 context: PASS
- S03 navigation patterns absent: PASS
- S04 sha256: PASS
- S04 three unique spans: PASS
- S04 context: PASS
- S04 navigation patterns absent: PASS
- all Python preformatted examples exact and ordered: PASS
- Python licence cached copy byte identical: PASS
- Doctorow source includes CC BY 4.0 rights statement: PASS
- all Cole article note sections present: PASS

## Scope and limitations

- Extraction is presentation conversion, not editorial rewriting: omitted article title, byline, dates, navigation, visual inserts and duplicated interactive note panels; kept narrative, notes, external links, and code.
- Doctorow source retains a third-party quotation as part of the source; the post expressly excludes quotations and images from its CC license.
- Paragraph selection uses exact Unicode offsets in the extracted Markdown; several windows are shorter than 120 words because of paragraph and section boundaries.
- Checks establish extraction and index consistency, not semantic gold, independent rights clearance for third-party quotations, or writing quality.

## Rights provenance

- doctorow: Cached original post colophon states Creative Commons Attribution 4.0 and excludes quotations and images; https://pluralistic.net/2023/01/21/potemkin-ai/ ; https://creativecommons.org/licenses/by/4.0/
- python: Cached Python license retained as sources/python-license.html; https://docs.python.org/3.8/license.html
- cole: User authorized use in this trial.
