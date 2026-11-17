# Available-copy retrieval results

The authorized public-source pass accounts for **2,360 source entries**: 1,200 business, 350 engineering, 494 legal entries (including ranked-list records and four official examples), and 316 personal/public-writing entries. This denominator includes held and linked-duplicate records, not 2,360 independent works or article downloads. The source queues and historical preferences are preserved.

## Files obtained

| Discovery group | Saved primary candidate copies | Evidence and unresolved work |
| --- | ---: | --- |
| [Business](business/report.md) | 36 PDFs | Seven have matching first-page title/identifier evidence; 28 identity-unresolved, one without usable text. The seven are indexed as submitted versions, not verified historical publisher editions. |
| [Engineering](engineering/report.md) | 13 PDFs | One has matching bounded first-page title/DOI evidence; twelve need identity review. |
| [Law](law/summary.md) | 10 PDFs and one HTML file | Identity remains unresolved under the DOI/front-matter checks. Spot checks found matching titles/authors in two substantive law-review files, but did not establish published version or completeness. |
| [Personal/public writing](personal/summary.md) | 129 possible article bodies | Includes HTML and one PDF. Seventy-four have heuristic or manual title/author agreement; complete-body and original-edition status remain unverified. Forty-three need additional access-policy review. |

These are **189 candidate-file records**, not 189 verified complete works. An additional 31 personal HTML captures are retained as noncandidate/incorrect/landing/preview material, explicitly excluded from the 129. Across all four branches the selected paths comprise 220 retained file records and 213 distinct byte hashes; identical bytes do not necessarily imply identical bibliographic work, and multiple versions may represent one work.

The [clickable downloaded-file index](downloaded-files.md) links the 189 candidate copies. The [candidate-file CSV](candidate-article-files.csv) has paths, title/identifier fields, hashes, identity status, version metadata and source-manifest pointers. The [all-outcome CSV](retrieval-status.csv) retains every source entry, including failures, deferrals, holds and duplicates. The [saved-files CSV](saved-files.csv) includes the 31 noncandidate personal captures so they are not silently mistaken for successful articles.

Source files are stored locally outside Git under [/workspace/repos/builderbob/.writing-corpus-cache/fulltext/](/workspace/repos/builderbob/.writing-corpus-cache/fulltext/). Metadata, scripts and reports are in the repository. No source full texts were published or uploaded elsewhere.

## Remaining access and review

The [follow-up CSV](follow-up.csv) retains unresolved access, identity, version and completeness work. Some records with files need review rather than another download. The [library-missing RIS file](library-missing.ris) contains 2,082 deduplicated-by-DOI-or-title retrieval candidates without a retained candidate body, excluding held and explicitly linked-duplicate records. This is a citation-import aid, not a request to retrieve every entry blindly or an approved set of form exemplars. Generic RIS types reflect unresolved forms.

A publisher 403, asynchronous 202, rate response, robots restriction or dead URL is recorded as that outcome, not proof that a work is unavailable through the author's libraries or every other legitimate source. The scripts inspected public metadata, advertised open locations, permitted publisher/repository pages and source-specific full-text links. This was a bounded retrieval pass, not an exhaustive search of all possible copies. No authenticated institutional or Zotero session was established. Bounded connected-Drive searches did not establish exact article matches; unrelated files were not downloaded.

## Source and file checks

The parent rebuilt the indexes from the four final manifests and independently checked all 220 selected file paths and SHA-256 digests. They remain on the verified Samsung workspace. `index-validation.json` records counts and scope. Alternate PDF versions are retained in branch caches/manifests where applicable; the main index selects each record's primary file rather than counting every variant as another work.

Existing Poppler tools extracted text layers from 60 primary PDFs: 59 nonempty outputs and one empty layer. Local sidecar paths and hashes are in [pdf-text-layers.json](pdf-text-layers.json). Text-layer extraction does not establish a complete, correctly ordered or cleaned article and performs no OCR. Sidecars remain outside Git in the source cache.

An independent [four-file spot audit](engineering/cross-branch-file-audit.md) found expected titles/authors and substantive text in two personal HTML files and two law-review PDFs. It also found recommendations, newsletter material and other non-body text in HTML captures. Those findings limit automatic prose measurement; they are not a collection-wide estimate of completeness or correctness.

## Retrieval errors and remediation

Initial scholarly crawlers did not fully implement legitimate robots redirects or longer advertised pacing intervals; the personal crawler automatically followed some robots redirects before applying its intended per-host delay. Those defects were detected and corrected for resumed work. Earlier requests cannot be undone. Branch reports preserve the affected traces and do not claim the initial passes fully honored the intended pacing contract. The business branch also discloses early automatic redirect handling during its follow-up.

The personal branch rechecked captured robots metadata without retrieving the article bodies again. Of 129 candidate bodies, 86 had unchanged robots bytes and no detected `ai-input=no` signal; 43 remain flagged for policy review. This neither undoes earlier pacing errors nor establishes all reuse rights. No policy-flagged capture should be silently treated as analysis-ready. Rate-limited and challenged hosts remained deferred rather than bypassed. The final indexes preserve policy details as well as bibliographic uncertainty.

## Reproduction

`medsci-python experiments/form-corpus-2026-11-16/fulltext-retrieval/build_index.py` rebuilds the indexes and verifies retained hashes without network access. Add `--extract-pdf-text` to regenerate local text-layer sidecars with the installed Poppler runtime. Read branch reports before rerunning acquisition; live services, versions and policies change, while saved metadata and hashes preserve this pass's evidence.

Retrieval has not established paragraph functions, numerical writing profiles, source truth, author voice or reader usefulness. Review file identity/completeness and harmonize extraction before computing further form comparisons.
