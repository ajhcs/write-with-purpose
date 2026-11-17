# Reading the disagreements before expanding the sample

Recommendation: improve operational rules and contrasting examples before merging functions. Preserve legitimate multifunction writing. No catalogue change or original recoding is adopted by this review.

The [complete count and twelve-case diagnostic sample](diagnosis.md) covers all 138 second-coded targets. Of 83 disagreements, 50 have one label set strictly contained in the other; 41 differ by exactly one label. Another 33 have labels exclusive to each side. These are differences between coding passes, not an accuracy test with a reference standard. The primary column aggregates several article-level coders; A/B name the original and second coding roles rather than one first analyst for the whole corpus.

Four cases were chosen for a worked discussion: one direct explain/interpret substitution, one reflective-instruction addition, one category/example/scope disagreement, and one history/evidence overlap. This selection is diagnostic, not representative. Their [source and coding records](worked-cases.json) preserve hashes, private paragraph locators, both original label sets, recorded reasons where available, and proposed readings. Full normalized paragraphs and immediate context are recoverable from the private cache. The reading comparison displays the actual text; extraction normalization is identified. Neither coder set has been overwritten or promoted to a gold label.

## Four proposed readings

**NEJMp1616577-p10 — explain versus interpret.** The paragraph beginning “Put simply” summarizes the claimed stakes of repeal. Its preceding paragraph supplies a projection and conditional reasoning. I prefer interpret for the disputed local job: the paragraph draws the consequence together, without developing how a mechanism produces it. Naming an effect need not explain its mechanism. Assert can coexist. This is a boundary example for the existing definitions, not evidence that explain and interpret should merge or that the paragraph can have only one job.

**drucker-034 — orientation versus instruction.** The passage introduces the question of personal values, distinguishes it from ethics and names a mirror test. It prepares the next section and directs a self-question; the following paragraph develops an example. Whether to record instruct depends on an explicit policy for reflective prompts. Cognitive actions can be instructions; a bare question heading is not automatically one. An anchor and context can preserve the two jobs without treating orientation and instruction as rivals. The define tag, shared by both coders, should not be read as proof of a complete definition: the local distinction is limited. Agreement alone does not establish semantic correctness.

**xml-02359-p018 — definition, examples and scope.** The paragraph reports Table 3 and restricts categorization to the cases with adequate information; it then lists examples of outcome categories. My proposed reading is report + qualify + illustrate. The parenthetical restriction has a recoverable target: the table's categorization claim. The examples do not establish complete category membership rules, so define is less convincing. Both original codings omit something in this proposed reading; selecting an automatic winner would hide that.

This is also a measurement lesson. The paragraph contains **113 common-tokenizer words**, while its explicit denominator/scope condition contains **13**. The earlier function-conditioned distributions measured whole paragraphs containing a tag. They did not measure the length of the function's particular realization. Neither number supplies a writing target.

**drucker-007 — history and support.** A historical account of feedback analysis can report content, narrate an event sequence, advance a causal explanation and be offered as a reason for the preceding recommendation. These are different aspects of the paragraph. Require an identifiable supported claim and separately assess the truth and adequacy of the author's historical/causal account. Calling something intended support does not verify it. Fewer flat labels might raise exact agreement without preserving these distinctions.

## Candidate rules for the next small test

1. **Anchor every proposed function.** Give the words realizing it and a brief reason. A short but consequential qualification can deserve a tag; there is no proposed minimum word count. A label cannot rest only on paragraph position, a citation, a hedge, or declarative grammar.
2. **Separate local work from a relation to other material.** For support, qualify and illustrate, identify the claim or idea connected. Existing relation names can express these links. A narrative can report events and illustrate an idea; these jobs do not need to compete for one slot. Do not require exactly one primary function for every paragraph.
3. **Keep rhetorical use and evidence validity separate.** Record that a passage offers a reason independently of whether that reason is true or sufficient. A hypothetical instance may illustrate or support reasoning without becoming empirical evidence.
4. **Supply context and permit unresolved cases.** Include the relevant neighboring paragraph or target claim. Use an explicit status such as clear, ambiguous or insufficient_context, with a reason. The existing second-coder uncertainty field mixes nulls, booleans, strings and lists; do not treat absent notes as calibrated certainty.
5. **Distinguish measurement units.** Retain whole-paragraph lengths and any explicitly annotated function-span lengths separately. Some functions require discontinuous spans or context; do not force one contiguous span where it would misrepresent the writing. The existing annotation prototype does not yet implement nested move spans.

These are proposed application rules for the existing catalogue. They are not established inter-rater results. A link/span checker can validate IDs, text and offsets, not whether the interpretation succeeds.

## Contrasting examples to discuss

The following are synthetic teaching examples, not corpus observations or accepted reference labels:

| Boundary | Example A | Example B | Distinction to test |
| --- | --- | --- | --- |
| Explain / interpret | The queue grows because arrivals exceed the server's processing capacity. | The growing queue suggests the present staffing plan will miss its service target. | A causal relationship versus an implication drawn from an observation |
| Define / report a definition's use | An urgent request is one requiring a response within two working hours. | We used the agency's definition of an urgent request. | Gives a usable category rule versus reports adopting a rule supplied elsewhere |
| Orient / instruct | How do we know which records are eligible? | Compare each record with the eligibility criteria and record the reason for exclusion. | Frames the reader's question versus directs an executable action |
| Illustrate / intended support | Imagine a customer abandoning a form after its third error message. | In our observed sample, abandonment increased after repeated error messages; we offer that finding as a reason to simplify validation. | Makes a situation concrete versus offers an observation for an identified claim; validity still needs assessment |

The actual self-question in Drucker is deliberately harder than the clean orientation/instruction pair. Include near-boundary cases as well as clear contrasts; otherwise a model can memorize examples without learning the decision.

Before expanding, use these as teaching cases, then independently code a small new set whose prior labels and adjudication were not supplied. Review function evidence and target relationships as well as complete label-set agreement. There is no evidence here for a particular catalogue merger or for a forced single-function system.

## Reproduction

`python3 experiments/pattern-test-2026-11-16/disagreement-review/compute.py` recounts the original comparisons and recovers the twelve diagnostic paragraphs. `build_worked_cases.py` verifies four paragraph hashes and the 13/113 word scopes, retains proposed discussion records and rebuilds the reading comparison from its literal fragment template. It leaves the catalogue and original coding packets untouched. The JavaScript smoke receipt records selector resolution, case changes, state restoration and text preservation; browser rendering was not inspected.
