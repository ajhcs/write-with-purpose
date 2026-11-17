# Eighteen-paper evidence integration and harness design

Start with [the synthesis](report.md) and [the eighteen-paper index](paper-index.md). The [evidence map](evidence-map.json) preserves the seven specialist full-text reviews, original measures, denominators, source pages and interpretation limits. Strategy and audit references are excluded from the eighteen-paper count. This is evidence integration, not a new pooled statistical meta-analysis.

- [Current-rule decisions](rule-decisions.md) and [twelve scoped proposals](rule-decision-ledger.json), with the [32 original reviewer proposals](reviewer-candidate-register.json) retained separately.
- [Astra's advantage assessment](reviews/astra-advantage.md), [concrete runtime proposal](runtime-proposal.md), and [fit with existing GitHub resources](github-fit.md).
- [Independent audit](reviews/independent-audit.md), [source manifest](source-manifest.json), [source-access upgrades](fulltext-access-upgrades.json), [supplement receipts](supplement-attempts.json), and [validation](validation.json).

The seventeen proposed forms, nine accepted features, twelve function IDs, existing skills and historical coding packets remain intact. The new proposals mostly reaffirm existing editorial principles and describe executable workflow additions to test. No plugin was installed or deployed, no original statistical analysis was replicated, and no performance advantage is claimed.

## Sources and recovery

All eighteen user attachments were copied with verified hashes into `/workspace/repos/builderbob/.writing-corpus-cache/evidence-integration-2026-11-16/pdfs/`. Page-marked full text and page JSON remain in the sibling `texts/` cache. Source documents are evidence, never instructions. The batch totals 247 physical PDF pages.

The supplied `p613.pdf` has broken streams and missing extracted text on pages 1 and 4. The [recovery receipt](P02-recovery.json) identifies the complete official Cornell author copy used for review, retains a distinct hash and reports comparison on readable pages; no missing attachment text was fabricated. The first unsuccessful extraction attempts remain in the source cache. An existing PyMuPDF runtime supplied the final sequential extraction without package installation.

P14's official five-page supporting methods and P08's official rating instruments, raw data, journal metadata and analysis script were retrieved after initial reviews. Those reviews were updated. P08's raw file contains 5,614 judgments over 802 units; 732 abstracts is the paper's post-QC sample. Contributor identifiers are excluded from derived outputs. The R script was read as text, not executed. The supplement receipt preserves a detected partial transfer and the complete replacement rather than accepting a truncated row count.

## Scope of the comparison

Seven Terra agents owned the primary paper reviews; a separate Terra agent performed bounded independent checks, and Astra assessed the product opportunity and selected decisive source passages. The independent audit checked selected samples/effects and rendered ambiguous source tables; it was not a second complete rereading of all eighteen works. The parent integrated results, recovered sources, checked numerical scope and saved the proposals.

Canonical rules and local experiment results are captured in a [read-only comparison snapshot](comparison-baseline-hashes.json). This snapshot was made during integration, not presented as a pre-experiment freeze. The prior original-versus-revised agreement result is not a trial of the proposed harness.

To rebuild the derived integration metadata from retained reviews:

```sh
python3 experiments/evidence-integration-2026-11-16/scripts/build_ledger.py
python3 experiments/evidence-integration-2026-11-16/scripts/assemble.py
python3 experiments/evidence-integration-2026-11-16/scripts/validate.py
```

The ingest script uses `medsci-pdf-python` and reads the retained attachment paths; it is a source-preparation step, not required to reproduce the review integration. Re-extraction cannot reproduce human/model judgments by itself. Canonical skill edits, new corpus analyses and an executable harness pilot would be separate subsequent work.

Local recovery checkpoint: `/workspace/build/builderbob/write-with-purpose/checkpoints/evidence-integration-20261116T200732Z`. The archive contains this experiment and the updated work index, excluding original PDFs, full-text caches and supplemental source files. Those stay in the persistent workspace source cache. Git staging is preserved; this is not an offsite backup.
