# Writing, editing and improvement rule debate

16 November 2026. The author's [accepted direction](accepted-direction.md) adds editing and affirmative improvement to the harness and asks for a debate with an adjudicator prioritizing useful novelty. The [contract](debate-contract.md) defines the scope and the comparison baseline.

Five Terra advocates represented voice/originality, reader understanding/learning, form/paragraph functions, editing/improvement, and computable checks/evaluation. Each first submitted an independent position. They then challenged specific peer proposals and replied with revised wording. Astra adjudicates the resulting disagreements against the actual current skills and research, including its own earlier advice.

## Debate record

| Stage | Saved material | Scope |
| --- | --- | --- |
| Comparison baseline | [Snapshot](baseline-snapshot.json) | Seven original skill, foundation, evidence and calibration hashes |
| Independent positions | [Round 1 receipt](round1-receipt.json); `positions/` | Five advocates, 22 proposals |
| Peer challenges | [Round 2 receipt](round2-receipt.json); `challenges/` | 17 specific challenges |
| Replies | [Round 3 receipt](round3-receipt.json); `replies/` | All 17 challenges answered; original rounds retained |
| Adjudication criteria | [Charter](adjudication/charter.md) | Fidelity and author constraints determine eligibility; useful novelty then takes priority |
| Final dispositions | [Decisions](adjudication/decisions.md) and [structured record](adjudication/decisions.json) | All 22 proposals and 17 challenges receive traceable dispositions |
| Novelty and disagreement | [Novelty ledger](adjudication/novelty-ledger.md) | Distinguishes inherited practice, incremental changes and proposed mechanisms; retains minority alternatives |

The nine features, Family → Form → Section hierarchy, and distinction between observed ranges, working targets and declared limits remain foundations. Canonical skills and historical paragraph labels are comparison inputs; this experiment does not silently revise or install them.

## Operative candidate

Start with [the four core rules](candidate/operative-rules.md). Inherited foundations, final checks and optional teaching remain explicit, but are not counted as four additional innovations.

| Rule | What the harness does |
| --- | --- |
| R01: depth and whole-work review | Infers whether the task is correction, improvement or new writing. An improvement request triggers a search for a worthwhile better thought, structure or expression, even if the original is adequate. It carries a selected improvement into prose. |
| R02: develop the thought | Distinguishes the author's stated position, a grounded connection and a proposed new interpretation. For requested deeper thinking, tests a consequential claim against a relevant alternative or boundary. |
| R03: actual alternatives | When a material choice warrants comparison, writes the decisive passage and judges gains and losses. A substantive restructuring must change more than heading names. Keeping the original is allowed. |
| R04: objective determines investigation | Ordinary editing need not force a label when rival readings allow the same sound edit. Annotation and definition research still investigate their relevant disagreements, even if no edit follows. |

[Coding clarifications](candidate/coding-clarifications.md) retain all twelve function IDs and supply presence tests, boundaries, attribution, relation targets and separate anchor/realization records. Presence does not imply truth, quality or a need to revise. Applying this guidance requires a new versioned coding pass; historical labels stay intact.

### Running this manually in Codex

Point Codex to the operative guide, supply the draft or notes and source material, and state the actual task. For example:

> Read `experiments/rule-debate-2026-11-16/candidate/operative-rules.md`. Improve this decision memo's reasoning and organization, while preserving its supplied facts and uncertainty. Deliver the revised memo. Explain only the consequential changes and unresolved premises.

For coding, add the coding appendix and the declared annotation objective. For mechanical checks, use the existing checker only with actual supplied constraints. An explicit maximum or protected phrase can be enforced; a general readability preference cannot be turned into a hidden hard limit.

This is a manually loadable candidate, not an installed plugin, automatic form classifier or implemented repair loop. The narrower next engineering step is to connect task scope, form planning, actual edits and existing checks after the candidate survives further review.

## Development review

[Eight synthetic cases](development-cases.md) cover correction only, decision reasoning, personal expression, novice explanation, idea development, source-faithful Methods editing, standalone annotation research, and an explanation under a declared word limit. They include fixed facts, explicit task scope and selected mechanical constraints.

An exerciser receives the operative candidate and cases before reading adjudication reasoning. A separate auditor registers a rubric against the baseline before reviewing the candidate and its outputs. These are development checks, not a blinded comparison of old/new performance, expert gold labels, reader testing or proof that the candidate is optimized. The adjudicator has access to these cases, so they are not held out.

Code can check declared literal/word constraints and artifact consistency. Semantic fidelity, meaningful improvement, artistic effects and author approval remain separate judgments. A successful file check cannot certify those qualities.

### What happened in these examples

- E01 corrected only `record` → `records` and stayed at 26 whitespace-separated words.
- E02 developed the staffing decision from arrivals/closures and withdrew a headcount that the supplied facts did not establish.
- E03 kept the personal passage after considering a concrete alternative that did not clearly improve its rhythm.
- E04 explained the needed conceptual distinction while retaining `idempotent`.
- E05 developed the author's storage-versus-inquiry distinction without inventing motives or evidence.
- E06 retained the completed Methods action while removing an unsupported accuracy claim and reader directive.
- E07 performed standalone coding research, keeping opposed claims, hypothetical reasoning and overlapping functions visible; six exact anchors remain anchors, with realization extents not collected.
- E08 joined a material condition to the result and retained all supplied limits in 34 words, below the declared maximum of 45.

Read the actual outputs in [the exercise](validation/development-exercise.md). The existing checker ran on seven pure prose artifacts: [all five nonempty declared contracts passed](validation/mechanical-checks/summary.json); E02 and E05 had no such contract. Its E02 number-change observation is [explained against the supplied source notes](validation/parent-review.json), rather than being treated as a factual error or suppressed.

The independent review found two issues that were corrected: a worked example's count was 26, not 27; and an inherited teaching instruction could impose practice before a requested worked answer. The latter became [revision 0.1.1](adjudication/revision-0.1.1.json). The original eight cases used [frozen version 0.1 inputs](validation/execution-input-receipt.json). R01–R04 did not change in the correction. [Two additional learning-scope examples](validation/learning-scope-exercise.md) exercise the corrected behavior: deliver a requested solution directly, or wait for an expressly chosen practice attempt. Neither establishes learning efficacy.

The [independent audit](validation/independent-audit.md) separates these development observations from unmeasured reader gains. The current skills already permit substantial rewrites and could produce these same results. The candidate's proposed increment is more explicit selection behavior and usable coding distinctions; superiority has not been demonstrated. [Migration guidance](candidate/migration.md) preserves the old records and identifies what still needs implementation and validation.

The parent's [final consistency receipt](validation/packet-validation.json) verifies proposal/challenge coverage, unchanged baseline and frozen-round hashes, current guide/JSON correspondence, retained IDs, declared contracts and published local links. Its scope is mechanical artifact consistency, not semantic validation.

## Local recovery checkpoint

This debate packet and the updated work index are saved in `/workspace/build/builderbob/write-with-purpose/checkpoints/rule-debate-20261116T204221Z/`. The adjacent `manifest.json` records file and archive hashes, Git state and archive readback. It is a scoped local snapshot; raw article/corpus bytes remain in their existing `/workspace` caches and prior work has its earlier checkpoints. No staging, commit, installation or publication is performed by this checkpoint.
