# Empirical reports and methods papers: exploratory corpus

These are citation-ranked open-access samples, not global rankings or prescribed writing limits. Measured results reflect the sources and automated screens below; no independent full-text editorial suitability review was performed. Treat all results as provisional observed distributions. Counts can change as Europe PMC updates its index.

## Discovery and classification

- **Empirical:** pre-2015, Europe PMC randomized controlled trial publication-type metadata; JATS research-article, visible design/method and results headings, and at least 300 extracted prose words. This is a medical-trial subset, not all empirical research. Publication metadata and headings are screening evidence, not a manual assessment of every study.
- **Methods:** MethodsX journal, OA, title matching a method-contribution cue; excluded review/protocol title cues and non-research JATS types. This is a single-journal subset, mostly later than 2014, and title cues are a conservative imperfect proxy for article type. Elsevier describes MethodsX as publishing methodological advances as well as protocols and reviews: https://www.elsevier.com/researcher/author/tools-and-resources/research-elements-journals. Individual titles and source records remain available for review.
- Both pools use `SORT_CITED:y` from Europe PMC and retain the source citation count and query snapshot. Download failures, exclusions, and quota overflow appear in the manifest; not measured means not included in distributions. Candidate ranks record the order returned by Europe PMC; screening is bounded and may stop before every candidate is examined. High citation is a discovery signal, not evidence of writing quality.

## Extraction policy

Europe PMC OA full-text JATS XML, cached outside this repository on the verified Samsung workspace. A manifest row has URL, title, date, journal, DOI, source publication type, JATS type/category, selection reason, SHA-256 and retrieval timestamp where XML was retrieved. The repository contains derived measurements, not the copyrighted source texts. Licenses should be checked per source.

Main text comprises paragraph elements in body prose, including nested sections and direct body paragraphs. Excludes abstract, references, headings, citations/xrefs, figures, tables, captions, formulas, lists, boxed text, and supplementary material. Administrative sections with exact headings such as acknowledgments, competing interests, author contributions, funding, ethics, data availability, abbreviations and pre-publication history are excluded and their prose-word count retained separately; heading variants may escape this screen. Nested administrative headings are excluded from section totals. Top-level section totals include nested section paragraphs; unsectioned direct-body paragraphs are in total but not section totals. Counts of abstract, title and captions are separate. Citation cross-references count JATS bibr xref elements, including grouped references as one marker, with top-level section locations recorded separately. Reference, figure and table counts are element counts, not guarantees of unique conceptual objects. Unicode letter/digit word tokens include internal hyphens/apostrophes; characters include token punctuation. Sentence splitting is a punctuation/capital heuristic and can err on abbreviations, formulas, and unusual typography. Paragraph and sentence count arrays and section counts are in the manifest. The summary does not measure communicative functions, meaning, prose/list proportions, or semantic evidence placement.

## Reproduction

The scripts require Python 3 and the existing `requests` package. The first collector pass screens ranks 1–500; the separate continuation screens ranks 501–1000. The final merger applies a 200-work quota in source rank order and recomputes all measurements from cached XML, including the administrative exclusions. Queries and citation counts can change on a fresh run; the cache and snapshots are stored under `/workspace/repos/builderbob/.writing-corpus-cache/empirical-methods`.

```sh
CORPUS_FORM=empirical python3 collect.py
CORPUS_FORM=methods CORPUS_OUTPUT=/workspace/repos/builderbob/.writing-corpus-cache/empirical-methods/methods-run python3 collect.py
python3 continue_methods.py
python3 summarize.py
```

Run these commands from this directory. The recorded collection used six workers for the empirical pass and three for each methods pass; the default is three.

## Results

Values below are minimum / first quartile / median / third quartile / maximum, with quartiles linearly interpolated across works. Paragraphs and sentences are totals per work; the manifest contains per-paragraph and per-sentence counts. These are observed ranges, not hard limits.

### Empirical

Measured **200** of 275 screened candidates; target 200, shortfall 0. Status counts: excluded 41, measured 200, unavailable 34.

| Measure | Observed range and quartiles |
| --- | --- |
| Main-text words | 1,989 / 3,240.0 / 3,819.0 / 4,365.0 / 7,688 |
| Paragraphs | 13 / 27.8 / 33.0 / 40.0 / 65 |
| Sentences | 83 / 123.0 / 143.5 / 169.0 / 274 |
| Top-level sections | 3 / 4.0 / 5.0 / 7.0 / 16 |
| Figures | 0 / 1.0 / 3.0 / 4.0 / 9 |
| Tables | 0 / 2.0 / 3.0 / 4.0 / 9 |
| References | 11 / 25.0 / 32.0 / 40.0 / 83 |
| Citation markers | 12 / 31.0 / 41.5 / 53.2 / 129 |

| Publication year | Measured | Main-text words: min / Q1 / median / Q3 / max |
| --- | ---: | --- |
| Through 2014 | 200 | 1,989 / 3,240.0 / 3,819.0 / 4,365.0 / 7,688 |
| 2015–2019 | 0 | n/a |
| 2020 onward | 0 | n/a |

### Methods

Measured **200** of 650 screened candidates; target 200, shortfall 0. Status counts: excluded 426, measured 200, unavailable 24.

| Measure | Observed range and quartiles |
| --- | --- |
| Main-text words | 414 / 1,456.0 / 2,058.0 / 2,946.5 / 10,633 |
| Paragraphs | 3 / 13.8 / 20.0 / 32.2 / 283 |
| Sentences | 19 / 57.0 / 88.5 / 132.5 / 427 |
| Top-level sections | 0 / 3.0 / 5.0 / 7.0 / 14 |
| Figures | 0 / 1.0 / 3.0 / 5.0 / 18 |
| Tables | 0 / 1.0 / 2.0 / 3.0 / 15 |
| References | 1 / 10.0 / 16.0 / 27.2 / 79 |
| Citation markers | 0 / 12.0 / 20.5 / 35.2 / 130 |

| Publication year | Measured | Main-text words: min / Q1 / median / Q3 / max |
| --- | ---: | --- |
| Through 2014 | 15 | 916 / 1,209.5 / 1,647.0 / 1,864.0 / 2,942 |
| 2015–2019 | 82 | 694 / 1,243.2 / 1,709.5 / 2,466.8 / 5,382 |
| 2020 onward | 103 | 414 / 1,695.0 / 2,496.0 / 3,422.5 / 10,633 |

