# Business, engineering, law and personal writing

The author requested broader coverage after the first scholarly sample became dominated by medicine. Four GPT-6.1 Terra branches prepared the historical discovery collections below. These are **bibliographic/library leads**, not newly measured full texts or verified examples of all seventeen forms.

The subsequent authorized [available-copy retrieval pass](../fulltext-retrieval/summary.md) now links locally saved files and separates candidate articles from landing pages, failures and unresolved review. The discovery counts below remain discovery counts.

The [combined discovery CSV](nonmedical-discovery.csv) provides one browsing view while retaining each original source manifest and its classification limits. It does not establish one cross-field citation ranking. Law-specific flagged conflicts remain visible and can be filtered using `held_by_source_screen`; an unheld record is still unverified. Missing citation counts remain empty for editorial selections.

| Source group | Actual records | Source coverage | Historical and classification limits |
| --- | ---: | --- | --- |
| [Business](business/summary.md) | 1,200 | 200 each from AMR, AMJ, Strategic Management Journal, Organization Science, Management Science and HBR | OpenAlex dates through 2014; forms unverified. HBR is a separate practitioner source. 200 AMR records overlap the earlier queue |
| [Engineering](engineering/summary.md) | 350 | Seven journals spanning mechanical/thermal, civil, electrical, software and systems engineering | Indexed 2000–2014; dates/citations need source verification. This is research-journal discovery, not practitioner documentation |
| [Law](law/README.md) | 390 | Six law reviews | Indexed through 2014. 44 known/suspected book or book-review conflations are held; remaining 346 are unscreened leads |
| [Personal/public essays](personal/summary.md) | 316 | 305 Longform-linked items plus 11 historical Notables seeds | Displayed pre-2015 dates. Personal/argument/criticism/reporting distinction remains unresolved; some original links still need locating |

The main CSV has **2,256 source records**. This is not 2,256 validated or necessarily unique original works. Reconciliation with earlier queues and bibliographic verification remain necessary. The personal Longform subset spans 252 normalized author strings and 119 outlet labels, with at most six works per author; a normalized author string is not a verified independent author identity.

## A stronger legal ranking source

The separate [HeinOnline top-100 snapshot](law/heinonline-top100.csv) preserves the provider's actual ranks and citation/access columns, rather than assigning OpenAlex counts to HeinOnline. Three entries are held for scope/genre issues, leaving 97 provisional candidates in [heinonline-candidates.csv](law/heinonline-candidates.csv). Some works overlap other discovery pools; these rows are not added to the 2,256-record total.

The source is [HeinOnline's public most-cited-article table](https://access.heinonline.com/HOL/scholarly-impact-ranking/comprehensive-articles). The branch's direct HTTP request returned 403; the snapshot was transcribed from the web tool's rendered source. No raw HTML or source-byte hash is available for that table. The branch verifies rank sequence and the arithmetic of the displayed citation columns; this is not independent validation of provider counts or underlying article identities. The table's access column uses its stated window and is not global readership.

[Shapiro and Pearse's 2012 study](https://repository.law.umich.edu/mlr/vol110/iss8/2/) is an additional historical ranking reference. Its all-time and recent-period tables overlap; they have not been represented as 200 independent original works. Legal source guidance also identifies briefs, opinions and executive/legal memoranda as distinct writing tasks rather than assuming that all legal work is a research article.

## Use alongside form, audience and era

The [cross-domain sampling note](../../../docs/writing-harness/research/cross-domain-sampling.md) explains the design. Compare forms within their context and intended audience before combining anything across domains. A clinical case report, organizational case study and judicial case opinion have different evidential and structural purposes. The new domain groups do not automatically replace or expand the five proposed writing families.

Prioritize pre-2015 originals, keeping 2015–2019 as a separate supplement where needed. Metadata/display dates and first-online versus issue dates must be checked. Medical-source availability, citation counts and current software documentation should not determine general-purpose defaults.

## Reproduction and parent checks

`python3 experiments/form-corpus-2026-11-16/domain-expansion/merge_discovery.py` rebuilds the combined CSV from the four saved JSONL manifests without network requests. It preserves holds, missing identifiers and source-group attribution and writes [merge-receipt.json](merge-receipt.json) with input hashes and counts. Original branch collectors can make live requests that change the source snapshots; use their documented receipts and limits.

Parent checks reconcile row counts and source hashes, inspect sample bibliographic records and the legal provider table, and verify that legal held rows are excluded from the law branch's retrieval subsets. These checks do not establish individual form, text completeness, historical version, access entitlement, quality or representative sampling. No source full texts were acquired or measured by this domain expansion.
