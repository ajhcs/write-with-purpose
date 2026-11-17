# Measured family and form profiles

Design proposal, 15 November 2026. This extends [the form model](form-model.md) with the user's proposal to extract recurring structure and measurable ranges from examples. No reference corpus has been assembled or measured for this proposal. Numeric profile values remain unestimated.

Cole subsequently approved the nine feature groups, the Family → Form → Section hierarchy, and the distinction among observed ranges, working targets, and declared limits. The authoritative record is [accepted foundations](../../docs/writing-harness/accepted-foundations.md). The larger candidate measurement table below is exploratory detail rather than an expansion of the agreed nine groups.

## The unit to build

Each family supplies broad expectations. Each form supplies a more specific profile with two main outputs:

1. Distributions for measurable features, with the documents, scope, and measurement method identified.
2. A small set of reusable structural patterns, expressed as the work each part performs, with source-specific wording and facts removed.

The family and form selections should reduce the choices that the writer model has to invent. A chosen pattern and working budget turn those expectations into a concrete plan. Deterministic code can then verify the measurable parts of that plan. Interpretation, expression, and editorial judgment remain assessed separately.

Our current families began as navigation groups. Their value as predictive groups must be tested. If grouping forms produces several distinct clusters or extremely broad ranges, expose those differences and prefer the relevant form profile. A pooled family average may be a poor description of every member.

## What can be extracted

These are proposed measurement candidates, not established findings about the seventeen candidate forms.

| Feature | Measurement | Appropriate level and use |
| --- | --- | --- |
| Document size | Main-prose words; title, abstract, captions, notes, and references counted separately | Compare documents of the same form and declared scope. Use for whole-piece planning. |
| Heading structure | Heading count, levels, section count, heading length, and presence of unheaded passages | Form and structural pattern; distinguish visible headings from inferred rhetorical sections. |
| Allocation of space | Words per section and section share of main prose | Form and section role; useful for balancing a draft at different total lengths. |
| Paragraph shape | Words and sentences per prose paragraph; one-sentence paragraph frequency; within-document spread | Form, section role, and pattern. Preserve variation rather than replacing paragraphs with uniform blocks. |
| Sentence shape | Words per sentence; short and long tails; within-section variation | Section role and form where data supports it. Both subject matter and author may explain substantial variation. |
| Word length | Characters per word; optional syllable estimates | Descriptive diagnostic. Names, technical terms, language, and tokenization affect the result; it is a weak standalone writing target. |
| Rhetorical moves | Presence, recurrence, position, relative size, and order of communicative functions | Requires an annotation scheme and review. A move can span part of a paragraph or several paragraphs. |
| Examples and support | Where examples occur; citation counts and distribution; quoted-text share | Counts are measurable; whether an example explains or a source supports a claim requires judgment. |
| Presentation | Prose, lists, tables, code, figures, and captions; list-item and step counts | Form and document scope. Keep denominators explicit; avoid mixing code and prose words. |
| Register indicators | First-person use, questions, tense, obligation words, and qualification markers | Candidate diagnostics. Automated classification can be imperfect and frequencies do not establish good style. |
| Connections | Explicit cross-references and links; annotated transitions between moves | Exact references can be checked mechanically; reasoning continuity requires editorial assessment. |

Start with size, heading structure, section allocation, paragraph and sentence distributions, presentation, and a small reviewed move vocabulary. Introduce more difficult linguistic measures only when they help a specific decision.

Family and form alone do not determine the right claims, factual accuracy, the reader's actual vocabulary, originality, or whether a passage is useful. They provide expectations against which we can inspect and plan a piece.

## How to express a range

For every sufficiently supported numeric feature, retain:

- Number of contributing documents and number of measured units.
- Observed minimum and maximum.
- Median, 25th and 75th percentiles, and optionally 10th and 90th percentiles.
- Measurement unit, inclusion/exclusion rules, parser version, and corpus identity.
- Whether the summary is across documents or across units within documents.
- Uncertainty or a clear small-sample status; missing and unavailable measurements remain distinct from zero.

The middle 50% interval and median describe the central portion of the observed sample; min and max show its extremes. Wider percentile bands can also be useful, but their estimates need enough data. These are descriptive intervals, not confidence intervals or definitions of acceptable writing. [NIST box-plot guidance](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm)

Keep three separate concepts:

| Record | Meaning | Consequence |
| --- | --- | --- |
| Observed range | What occurred in the reference collection | Comparison and explanation |
| Working target | A chosen budget or pattern for this piece | Planning and targeted revision |
| Declared requirement | An explicit author, assignment, or venue constraint | Deterministic enforcement when the condition is mechanically testable |

A value outside a corpus range should prompt an inspectable observation, not an automatic rewrite. For example, an unusually long introduction may be justified by a novel concept or may reveal delayed explanation. The range cannot decide which.

Compute paragraph and sentence summaries within each document and section first, then summarize those document-level results with the intended weighting. A long document should not silently dominate a typical-document profile. Retain pooled unit distributions when useful, but label them separately. Do not infer a typical sentence distribution from a distribution of document medians.

Budget relationships also matter. Choose a feasible total and allocate it among sections whose shares sum to one. Do not independently combine marginal medians or maximum values and assume they form a coherent document. Preserve observed combinations or use a reviewed pattern as the basis for the allocation.

## Structural patterns with the wording removed

The user's observation suggests a progression in the useful information supplied by a blank:

1. A container: paragraph.
2. A position: opening paragraph.
3. A communicative job: establish the reader's question.
4. A concrete assignment: use the author's supplied situation to establish the question that the next section explains.

The third and fourth descriptions narrow the model's task while leaving expression open. In genre analysis, a rhetorical move is a unit serving a communicative function. Manchester's Academic Phrasebank uses this concept and describes extracting general patterns from authentic writing. Here we propose retaining functions and structural relationships while omitting borrowed sentence stems from the writer's structural reference. [Academic Phrasebank](https://www.phrasebank.manchester.ac.uk/about-academic-phrasebank/)

For a move or section, record an identifier, function, source-input bindings, required information, prerequisites, allowed repetition, conditional presence, possible realization, and size guidance. A function is not necessarily a printed heading. The profile must distinguish author instructions from text intended for publication.

For a conceptual explainer, candidate patterns could include:

- Question, mechanism, worked example, qualification, implication.
- Concrete case, discovered pattern, explanation, broader consequence.
- Misconception, useful distinction, explanation and evidence, revised understanding.

These examples are proposed patterns for testing. Their prevalence has not been measured. The number and shape of useful patterns should come from the corpus and practical evaluation. Each form can contain multiple patterns without adding more up-front classification choices.

See the [content-neutral scaffold](examples/conceptual-explainer.scaffold.md) for a concrete example. It contains no invented numerical ranges and no factual claims to transplant.

## Extract examples in a separate stage

The reference-analysis stage can inspect full exemplars. It should preserve document identity and produce measured features, a document tree, reviewed move annotations, and abstract patterns. Keep original text available for auditing these extractions.

The writer receives the selected pattern, resolved working budget, relevant checks, and the author's actual material. A structural exemplar's topic-specific wording, memorable metaphors, names, facts, citations, and authorial stance should not enter that packet. Use multiple exemplars when deriving a reusable pattern, so a single author's distinctive sequence does not accidentally become the default for the form.

The author's own approved wording can remain available for voice, and factual sources remain available for evidence. Those are separate roles from an external structural exemplar. Merely replacing names with X does not reliably remove a distinctive argument or phrase; abstraction needs review.

This is a hypothesis about improving our writing workflow. Skeleton-of-Thought research demonstrates a skeleton-first generation approach, but its main objective is inference efficiency. It does not establish that our proposed scaffolds improve long-form authorial voice. [Ning et al.](https://arxiv.org/abs/2307.15337)

## Form-specific components

Resolve the family profile, form profile, and selected pattern into one inspectable plan. That plan should select only the needed components:

- Concise instructions for the selected form and its writing moves.
- The selected scaffold and its source-input bindings.
- Observed ranges and the working targets chosen from them.
- Mechanical checks for actual requirements and measurements.
- Form-specific editorial questions.
- Abstract structural examples, with complete exemplars retained for analysis or explicitly requested inspection.

Record where each setting came from. Specific form guidance can refine a family default, but cannot silently replace an explicit task constraint. Conflicting requirements should be identified with the relevant source. Unavailable metrics and failed parsers must not become passing checks.

The current checker supports declared literal preservation and whole-artifact whitespace-token limits. It does not yet compute these form profiles or section-aware prose distributions. A new extractor would need explicit parsing rules for Markdown, headings, paragraphs, sentences, quotations, abbreviations, citations, tables, and code. Corpus analysis and draft checking must use the same versioned conventions. See [current check scope](../../skills/write-with-purpose/references/checks.md).

## A bounded first experiment

Choose several contrasting forms and collect a diverse pilot set of examples for each. Record author, outlet, date, language, discipline, document scope, selection reason, and source. Awards and high citation counts can identify candidates; evaluate suitability as writing examples separately. Include variation within the form, and keep repeated editions, reprints, and closely related pieces from distorting counts.

Measure the low-ambiguity features. Independently review a sample of section and move annotations against written definitions and retain disagreements. Compare family-level distributions with the distributions of their forms. Investigate distinct clusters rather than hiding them in one median. Use held-out authors or outlets where practical when assessing whether the profile transfers.

Test four prompting conditions on the same writing tasks:

1. A complete exemplar and a request to follow its format.
2. A positional skeleton with labels such as title, heading, and paragraph.
3. A functional skeleton with named writing moves and source-input bindings.
4. The functional skeleton plus measured ranges and executable checks.

Hold the author's source material, model configuration, requested contribution, and evaluation criteria steady. Run repeated trials. Record context and generation budgets; if repeated checking allows more computation in one condition, account for that difference. An additional comparison can separate the effect of ranges from the effect of revision checks.

Assess structure, compliance with declared constraints, unsupported additions, omission of necessary qualifications, transfer of distinctive exemplar wording or facts, reader understanding, and the author's judgment of voice and originality. Automatic phrase overlap is a screening signal; common technical terms, quotations, and conventional language need separate handling.

Also measure whether the scaffold helps the author write and revise a passage, explain its role, and reuse the technique. Passing a length check does not establish that the approach improved writing. The experiment should decide which information earns a place in the concise skill and which belongs in profile data or optional references.
