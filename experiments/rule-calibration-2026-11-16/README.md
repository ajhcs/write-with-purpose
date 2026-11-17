# Original versus Astra: fresh-paragraph calibration

Completed 16 November 2026. [Read the results and proposed next changes](report.md).

Thirty-six fresh paragraphs from twelve documents; two independent GPT-6.1 Terra coders per arm per stage; eight coder instances, 144 individual paragraph codings. Both guides and two source samples were frozen before coding; no rule tuning between stages. All selected submissions pass bounded structural checks; an independent audit reproduces the primary counts.

Clear exact-set agreement: original **21/36**, revised **18/36**. Including unresolved possibilities: **19/36** versus **18/36**. No demonstrated agreement improvement; no human accuracy claim. The richer records expose inspectable targets and attribution, but require about three times the annotation text. Evidence-anchor lengths are not complete function-length ranges.

- `protocol/`: frozen plan, guide copies, hashes and allocation metadata.
- `sampling/`: twelve-source manifest, exclusions and preparation code; full bodies remain private in the persistent `/workspace` cache.
- `coding/`: unchanged raw submissions, retained context correction and mechanically normalized copies.
- `analysis/`: bounded contract checker, seven focused tests, packet builder and matched analysis.
- `results/`: full comparison and masked-review identity key; no gold labels.
- `review/`: separate masked AI semantic diagnostic of twenty prespecified targets.
- `audit/`: independent recomputation, source checks and documented limitations.

This experiment changes no installed skill, original catalogue or frozen candidate. Its proposed clarifications require another frozen test on additional untouched documents before scaling. The current sample is now exposed development material.
