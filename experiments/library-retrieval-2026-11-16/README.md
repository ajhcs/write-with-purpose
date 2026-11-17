# Full-text retrieval and remaining library requests

Completed 16 November 2026 against the preserved library-expansion shortlist. The approximate “150” list is the **154 unique DOI works**. The broader shortlist also contains sixty non-DOI targets, which were searched separately.

| Requested set | Requested works | Matched copy obtained | Remaining |
| --- | --- | --- | --- |
| DOI list | 154 | **70** | **84** |
| Additional non-DOI targets | 60 | **36** | **24** |
| All requested works | 214 | **106** | **108** |

The delivery has 78 preferred PDFs, twenty-one original full HTML pages, six pinned documentation-source records and one official RFC text. Three reference entries share one source file, so there are **104 unique full-text files for 106 requested works**. Three preferred copies were recovered from the existing local collection; counts are reconciled copies, not 106 newly discovered publications.

## Downloads and library remainder

- [Full-text bundle](/workspace/build/builderbob/write-with-purpose/library-retrieval-2026-11-16/retrieved-fulltexts.zip), approximately 95 MiB. Filenames are readable, grouped by field; its index maps each requested work to its file and source URL.
- [Remaining 84 DOI works](remaining-doi.csv), with [DOIs only](remaining-dois.txt).
- [Remaining 24 additional works](remaining-additional.csv).
- [Readable remaining list by field](remaining-list.md), [combined CSV](remaining-all.csv), and [RIS import for the 108 remaining works](remaining-library-pull.ris).
- [Retrieved-copy index](retrieved.csv), [complete results](all-results.csv), and [DOI works with text but no selected PDF](doi-text-without-pdf.csv).
- [Machine-readable source ledger](retrieval-ledger.json), [counts](summary.json), and [bundle hashes](delivery.json).

The remaining list includes title, author(s), date, form, DOI or stable locator, candidate-file paths and retrieval notes. A remaining item may have a blocked public route, an unavailable download, a timeout, a different work at a promising URL, or an unconfirmed candidate. It is not automatically classified as paywalled. The author can use the CSV or RIS with library access; the original shortlist is unchanged.

## What was checked

The pass consulted Europe PMC, OpenAlex, Crossref, registered publisher sources, public author/institutional repositories, and title/author web searches. Existing PDF candidates were indexed first. Found candidates were downloaded, not merely listed as links. Requests were paced; access and rate failures remain in their receipts. Unpaywall was not called because no real contact email was configured; no substitute email was invented. This exhausts the attempted public routes and discovered candidate URLs for unresolved items, not every possible copy on the Internet.

PDF candidates retain file hashes, source URLs, page counts and the fulltext-retrieval skill's original bounded identity assessment. Additional layout-text and first-page OCR checks look for the complete normalized title and the author surname on the same reviewed front page. Explicitly recorded title variants remove catalogue labels or appended investigator-group attributions; they do not silently rewrite the original bibliography. Eight source-specific parent reviews are retained in [manual-pdf-decisions.json](manual-pdf-decisions.json), including two extracted procedures. Automated identity warnings remain visible even when additional review accepts the work. A title/author match does not independently certify publication authenticity, every page's completeness, exact edition or suitability as a writing exemplar. Author manuscripts and reprints can differ from publisher versions.

Complete article-body HTML is accepted only through recorded source review and, for the academic HTML copies, matching citation DOI metadata. Original pages retain references and surrounding furniture; external figures/styles were not mirrored. SEC's shareholder proposal is available inside the exact complete proxy source, with that container scope recorded. FRUS copies are official archival document transcriptions. Documentation copies preserve the exact registered repository commit and file; reference-entry selection remains a later analysis step.

The two NIST procedures are complete numbered original-page subsets: SOP 9, September 2014, parent PDF pages 134–140 (procedure pages 1–7); SOP 14, April 2013, parent pages 35–53 (procedure pages 1–19). Parent manuals, original hashes, page mappings and source dates are retained. No prose was rewritten or reflowed into a simulated publisher PDF.

One important version correction: the existing uploaded **How Will You Measure Your Life?** file is a 168-page Christensen/Allworth/Dillon book. The request is for the **2010 HBR essay**. It remains on the retrieval list; the book is preserved and is not counted as that article. [Version decision](version-decisions.json).

All 214 rows received a first-pass retrieval result. Search queries and discovered URLs are recorded in `searches/`; full search responses, API responses, raw candidates and source text stay in the private persistent `/workspace` cache. A stalled supplementary HTTP worker was stopped after 141/142 completed futures; the downloader gained a total-transfer ceiling and completed the remaining discovered routes on a resumed pass. [Interruption record](interrupted-run.json). The final unattempted-discovery list is [empty](pending-discovered-urls.json).

## Verification and reuse

The delivery builder checks every declared candidate-file hash, validates accepted JATS DOI/body bindings, retains original and supplementary identity evidence, reconciles the 154/60 partition and writes one preferred file per work to the bundle. All archive members pass CRC checks, and their decompressed SHA-256 hashes match the retained selected files. A separate final readback checks the CSV partitions, actual PDF headers and the bundle/index mappings in [validation.json](validation.json).

The fulltext-retrieval skill is read and imported; installed skill files are unchanged. Task-local scripts live in `analysis/`. They use the existing `medsci-python`/Poppler/Tesseract runtime; the NIST page subsets used `medsci-pdf-python`. No package installation, library login, Git staging or publication was performed. Copies are retrieval material; no new function labels, writing profiles or rule adoption follows from acquisition.

Source cache: `/workspace/repos/builderbob/.writing-corpus-cache/library-retrieval-2026-11-16/`. Selected originals and provenance are retained even after packaging. Rebuild the exports offline with:

```bash
medsci-python experiments/library-retrieval-2026-11-16/analysis/build_delivery.py
python3 experiments/library-retrieval-2026-11-16/analysis/validate_delivery.py
```

This changes generated timestamps and bundle metadata; refresh validation and the checkpoint after a rebuild. The readable report and accepted-copy counts describe this run, not a promise about future host availability.
