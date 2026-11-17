# Independent shortlist audit, 2026-11-16

Scope: metadata and locator checks only; no article PDFs downloaded. `checks.json` records per-row HTTP outcomes and the structural audit. `check.py` is the reproducible checker. This is not a full-text writing-quality assessment. Citations and editorial selections signal influence, not readership or quality.

## Findings requiring attention

- `p05`: the original Gawker URL returned HTTP 404 to HEAD; this alone does not establish GET failure. [Longreads](https://longreads.com/2014/11/30/my-vassar-college-faculty-id-makes-everything-ok/) independently gives Kiese Laymon, Gawker, 29 November 2014. Flag original access as unresolved and include that metadata locator for retrieval.
- `psm_33`: its NIST PDF locator returned 404 to HEAD, although search indexing locates the same PDF. Use the [2013 NIST publication record](https://www.nist.gov/publications/selected-procedures-volumetric-calibrations-2013-ed) as an additional metadata locator. SOP 14 is a procedure within NISTIR 7383, not a standalone article or the entire container; identify the SOP and edition explicitly. Do not infer a PDF access failure solely from HEAD.
- Business had unreferenced `business_014`, `business_015`, `business_017`, `business_042` at audit snapshot; the field was actively changing. Re-run reconciliation against the frozen files before delivery. Unreferenced candidates should not silently count toward a cell.
- Medicine reference entries, proposals and decision memos are explicitly conditional analogues, not three primary targets. Law tutorial, procedure and reference entries are likewise conditional analogues, including undated/current versions. Preserve that distinction in aggregated counts. Personal has four filled cells, not seventeen; physical sciences has four unfilled research-form cells and only one decision memorandum.
- `law_w4237793781` has null DOI but a DOI URL; do not invent a DOI, but reconcile this inconsistency against the publisher before claiming it is absent. The article is a reply and its fit as an empirical report needs content-level review.

## Structural scope

The stable law, medicine, personal, and physical-sciences snapshots have 44, 51, 12, and 37 candidate rows respectively. Each has exactly the contract's 17 coverage form IDs, and each listed ID exists, belongs to its cell, agrees with `provided`, and is referenced exactly once within its cell. The engineering snapshot (42 rows) also passed these structural checks; business (47) had the four unreferenced rows noted above. These checks do not independently establish bibliographic identity or form fit. Files may have changed after capture; run the checker after freeze.

## Selected primary metadata checks

- `medicine-critical_review_of_work-1`: [PubMed](https://pubmed.ncbi.nlm.nih.gov/29405744/) identifies Lita M. Proctor, 2014, 28(9), 3821–3822, DOI 10.1096/fj.14-0901ufm. The DOI names the review, not the reviewed book.
- `medicine-study_review_protocol-1`: [PubMed](https://pubmed.ncbi.nlm.nih.gov/15178990/) identifies the 2004 ICSS study protocol, Featherstone, Brown and Coward / ICSS Investigators, DOI 10.1159/000078753, with an abstract describing its planned design and outcomes.
- `law_w2657814049`: the [Harvard Law Review publisher record](https://harvardlawreview.org/print/vol-128/the-laws-of-capitalism/) identifies the specific review. `law_w1578338854`: the [Texas A&M repository record](https://scholarship.law.tamu.edu/facscholar/2481/) identifies Solum's review. Identify reviewer, not the author of the reviewed book, in exports.
- `psm_01`: [Caltech's record](https://calteches.library.caltech.edu/3090/) identifies Feynman, 1976, Engineering and Science 39(2), 11–30. `psm_02`: [Nobel's autobiographical page](https://www.nobelprize.org/prizes/physics/2001/cornell/biographical/) is first-person Cornell; distinguish the 2001 Nobel reference from a confirmed page publication date.
- `p04`: [Atlantic publisher record](https://www.theatlantic.com/magazine/archive/2014/06/the-case-for-reparations/361631/) identifies Coates's 2014 article. `p05`: original publisher returned 404 to HEAD; secondary metadata corroboration is listed above, so primary confirmation remains unresolved.

## Limits and follow-up

The checker attempted every listed primary locator with HEAD for non-DOI rows and Crossref metadata GET for DOI rows. HTTP 403, 404 to HEAD, 429 and bot challenges are inconclusive about article existence; consult `checks.json` for each outcome. Crossref rate-limited the bulk run, so most DOI metadata were **not** independently confirmed by this audit. A successful HEAD only establishes endpoint response, not identity, year or authors. Retry targeted DOI metadata serially through primary registries/publishers and parse source receipts, especially any high-risk review, protocol, historical version, or mismatch. Do not represent the bulk HTTP attempt as a live metadata pass. The two case-specific medical primary checks above verify individual metadata, not the complete medicine set. All non-DOI locator attempts are recorded, but identity validation remains incomplete where access was blocked or only HEAD was used. Full text should later be inspected for form and writing-model fit when actual library retrieval is authorized.
