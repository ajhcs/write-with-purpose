# Prior work and data reuse

Start with [what existing systems and data change](reuse-plan.md), then [the detailed research synthesis](report.md), [the independent audit](audit/report.md), [the source-record bibliography](merged-records.json), and [the research retrieval list](paywalled-research.md) ([CSV](paywalled-research.csv)). Eight Terra scouts supplied 67 observations consolidated into 66 DOI-deduplicated records; a ninth Terra agent audited them. The parent added [two verified writing-feedback systems](supplemental-systems.json), separately counted. Scout evidence and detailed provenance remain under [agents](agents/). The [research contract](research-contract.md) defines scope, accepted foundations and rights boundaries.

[Local Webis proof](audit/reusable-data-proof.json) contains counts and archive hash without text; it demonstrates parseable files, not validated function distributions. No corpus or linked source license is automatically granted by the presence of these records. Dataset releases and overlapping source texts are not independent samples.

The raw archive is retained outside the checkout at the path in [its receipt](audit/archive-location.json). Run `python3 experiments/prior-work-reuse-2026-11-16/audit/integrate.py` from the repository root to rebuild the merged scout records and count receipts. It does not overwrite authored reports, access lists or supplemental system records. Source checks and access metadata are recorded under `audit/`.

Local metadata checkpoint: `/workspace/build/builderbob/write-with-purpose/checkpoints/prior-work-reuse-20261116T185721Z`. Includes this experiment and the updated work index; raw source corpora are excluded. This is a local recovery snapshot, not an offsite backup.
