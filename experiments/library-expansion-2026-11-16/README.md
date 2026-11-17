# Library expansion across all seventeen forms

The author confirmed **all applicable seventeen forms**, with approximately three worthwhile retrieval candidates per field/form. This pass assesses six source groups: business/management, engineering/computing, law/public policy, medicine/health, personal/public writing, and physical sciences/mathematics. Physics is separate because the supplied collection includes scientific reviews whose conventions differ from engineering documentation.

There are **235 candidate records**: **214 primary retrieval targets** and **21 conditional analogues or uncounted alternatives**. Seventy of the 102 assessed field/form cells have three direct candidates. Nine cells are not applicable within the selected stratum, fifteen are conditional, three have partial gaps, and five have no verified targets from this search. All seventeen forms have direct candidates somewhere in the list; this does not mean every applicable field/form target was filled.

The recorded years are 211 before 2015, eighteen in the separate 2015–2019 supplement, and six unresolved. Original dates, reprint/version dates and modern archive captures must stay distinct. Some official pages remain current or undated comparisons, not historical writing evidence. These are bibliographic retrieval candidates with provisional form assignments, not 235 inspected exemplary texts or new downloaded PDFs.

## Use these files

**Full-text follow-up, 16 November:** the [retrieval pass](../library-retrieval-2026-11-16/README.md) now supplies copies for 70 DOI works and 36 additional non-DOI targets, with a download bundle and remaining library lists. The original acquisition-planning records below are preserved as the earlier bibliographic snapshot.

- [First batch: eighteen works](first-pull-batch.md), with [CSV](first-pull-batch.csv): three per source group, selecting contrasting forms. This is a starting order, not a replacement for the full grid.
- [Complete readable shortlist](shortlist.md): all seventeen forms within each field, source reasons, version notes and visible gaps.
- [Primary library pull list](library-pull-list.csv): 214 titles, authors, dates, DOIs or alternate locators, source/form hypotheses, influence evidence and copy status.
- [RIS import](library-pull-list.ris): the same 214 retrieval works for reference managers.
- [DOIs only](dois-to-pull.txt): 154 unique supplied identifiers.
- [BibTeX pool](references/library.bib): generated retrieval entries with explicit verification fields. Here `verified` uses the search skill's DOI/PMID API convention; false does not by itself mean a non-DOI publisher/archive citation is false. Read `verified_by` and the CSV verification status.
- [Conditional examples and alternatives](conditional-and-alternate-candidates.csv): 21 records kept outside primary quotas.
- [Coverage matrix](coverage.csv): all 102 assessed cells and the reason for each status.
- [Complete candidate ledger](candidate-ledger.json), [summary](summary.json) and [validation receipt](validation.json).

## Identity, attention and suitability are separate

Field agents verified bibliography through live Crossref, PubMed, Europe PMC, publisher records, official archives or editorial/award sources as applicable. Their raw receipts and qualifications remain in the six field folders. Crossref redirected some publisher DOI records to alternate registry records; exact source versions and aliases still require care. A law empirical-reply DOI remains withheld because the bibliographic match was not resolved; its suspected identifier is a lead in its locator, not a verified DOI field.

The candidate ledger records 150 citation-count signals, 36 named editorial/award/bestseller signals, two publisher-access signals, 43 institutional/contextual selections without readership measures, and four relevant works lacking individual prominence evidence. These are different evidence kinds. A nonzero citation count is not automatically “highly cited,” an award is not a readership count, and publisher accesses are not unique readers. There is **no claim that every cell has three empirically proven widely read works**. The weaker selections identify where an authoritative source or a promising example was available but the desired individual influence evidence was not established.

Highly cited research can be a poor writing model. A publisher category can contain several forms. A systematic-review methods paper is not automatically a systematic-review example; a business case study is not a clinical case report; a physics review with numerical synthesis need not document systematic selection. Reference entries are bounded topics, not entire encyclopedias. The provisional field/form labels must be checked after retrieval.

All three original development articles and the nineteen full-coded pilot texts remain a separate known-source set. The merger checked the retained-source inventory, PDF retrieval metadata and derived-only legacy measurements using exact DOI and normalized-title keys. No primary target matched a previously retained XML/HTML body or reviewed pilot reconstruction under those keys. Three targets have retained PDF candidates whose identity/completeness is unresolved; review those files or obtain the publisher version. Two medical work reviews have legacy measurements without retained source bytes, so actual copies are useful. Unknown aliases, short titles, editions and earlier metadata may conceal overlap; the check is not a complete library inventory.

## Independent checks and parent corrections

The [independent audit](audit/report.md) checked the field schemas and selected primary metadata. Its initial bulk Crossref attempt was rate-limited; most rows were not independently reverified by that attempt. Do not mistake HTTP HEAD success for bibliographic identity, or a HEAD failure for proof that a work is absent. The original response log is retained in `audit/checks.json`. The checker now defaults to offline structural checks; optional live checks are bounded, sequential and stop Crossref work after a rate/access failure.

The parent independently found the original Los Angeles Times title/date for Solnit's 2008 article and separated that newspaper version from the later collection/longer versions. Its exact-version readership remains unquantified. The Gawker item has a corroborating Longreads metadata locator while original-publisher access remains unresolved. NIST SOP 14 now points to the 2013 parent publication record and names the exact procedure; it does not inherit a later edition DOI. [Parent overrides](parent-overrides.json) preserve corrections separately from the field originals.

## Reproduce the exports offline

```bash
python3 experiments/library-expansion-2026-11-16/analysis/build_queue.py
python3 experiments/library-expansion-2026-11-16/audit/check.py
python3 experiments/library-expansion-2026-11-16/analysis/validate_queue.py
```

The builder reads frozen field records, applies explicit parent corrections, reconciles coverage and existing-source indicators, and writes the readable/CSV/RIS/DOI exports. It appends unseen keys to the task's BibTeX pool rather than overwriting an existing bibliography. The validation checks source-file freshness, IDs, denominators and export counts. It does not make fresh network calls or certify source truth, article completeness, genre suitability, readership or writing quality.
