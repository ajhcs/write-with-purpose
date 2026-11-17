# Essay corpus: discovery and first measurements

16 November 2026. This is an exploratory acquisition and extraction run, not an accepted form profile. The two provisional forms can overlap. None of the numeric observations is a writing target or a limit. The 200-per-form goal is **not met**: four individual texts were screened by one reviewer, two per form.

| Collection | Discovery / selected | Acquired and mechanically extracted | Form eligibility |
| --- | --- | --- | --- |
| Longform essay-tag archive | 467 distinct target URLs, editorially selected; full tag through page 19 | 25 publisher-domain probes; 6 returned at least 100 extracted article words, body completeness unverified | No full-text eligibility decisions |
| Paul Graham original essay archive | 234 distinct index links; first 225 selected in index order | 221 with at least 100 extracted words; 4 yielded too little | Four one-reviewer provisional inclusions; multiple forms possible |
| Europe PMC personal narrative indexing | 303 search hits; 300 selected | 297 bodies extracted | Not manually screened; publication-type labels contain clear mismatches |
| Europe PMC editorial indexing | 150,880 search hits; 300 selected | 293 bodies extracted | Not manually screened; publication-type labels contain clear mismatches |

The selected collections overlap in possible form and may overlap in work identity; do not add their counts to claim a deduplicated form corpus. The archive is one author and cannot estimate a general personal-essay or argument distribution. The biomedical sample is a separate disciplinary cohort. Its citation sort is a retrieval-specific metric, not literary importance or readership.

## Historical strata

Year for the author archive is the first year in its original date label; labels sometimes include revisions. Longform dates are displayed index metadata and should be checked against original publication. Europe PMC uses its indexed `pubYear`. Unknown stays separate.

| Collection | Pre-2015 | 2015–19 | 2020 onward | Unknown |
| --- | ---: | ---: | ---: | ---: |
| Longform candidates | 305 | 112 | 48 | 2 |
| Paul Graham extracted | 148 | 23 | 48 | 2 |
| Europe PMC extracted | 109 | 167 | 314 | 0 |

The [historical discovery note](historical-discovery.md) links an independent editorial list, a publisher award/finalist register and specific library leads. Accolades and editorial inclusion are recorded distinctly; neither is a readership ranking.

## Observations within the single-author archive

The table describes only extracted pages from this author’s index, with no classification by form. The word unit and extraction rules below matter when comparing strata. Each paragraph figure is the median of the individual documents’ median paragraph lengths, avoiding simple weighting toward long documents.

| Date stratum | Documents | Body words: min / median / max | Median of document paragraph medians |
| --- | ---: | ---: | ---: |
| pre-2015 | 148 | 146 / 1538.0 / 10800 | 56.0 |
| 2015–19 | 23 | 119 / 631 / 5180 | 59.5 |
| 2020 onward | 48 | 145 / 1157.5 / 12527 | 60.25 |
| unknown | 2 | 216 / 351.5 / 487 | 25.5 |

These differences are descriptive only. Index-order selection, changes in topic and genre, parser errors, and this single author all confound temporal comparisons. Four checked examples are below; one-reviewer form judgment is provisional, and no claim facts were verified.

| Example | Year | Provisional form | Extracted body words | Paragraphs |
| --- | ---: | --- | ---: | ---: |
| [Having Kids](https://paulgraham.com/kids.html) | 2019 | personal / reflective | 1485 | 25 |
| [Life is Short](https://paulgraham.com/vb.html) | 2016 | personal / reflective | 1565 | 25 |
| [Founder Mode](https://paulgraham.com/foundermode.html) | 2024 | argument / perspective | 1054 | 14 |
| [The Real Reason to End the Death Penalty](https://paulgraham.com/real.html) | 2021 | argument / perspective | 746 | 12 |

## Method, provenance, limits

- `longform_dated_candidates.jsonl` and `longform_dated_pages.jsonl` retain displayed metadata, links, search pages, hashes and retrieval times. `longform_public_probes.jsonl` records retrieval refusals, redirects, paywall declarations and provisional extraction outcomes. No paywall was bypassed; a returned article body has not been checked for completeness.
- One page per publisher domain was probed after checking robots; non-200 robots and non-200 article responses were skipped. A manual preliminary Guernica page request and the subsequent automated probe occurred within Guernica’s 600-second crawl delay. That was an access-rate error; no further Guernica requests were made.
- `public_archive_candidates.jsonl` and `public_archive_measurements.jsonl` record author-index links and page hashes. Body paragraphs are estimated from the longest Verdana block and double line breaks; leading promotions/date and notes are excluded when identified. The 100-word cutoff is an extraction triage rule, not an eligibility or quality rule. Four pages did not yield sufficient text under this parser. Body completeness, headings, citation function, and footnote boundaries need review.
- `candidates.jsonl`, `discovery.json`, and `measurements.jsonl` preserve the Europe PMC queries, citation order, source identifiers, year, article types, XML hashes, retrieved times, extraction states and mechanical counts. The extracted JATS body excludes lists, figures, tables, formulas, boxes, captions, acknowledgments and references. Citation or quote counts do not establish supporting function. Sections without headings and repeated headings are not resolved reliably.
- The character/word and sentence/paragraph distributions are mechanical approximations; word tokenization and punctuation-based sentence splitting are defined in `acquire_measure.py`. HTML and JATS parser failures, figures, headings, notes and embedded content can distort results. No rhetorical functions were assigned by code; the [four human screening notes](manual-screen.jsonl) are not independent agreement.
- Source HTML/XML is retained only in the local `/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16/` cache; these repository files contain metadata and derived statistics, not article prose. No publication, deployment, or source-content redistribution is implied.

Longform probe outcomes: `{'robots_unavailable_skipped': 5, 'extracted_unvalidated': 6, 'no_article_body': 5, 'http_non_200_skipped': 6, 'declared_paywalled_skipped': 2, 'failed': 1}`. Europe PMC outcomes: `{('personal_reflective', 'measured'): 297, ('personal_reflective', 'failed'): 3, ('argument_perspective', 'measured'): 293, ('argument_perspective', 'no_body'): 1, ('argument_perspective', 'no_prose'): 3, ('argument_perspective', 'failed'): 3}`.

To reproduce the analysis, use the three acquisition scripts only when access terms and crawl delays permit; then run `python3 experiments/form-corpus-2026-11-16/essays/summarize.py`. Acquisition can change as pages, access and rankings change. For a stronger form study, screen individual texts and source editions, broaden authors/outlets and historic works, compare independent reviewers, and extract accessible library texts without bypassing access controls.
