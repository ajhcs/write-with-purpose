# Unblinded author-review results

The author explicitly requested unblinding after closing the review. **The revised writer was preferred in six rated cases, the baseline in three, and the original in one.** The frozen key matches its pre-generation hash commitment; raw choices, comments, blank fields and uncertainties were not changed.

The result is promising for continuing with the revised writer as the working candidate. It does not establish a general success rate, a reliable margin of superiority or a particular rule's causal effect.

## What was actually compared

Every generator selected `write-with-purpose`: baseline **0.4.0-alpha.5** versus revised **0.4.0-alpha.6**. All eight contexts used GPT-6.1 Terra with high reasoning effort. Both received the same substantive-rewrite briefs and source context. The editor skill was available in each package but was not selected, so this round does not directly test `edit-with-purpose`.

All ten submitted ratings concern section passages. The four full-work comparisons have no submitted ratings. There was one paired generation per source and condition, with four tasks sharing each context. The ten ratings therefore are not ten independent replications. The unrated cases remain unrated.

## Your choices decoded

| Case | Source and location | Chosen version | Condition preferred | Substantive-improvement response |
| --- | --- | --- | --- | --- |
| R01 | CS50 · opening | B | Baseline | Baseline |
| R02 | CS50 · middle | B | Revised | Revised |
| R03 | CS50 · closing | A | Baseline | Baseline |
| R05 | Healthcare engineering · opening | A | Revised | Revised |
| R06 | Healthcare engineering · middle | B | Revised | Unsure |
| R07 | Healthcare engineering · closing | A | Revised | Revised |
| R09 | Doctorow · opening | A | Baseline | Baseline |
| R10 | Doctorow · middle | A | Revised | Revised |
| R11 | Doctorow · closing | Original | Original | Revised (A) |
| R13 | Python · opening | A | Revised | Unanswered |

R01's praised B passage was baseline. R05's strongly praised A passage was revised. Enthusiasm in the comments should not be interpreted as uniformly supporting either condition, or as a measured margin between versions.

R11 is not a contradictory rating: the author can recognize a substantive improvement in A while still preferring the original's overall story. R06's preferred rewrite is not automatically a confirmed substantive gain, and R13's blank is not a negative or positive rating.

| Section | Revised preferred | Baseline preferred | Original preferred |
| --- | ---: | ---: | ---: |
| Opening | 2 | 2 | 0 |
| Middle | 3 | 0 | 0 |
| Closing | 1 | 1 | 1 |
| Total | 6 | 3 | 1 |

The middle-passage result is a useful hypothesis to retest. It does not establish that the revised rules are universally better for middles or that the baseline should automatically handle openings and endings.

| Source | Revised | Baseline | Original |
| --- | ---: | ---: | ---: |
| Cole's CS50 essay | 1 | 2 | 0 |
| Cole's healthcare-engineering essay | 3 | 0 | 0 |
| Doctorow's platform essay | 1 | 1 | 1 |
| Python tutorial | 1 | 0 | 0 |

These source differences support keeping form and section visible in further testing. They do not yet justify a routing rule by form; the samples and generation contexts are too few and clustered.

## Improvement priorities

### Select examples instead of preserving enumerative filler

R02 objects to both versions' long inline lists and to multiple inventories in a paragraph. R03 objects to a three-item setup too, so a count ceiling is not a sufficient quality rule.

For Cole's prose, carry the stated preference for at most three illustrative items into the author profile, with attention to whether any enumeration earns its space. Choose the examples that establish the point, or express their accurate shared role or relationship. Splitting a long inventory into several smaller lists would not address the criticism. Required technical coverage is a separate task obligation; do not silently lose facts to satisfy a count.

A likely contributor worth testing is the common trial brief's instruction to preserve material facts and examples. Both versions may have treated illustrative inventories too literally. A more discriminating brief would protect facts and required coverage while allowing selection of examples. This is a hypothesis about the prompt, not an established cause.

A future linter could count explicit list items and flag likely inline enumerations. It would supply review candidates, not decide whether an item is necessary or automatically delete it. No such new linter was implemented in this unblinding step.

### Preserve the explanatory connection and narrative progression

The author singled out the baseline's R03 sentence:

> The speed makes it all the more useful to know what each part is meant to do and to check what happens when the parts meet.

The revised counterpart says:

> I still need to know what each part is supposed to do and check what happens when the parts meet.

The baseline explicitly develops why increased speed makes this understanding more valuable. The revised sentence states a continuing obligation. Both may be intelligible, but the latter weakens the particular relationship the author praised.

R11 similarly distinguishes corrected wording from a stronger overall story. Refine the existing whole-result review to inspect the passage's progression and rhetorical force: what leads to what, what becomes more important, and what the ending achieves. When the original progression works better, retain it and apply the useful local corrections. This needs actual comparison and author judgment, not a universal story template or shorter-sentence target.

Use the baseline wins and Original R11 as contrasting examples within the revised package. Keep these as scoped examples rather than inventing a new rule that all endings need restraint. For commentless choices, proposed explanations of preference remain the analyst's hypotheses.

### Check new implications and inherited caveats separately

The separate source audit found a subtle addition in revised R05: “an argument I first encountered in” adds a first-encounter claim that the supplied original does not establish. Removing the unsupported “first” can preserve the preferred prose. The audit also flagged baseline R11's change from “the former” to “both,” which broadens or resolves a reference without establishing the intended scope. These flags concern supplied-source fidelity; they do not prove the real-world claims false.

The enrollment/credit disclaimer in R01 already existed in the original and was retained in both rewrites. The author's objection therefore also updates the source understanding. Preserve that correction in the author-fact record. When credential status matters, use the precise author-confirmed claim; do not invent a degree or return to an unwanted denial. When it does not serve the passage, the disclaimer need not occupy the narrative.

Strengthen semantic review of changed chronology, causal force and attribution using exact edit differences and supported source anchors. Existing numeric/literal checks cannot certify those implications. Avoid turning words such as “first” or qualifications generally into a blacklist.

## Recommended next iteration

Retain the revised writer as the working candidate and refine it with the specific successful and unsuccessful passages above. Put author preferences in the author profile, operational distinctions in the relevant reference, and observed errors in short contrasting examples. The four core rules do not need to become a larger universal checklist.

Test the changes on fresh material with repeated independent generations and a manageable set of whole-piece comparisons. Test the editor under genuinely editorial requests, separate from the substantive-rewrite wording that selected the writer in every context. Keep human preference, source fidelity and measurable constraints as distinct outcomes.

These are proposed improvements. No canonical skill, source website or installed copy was changed by unblinding.

## Evidence

[Decoded data](unblinded-results.json), [all sixteen A/B mappings](unblinded-key.json), [reveal authorization](reveal-authorization.json), and [binding/arithmetic checks](../validation/unblinding.json) preserve the result. The [pre-reveal register](pre-reveal-adjudications.json) and submission history preserve the blinded judgments. The key was not regenerated and the writing was not edited after the author's choices.

[The structured improvement plan](improvement-plan.json) distinguishes proposed guidance, code opportunities and test gaps. [Source-audit notes for the rated cases](unblinded-source-notes.json) preserve the model's findings separately from the author's preferences; their judgments are not treated as ground truth.
