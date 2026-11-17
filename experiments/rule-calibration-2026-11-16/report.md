# Fresh-paragraph comparison: original rules and Astra revision

16 November 2026. **This pilot did not demonstrate improved reproducibility from Astra's revised package. Keep it as a candidate and resolve the diagnostic issues before scaling.** The result does not establish which arm is more accurate: there is no human gold standard.

Eight independent GPT-6.1 Terra/high coder instances produced 144 paragraph codings: two coders per rule arm on each of two samples. The 36 unique targets come from twelve fresh documents, with identical available source context within each comparison. Separate fresh-context dispatches instructed coders not to inspect one another's work. The shared filesystem was not an access-control sandbox. A separate masked model review inspected twenty prespecified targets; another agent independently audited the arithmetic and source bindings.

## Matched results

Exact agreement means both coders assigned precisely the same set of functions to the paragraph. “Clear” excludes unresolved possibilities; “candidate union” includes them. The denominator is unique target paragraphs compared within an arm, not all individual coder records.

| Sample | Paragraphs / documents | Original: clear exact | Revised: clear exact | Original: candidate-union exact | Revised: candidate-union exact |
| --- | --- | --- | --- | --- | --- |
| A | 24 / 8 | 13/24, 54.2% | 12/24, 50.0% | 12/24, 50.0% | 12/24, 50.0% |
| B: untouched additional documents | 12 / 4 | 8/12, 66.7% | 6/12, 50.0% | 7/12, 58.3% | 6/12, 50.0% |
| Combined | 36 / 12 | **21/36, 58.3%** | **18/36, 50.0%** | **19/36, 52.8%** | **18/36, 50.0%** |

The revised-minus-original difference in clear exact agreement is −8.3 percentage points overall. Mean set Jaccard was 0.829 versus 0.795. Neither result supports an agreement gain here. This is a small, selected, document-clustered model pilot with one coder pair per arm per stage; no statistical significance or general superiority claim is made. The earlier 138-paragraph experiment is not a matched comparator.

| Context, nine paragraphs from three documents each | Original: clear exact | Revised: clear exact |
| --- | --- | --- |
| Argument / perspective | 6/9 | 4/9 |
| Personal reflection | 5/9 | 5/9 |
| Research / synthesis | 5/9 | 4/9 |
| Explanation / procedure | 5/9 | 5/9 |

By document, the revised pair had more exact matches in one document, fewer in four and the same in seven. Of the eighteen revised disagreements, fourteen were strict subsets and four contained different labels on both sides. Original disagreements comprised ten subsets and five two-sided differences. Optional additional labels remain a major source of variance.

## Did uncertainty or label loss explain the outcome?

Each arm supplied 72 paragraph-coder records: 36 targets × two coders.

| Recording outcome | Original | Revised |
| --- | --- | --- |
| Clear function assignments | 188, or 2.61 per paragraph-coding | 174, or 2.42 per paragraph-coding |
| Unresolved function records | 2 | 0 |
| Empty clear-label sets | 0 | 0 |
| All role records, including rejections | 191 | 182 |
| Compact JSON characters | 77,833 | 236,682 |

The revised arm assigned fewer positive labels without improving exact agreement. Its richer uncertainty mechanism was unused in these submissions. This does not establish that nothing was uncertain: the masked review found contestable choices. In particular, support had six positive assignments across original coders and one across revised coders; illustration had twelve versus six. These reductions need source-level review rather than being interpreted automatically as better precision or lost accuracy.

The revised records contained approximately **3.04 times** as much compact annotation text. This measures artifact volume, not cognitive effort, tokens or cost. Coder-recorded drafting intervals totaled 262 seconds versus 398 seconds across the respective four instances; these are not independently timed end-to-end workloads, exclude later repair, and have uncertain tool/scheduling effects. A-revised-2 retained a second submission correcting context bookkeeping, with unchanged role judgments and anchors. Both retained versions pass the bounded checker.

## What the revised records make visible

On nine paragraph/function instances where both revised coders assigned the same relational function, their targets pointed to the same source-unit set in seven. Mean target character-span overlap was 0.390. Unit matching and span overlap are structural proxies, not tests of whether target meaning agrees. For example, both coders can select different clauses within the same paragraph, or choose adjacent contributions that plausibly belong to the same argument.

Agreement restricted to the relation layer was 29/36, but 21 of those were shared empty sets. Temporal-layer agreement was 35/36 with 27 shared empty sets. Those high percentages should not be mistaken for reliable positive coding. Per-label positive agreement and directional differences are retained in [comparison.json](results/comparison.json).

The richer target and attribution records help locate disagreements for inspection. That is a concrete inspection capability; improved reader outcomes or semantic accuracy have not been demonstrated.

## Concrete cases and proposed clarifications

These are diagnostic readings, not adjudicated gold labels. The [masked review](review/review.md) covers twenty prespecified paragraphs and eighty anonymous coder records. Four codings were shuffled separately per paragraph; wording and richer target detail could still reveal their arm. Its concerns are not an accuracy score. Some “potential omissions” refer to an additional instance or span of a function already present, rather than a missing paragraph-level label; its “extraction” concerns generally address annotation coverage, not proof of a faulty source parser.

| Fresh case | Original coders | Revised coders | What needs a better example or rule |
| --- | --- | --- | --- |
| `PMC2867979-p011`, reporting-bias narrative review | Both: compare, qualify, report, support | Both: illustrate, qualify, report; one also compare | A reported study can make an association concrete **and** supply evidence for it. Do not make support and illustration exclusive. The scope exclusion at the end limits this review's coverage, not the preceding association. |
| `python-p02`, module introduction | Define + explain versus define + report | Both: define + explain | A brief operational definition can count. State what relationship the import account explains, rather than calling every capability statement an explanation. This is a local agreement improvement, not an overall one. |
| `curl-p04`, response-code description | Both: define + report | Explain + report versus define + report | A short statement of what something communicates can characterize its meaning and explain a relationship. Specify when these are distinct jobs; do not require a complete textbook definition. |
| `LF-d23d38c43ea7-p005`, Russell's transition to his thesis | Both: assert + orient | Both: assert + orient, with different orientation targets | Matching labels can conceal a different account of what the passage prepares. Record local versus later target scope without assuming that one target is always compulsory. |
| `LF-03f718ef8cc6-p021`, narrated hang-gliding episode | Both: explain + narrate; one additionally retains unresolved instruct | Both: explain + narrate + report | Distinguish a speaker's instruction to a character, an explanation of that instruction, and a directive addressed to the reader. Retain speaker and addressed actor; a cross-paragraph dialogue can still narrate. |

The review also found a reason claiming four category definitions supported by only one category's quoted anchor (`PMC4566873-p028`), and a chunked-response explanation whose reason went beyond its selected quotation (`curl-p11`). Exact quotations alone do not establish sufficient evidence coverage.

**Proposed disposition before another small test:**

1. Keep the twelve IDs. This pilot does not establish that merging functions would improve usefulness; several disputed combinations perform defensible different work.
2. Separate an **evidence anchor** used to justify a label from the **complete realization span** used to measure how much text performs it. Allow discontinuous realization spans and overlap; maintain measurement scope and attribution. Require explicit `not_collected` when only an evidence anchor was collected.
3. Add a small set of contrasting examples for support + illustrate, partial define + explain, report + narrate, and reported versus reader-directed instruct. Each example should show both a defensible overlap and a superficially similar case with no additional job.
4. Make relational scope visible: the affected claim/contribution, local or later scope, speaker and certainty. Preserve multiple plausible target readings rather than substituting an easier claim.
5. Reduce routine form filling. Retain common context once per document with explicit per-target overrides; collect detailed target/alternative fields when the relation or ambiguity calls for them. Evaluate this as a new interface proposal, not a validated improvement.
6. Have the author review a few disputed cases, freeze the next candidate and repeat on additional untouched documents. Keep this sample as development material from now on. Test uncertainty and complete realization spans explicitly; no numeric acceptance threshold has been selected.

These proposals are saved for review; the original catalogue and frozen candidate have not been changed or installed.

## Length measurements and their limits

The common tokenizer mechanically counted the thirty-six unique whole target paragraphs:

| Selected context | n | Observed minimum | Median | Observed maximum |
| --- | --- | --- | --- | --- |
| Argument / perspective | 9 | 48 | 157 | 264 |
| Personal reflection | 9 | 15 | 121 | 589 |
| Research / synthesis | 9 | 60 | 106 | 314 |
| Explanation / procedure | 9 | 13 | 45 | 142 |

These are convenience-sample descriptive counts, not general form profiles, working targets or limits. Contexts combine forms; software sources are scoped sections. Typical audience vocabulary, sentence complexity and voice have not been validated here.

**Do not use the recorded anchor-word distributions as function-length ranges.** Coders often supplied short diagnostic quotes rather than complete realizations. For example, the two A revised coders' median explain-anchor lengths were 5.5 and 24 words. That difference can reflect selection practice rather than actual rhetorical length. `lengths.role_span_by_coder` in the machine result means only the within-target union of submitted clear-role anchors. It is retained for audit, with this narrower interpretation. Working targets, minimum limits and maximum limits remain unset.

## What was frozen and checked

The [plan](protocol/plan.md), original catalogue and Markdown guide, revised JSON rules/examples, common recording format and checker were hashed before coder starts. Both source samples were sealed before A coding; B used four new instances without rule tuning. Original coders used the original function definitions, with the same typed-status and quotation reporting envelope used in the revised arm. Revised coders additionally used Astra's procedures, worked examples, targets, per-function fields and evidence distinctions. This is a comparison of whole guidance packages, not the isolated effect of rule wording or an exact historical rerun of the old annotation interface.

There are three documents per context: two in A and one in B. Essay sources range from 1932 to 2014; the retained review metadata gives 2010/2014 dates, including online publication where relevant; Git and Python use immutable 2014 versions and curl a 2019 supplement. Targets are fixed positions at approximately one-sixth, one-half and five-sixths of each eligible prose sequence, without function-based selection. [Source manifest](sampling/source-manifest.json) and [exclusions](sampling/candidate-exclusions.json) retain scope, provenance, dates and rejected candidates. “Fresh” means outside recorded function coding and rule-development examples, not outside model training. Prior-exposure and cross-format-duplicate checks are bounded, as the audit explains. This is not coverage of all seventeen proposed forms or a prominence-ranked sample.

The checker validates exact source quotations and digests, target binding, known functions, designated fields, statuses, coverage and summary derivation. Its experimental interface is narrower than Astra's full proposal: it does not enforce the supplied layer field and it disallows different decision types for separate instances of one function within a paragraph. All selected revised records supplied the expected layer; none recorded mixed decisions. These checks cannot rule out interface effects before submission or establish semantic correctness. Seven focused checker tests passed.

The [independent audit](audit/report.md) reproduced all primary A/B counts and all nine target-span overlap calculations; inspected four source boundaries and neighboring contexts against retained underlying sources; and checked source/body/packet bindings and deterministic target positions. No blocking arithmetic error was found. Source authenticity, exhaustive extraction quality and independent reader benefit remain outside that audit. The dispatch receipt is retrospective metadata; self-recorded timestamps are not proof of isolation or complete timing. Full article/source bodies remain in the persistent private `/workspace` cache, separate from these research reports.

## Reproduce

From the repository root, with the retained source cache present:

```bash
python3 -m unittest discover -s experiments/rule-calibration-2026-11-16/analysis -p 'test_contract.py' -v
python3 experiments/rule-calibration-2026-11-16/analysis/analyze.py
python3 experiments/rule-calibration-2026-11-16/audit/check.py
```

The analysis selects the retained final submission for each coder, checks frozen input hashes, preserves raw packets and emits normalized copies and `results/comparison.json`. Re-running changes its generation timestamp/digest; refresh the audit receipt afterward. Source-packet construction is a preparation step, not necessary for analysis; do not reseal or replace the frozen sample to reproduce this run.
