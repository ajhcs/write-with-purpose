# Disagreement diagnosis

Of 138 compared targets, 55 have exact label sets, 50 are strict subsets, and 33 have labels exclusive to both coders. Forty-one differ by one label. Several sampled paragraphs perform multiple functions: a smaller catalogue or a forced single primary function would obscure real work and is not justified by these readings. These counts measure agreement between two interpretations, not accuracy.

| Cohort | Exact | Strict subset | Both sides exclusive |
|---|---:|---:|---:|
| NEJM | 23 | 12 | 19 |
| Systematic reviews | 25 | 18 | 5 |
| HBR | 7 | 20 | 9 |

A one-label difference is directional only in the sense of the recorded primary and second sets; neither is a reference standard. Across all targets, primary-only occurrences are report 19, qualify 8, interpret 5, define 5, explain 4, assert 2, orient 2, compare 1, narrate 1, instruct 1. Second-only occurrences are report 16, interpret 15, illustrate 13, explain 11, assert 10, support 7, orient 6, qualify 5, compare 3, instruct 3, narrate 2. Occurrences are labels, not independent paragraphs.

The second coder's uncertainty field is heterogeneous: 49 explicit false, 5 true, 21 nonempty text or lists, 29 empty lists, and 34 null or absent. Null and empty values do not establish certainty, and these categories are not equivalent scales. The JSON retains original values. Evidence quality is separate from rhetorical role: a case can be intended as support yet fail to establish a claim.

## Selection and bounded readings

Within each cohort, sort target IDs lexicographically; select two strict-subset and two both-sides-exclusive cases, preferring documents not already selected within that cohort, then fill in order if necessary. All twelve recovered paragraph hashes matched their recorded text hashes. That does not establish faithful extraction, correct paragraph boundaries, or source validity. Actual texts remain in the private corpus, while IDs and source and paragraph hashes in the JSON allow recovery. These cases are diagnostic, not a representative sample or an adjudicated recode. Where the job is relational, local context may not suffice.

### NEJMp1616577-p01 (nejm, subset)

Primary: assert, interpret, orient, report. Second: assert, interpret, orient.

Opening mixes contextual history, evaluation and recommendation. Whether the past administration sentence is independently substantial reporting is a paragraph threshold decision. Clarify a minimum independent contribution and use a paired example; existing report/assert boundaries already cover declaratives.

### NEJMp1702362-p01 (nejm, subset)

Primary: interpret, narrate, orient. Second: illustrate, interpret, narrate, orient.

A narrated personal episode also makes a general communication problem concrete; both narrative and illustration are plausible. Keep both; illustrate requires an identifiable idea or relationship made concrete, not merely a story.

### NEJMp1707514-p008 (nejm, exclusive)

Primary: interpret, narrate, qualify. Second: interpret, report.

Brief temporal updates lead into reflection. A sequence of life states can be reporting without necessarily constituting a developed narrative; the closing uncertainty may or may not limit an identifiable claim. Use contrasting report/narrate and qualify examples; require the claim limited, not merely a question.

### NEJMp1711886-p001 (nejm, exclusive)

Primary: narrate, report. Second: narrate, orient.

A patient history narrates events and introduces a treatment that gains significance from the following article; orientation is relational to subsequent text, while report reflects content. Keep roles distinct; annotate the later contribution that makes orient operative. Local text alone cannot resolve all relationships.

### xml-02282-p013 (systematic, subset)

Primary: compare, qualify, report. Second: compare, interpret, qualify, report.

The final generalization about study quality explicitly goes beyond the individual estimates and includes a counterexample. The established report/interpret boundary applies. Keep both; use inference versus faithful recap as a contrastive example.

### xml-02298-p003 (systematic, subset)

Primary: compare, explain, illustrate, qualify. Second: compare, explain, illustrate, orient, qualify, report.

A long paragraph combines data quality framing, a case, process description and exceptions. Added report and orient depend on scope and threshold, not missing concepts. Offer a multi-function example with paragraph-level threshold and links to subsequent text.

### xml-02359-p003 (systematic, exclusive)

Primary: illustrate, interpret. Second: assert, explain, illustrate, orient.

The author values patient experience, lists cases and reasons that fragmented care makes a whole-system perspective useful. Assertion, illustration, explanation and interpretation can coexist depending on contribution threshold. Keep the functions; illustrate coexisting claim and reason, and distinguish inference from mechanism using paired examples.

### xml-02382-p038 (systematic, exclusive)

Primary: explain, interpret. Second: assert, explain.

A recommendation to address stigma and its hypothesized effects coexist; calling the final forecast interpretation or assertion depends on whether synthesis or proposed position is the relevant job. Clarify assert versus interpret operationally with examples rather than merge them.

### customers-004 (hbr, subset)

Primary: illustrate, report. Second: assert, illustrate, report, support.

Industry examples accompany an explicit transformation claim and a market figure. Illustration and support can coexist if the figure is linked as a reason, regardless of whether it proves the broad claim. Retain illustrate and support; code intended evidential link separately from whether evidence justifies the claim.

### designing-services-018 (hbr, subset)

Primary: illustrate, report. Second: illustrate, interpret, report.

A measured tolerance is converted into an acceptable time. Whether that conclusion counts as inference beyond faithful restatement is close; illustrative status depends on its relation to surrounding method. Use a near-boundary report/interpret example and record the contextual target of illustration.

### house-020 (hbr, exclusive)

Primary: explain, orient. Second: explain, instruct.

The authors describe where they place evaluations in a diagram as part of a method. Whether this is instruction for the reader or narration of the authors’ practice depends on surrounding procedural framing. Clarify instruct as an actionable direction in context, including descriptive first-person method wording; no automatic label.

### power-030 (hbr, exclusive)

Primary: explain, qualify, report. Second: assert, explain, illustrate.

The paragraph mixes a tentative gender-related proposition, a directions example and a proposed mechanism. An example can illustrate a claim even when its evidential basis is weak; qualification requires a limit attached to a claim. Separate illustration, assertion, explanation and qualification from the strength or truth of the generalization.

## Decisions to test before scaling

- **Keep** report, interpret, illustrate, support, narrate, orient, assert, explain and instruct as distinct candidates. Their jobs can coexist and some depend on relations to other claims or neighboring text.
- **Clarify operational application:** specify what counts as a sufficiently distinct contribution at paragraph level; require coders to identify the claim supported or limited, the idea illustrated, and the neighboring contribution oriented toward. Permit multiple functions without requiring one primary role. Use context when the target job is relational and record insufficient context or extraction uncertainty.
- **Improve examples:** contrast faithful recap with a new inference; narrative with a bare sequence of updates; descriptive method with an instruction; an instance with evidence offered for a claim; a hedge with a claim-bound qualification. Include long paragraphs with several legitimate functions. These primarily operationalize boundaries already present; they are not evidence that new definitions are required.
- **Merge candidates:** none demonstrated by this sample. Assert/interpret and report/interpret merit targeted contrastive testing, but ambiguity alone does not show they are redundant. Test independent coding on new cases after revising the guide; no catalogue changes are accepted by this diagnosis.

[Machine-readable counts and case provenance](diagnosis.json) include every compared target, directional set differences, source hashes and original uncertainty values. The counts depend on existing target selection and recordings, and no whole-corpus recode was performed.
