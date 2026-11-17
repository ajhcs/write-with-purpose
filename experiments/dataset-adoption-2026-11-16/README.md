# Dataset acquisition and paragraph-function comparison

Start with [the comparison of all twelve functions](comparison.md). The [159-entry CSV](crosswalk.csv) and [JSON](crosswalk.json) retain original source labels, serialization, unit, evidence, possible functions, conditions, counterexamples and code-check limits. These mappings are proposals for our own plugin, not adopted relabelings.

- [Downloaded source inventory](dataset-inventory.md), [acquisition receipts](acquisition-index.json), [codebooks and guides](codebook-index.md), and [remaining access/format gaps](remaining-access.md).
- [Actual original-unit profiles](source-profiles.json), [scientific label inventories](reviews/scientific-observed-labels.json), [unreviewed source labels](source-label-gaps.json), and [PERSUADE offset diagnostics](persuade-offset-diagnostics.json).
- [All seventeen forms and their remaining gaps](form-gaps.md), [how to reuse this inside our plugin](plugin-reuse-notes.md), [independent audit](reviews/independent-audit.md), and [mechanical validation receipt](validation.json).

Original files remain outside the Git checkout under `/workspace/repos/builderbob/.writing-corpus-cache/dataset-adoption-2026-11-16/`; the reused Webis archive also remains in the prior-work cache. Each acquisition records its source URL, commit where applicable, byte count, hash and outcome. No upstream training code or serialized Python objects were executed. Source rights, annotation rights and code rights remain separate. The bibliography's datasets overlap and must not be treated as independent populations.

The previous [prior-work map](../prior-work-reuse-2026-11-16/README.md) discovered and appraised resources. This experiment acquires accessible files and tests their units and schemas. Five existing Terra agents supplied four specialist reviews and an independent audit; the parent added documentation and PERSUADE comparisons, downloads, parsers and integration. The accepted catalogue and historical coding results are preserved.

## Reproduce the derived metadata

Run from the repository root with Python 3:

```sh
python3 experiments/dataset-adoption-2026-11-16/scripts/profile_sources.py
python3 experiments/dataset-adoption-2026-11-16/scripts/technical_crosswalk.py
python3 experiments/dataset-adoption-2026-11-16/scripts/persuade_crosswalk.py
python3 experiments/dataset-adoption-2026-11-16/scripts/merge_crosswalks.py
python3 experiments/dataset-adoption-2026-11-16/scripts/finalize.py
```

The acquisition scripts are separate because rerunning them performs network transfers. `acquisition.json` retains initial failures; `followup-acquisition.json` records subsequent successful public releases and guides. `identity-corrections.json` preserves an incorrect paper link and the correct replacement rather than silently counting both as codebooks. `persuade-extraction.json` records ordinary extraction of the public test archive using the creator-published password. The unopened SciPara pickle remains a format gap.

Validation checks hashes, label vocabularies, counting units and metadata consistency. It does not establish semantic equivalence, writing quality, form completeness or usable observed length targets. The next step is a small compatibility pilot using existing annotations and independent function judgments, with the author retaining decisions about structure, voice and wording.

Local metadata checkpoint: `/workspace/build/builderbob/write-with-purpose/checkpoints/dataset-adoption-20261116T193140Z`. Raw corpora and codebooks remain in the persistent source cache; the checkpoint includes only this experiment, scripts and the work index. It preserves staging and is a local recovery snapshot.
