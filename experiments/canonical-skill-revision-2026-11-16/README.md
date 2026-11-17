# Canonical skill revision

Start with [the implementation and test report](report.md).

- [Protocol and scope](protocol.md)
- [Astra's implementation map](implementation/implementation-map.md)
- [Independent source audit](review/source-audit.md)
- [Masked initial comparison](review/masked-comparison.md) and [decoded results](results/comparison-summary.json)
- [Final focused observations](review/focused-parent-review.json)
- [Baseline manifest](baseline-manifest.json) and [final reviewed snapshot manifest](reviewed-snapshot-manifest.json)

`baseline/`, `revised-snapshot/`, `final-snapshot/` and `reviewed-snapshot/` preserve the source stages actually exercised. Initial matched outputs and both focused attempts remain in `runs/`; review fixes record the intervening changes. Global installed skills are separate from this repository revision.

The [final consistency receipt](results/final-validation.json) verifies the captured checks, source/snapshot correspondence, preserved historical records and staging, installed entrypoint hashes and file links. It does not certify writing quality.

Local recovery checkpoint: `/workspace/build/builderbob/write-with-purpose/checkpoints/canonical-skills-20261116T214225Z/`. Its manifest records selected source and artifact hashes, Git receipts and archive readback. The snapshot includes this experiment, canonical skill folders, unchanged Python tests, package metadata and updated documents. Raw corpora/PDFs and unrelated working files remain in their existing locations; this is a scoped local checkpoint, not a complete repository or offsite backup.
