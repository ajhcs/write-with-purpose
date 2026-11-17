# Canonical skill revision and test rerun

16 November 2026. Astra implemented the adjudicated rules in the repository's two canonical skills: writer **0.4.0-alpha.6** and editor **0.3.0-alpha.6**, packaged as **0.6.0-alpha.6**. The source now supports correction, polish, substantive improvement and new drafting at the requested depth. No global installation, release or commit was performed.

## What changed

R01–R04 are operative guidance in both entrypoints. An improvement request searches for a better thought, structure or expression even if the original is adequate; a correction-only request stays narrow. Reasoning development distinguishes the author's position, a grounded connective and a proposed interpretation. Consequential alternatives become actual prose. Annotation research retains its disagreements even when no edit follows.

Each skill has its own synchronized structure/development and function/ambiguity references, so neither requires the other to supply those instructions. The twelve function IDs remain provisional analytical tools. Family → Form → Section, the nine feature groups, and the distinctions between observed ranges, working targets and declared limits remain visible during relevant work.

The existing scripts already implement the supported mechanical contracts. Their code and tests are unchanged. Instructions now clarify final body scope, stale receipts, unsupported contract keys, advisory findings and separate semantic review. The editor can use an ordinary counter when the writer helper is unavailable. No semantic linter, grammar dependency, automatic hook or calibrated form-length profile was added.

See [Astra's implementation map](implementation/implementation-map.md) and [the independent source audit](review/source-audit.md). Approved style/article copies remain identical and unchanged.

## Captured software and artifact checks

| Check | Result | Evidence |
| --- | --- | --- |
| Frozen baseline Python suite | 47 passed | [Receipt](runs/baseline-unit.json) |
| Final canonical Python suite | 47 passed | [Receipt](runs/revised-unit.json) |
| Annotation-prototype suite | 15 passed | [Receipt](runs/annotation-unit.json) |
| Skill-creator validation | Both skills passed | [Receipt](runs/skill-validation.json) |
| Declared contracts on initial matched outputs | Seven per arm passed | [Reports](results/mechanical-checks/summary.json) |
| Final focused body contracts | Two passed | Same reports; actual body files checked |

These tests establish their implemented software and contract behavior. They do not establish source truth, rhetorical quality or author acceptance. The annotation suite is distinct from re-running the earlier 36-paragraph coder-agreement experiment; its reported findings remain unchanged.

## Matched writing exercise

Four fresh Terra contexts applied old or revised skill snapshots to the same twelve raw tasks, six tasks per context. Ten tasks were known synthetic development examples; two were new parent-authored drafting tasks. A fifth fresh context reviewed masked pairs without skill instructions, arm identities or prior verdicts. The [protocol](protocol.md), [frozen inputs](inputs/cases.json), [masked review](review/masked-comparison.md) and [decoded results](results/comparison-summary.json) preserve the comparison.

The reviewer preferred the revised output in **two** cases, the baseline in **one**, and judged **nine** ties. E04's revised explanation repeated less; E07's revised analysis clarified relation scope and provisional readings. E06's baseline separated manuscript text and its issue note more clearly. These are particular model judgments, not a reliable quality improvement estimate.

Both initial arms failed the attempt-first practice task by supplying an already-composed answer as a source fact. The first focused retest repeated that failure after a sequencing clarification. All outputs remain saved. The source was refined to leave the selected writing move to the learner, and to distinguish publishable prose from editorial notes. Exact changes and hashes are in [fix 01](implementation/review-fix-01.md), [fix 02](implementation/review-fix-02.md) and [fix 03](implementation/review-fix-03.md).

## Focused final retest

A new fresh context received four raw tasks and the final reviewed skills, without prior outputs or expected answers. Parent inspection found:

- **E06:** a [pure Methods body](runs/reviewed-focused/E06/body.txt) and a [separate source note](runs/reviewed-focused/E06/notes.txt). A combined transcript is also retained; the body file defines the manuscript scope.
- **L01:** the [requested worked solution](runs/reviewed-focused/L01/output.txt) was supplied directly.
- **L02:** [raw counts and an invitation to attempt](runs/reviewed-focused/L02/output.txt) left the sentence unwritten.
- **S01:** the [standalone editor result](runs/reviewed-focused/S01/body.txt) retained the technical conditions in 36 words. The executor received only the editor installation for this task and used a standard-library counter; the writer is not a dependency.

[Parent observations and hashes](review/focused-parent-review.json) record the scope. These examples support the narrow corrections, not demonstrated learning transfer or general reliability.

## Interpretation and limits

The canonical implementation is complete and the captured checks pass. The initial paired results were mostly ties and identified real defects; the final four cases are development retests after those defects were known, not a new masked comparison of the finished skills. No superiority claim follows.

Read boundaries were instructions on a shared filesystem. One revised executor disclosed reading other raw task inputs from the shared twelve-task file, although it reported no access to other outputs, verdicts or skills. This weakens strict context equivalence. The [comparison record](results/comparison-summary.json) preserves that limitation. Small synthetic samples, one output per arm, model judgments and possible position effects further limit conclusions. Actual author feedback, reader outcomes and unaided learning remain unmeasured.

The previous corpus analyses, coding results, accepted foundations and global skill installations are preserved. The final source snapshot and recovery receipt make this revision reviewable without rewriting those earlier findings.

[The final consistency receipt](results/final-validation.json) records seventeen scoped checks. Checkpoint details are in [the experiment index](README.md).
