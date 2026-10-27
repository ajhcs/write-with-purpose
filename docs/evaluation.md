# Evaluation and limits

The package separates three questions:

| Question | Evidence |
| --- | --- |
| Conformance | Does the writing meet the actual brief, terminology, coverage and format requirements? |
| Correctness | Are the claims, relationships and quantities supported? A faithful paraphrase can still preserve an incorrect source. |
| Usefulness | Does the passage help its reader understand, act, decide or follow the intended experience with a reasonable amount of effort? |

## Skill behavior

Development covered engineering decisions, fictional medical summaries, assignments and explanatory blog passages. Instructions were revised after specific author feedback on unclear connections, repeated explanation, choppy sentences and unnecessary endings.

The editor's final development round used eight known regression cases: four criticized passages, two exact paragraphs explicitly praised by the author, and two passages from a response praised overall. These approval levels were recorded separately. Some cases share facts or text.

Eight fresh editing contexts received only a draft, brief, common prose preferences and the editor instructions. All first proposals were saved before sources arrived. Each editor then checked the relevant source packet. A separate source auditor checked masked pairs for conformance and source fidelity. Two additional source-blind readers assessed usefulness through recovery questions and pairwise comparison.

All eight final edits met their briefs and preserved the selected source claims. The source phase narrowed one unsupported claim about the absence of a requirement. The model readers preferred four edits, two originals and two ties; one passage remained unchanged.

Those preferences did not consistently match the author's feedback. Some edits shortened an explicitly liked explanation, retained an unwanted closing observation or reduced a handoff's findability. These are usefulness limitations even where conformance and source fidelity hold. An edit remains a proposal for the author to judge.

An earlier editor version left all four criticized passages substantively unchanged and expanded a passage from a praised response. Its first-stage outputs were retained, and that round stopped before source checking. The retest changed instructions, the author-preference summary and the harness together; it does not isolate the effect of any one change.

These are known development examples, with one editing trajectory per case, overlapping material and model readers. They are not a randomized no-skill comparison, an unseen benchmark or a human comprehension study. They do not validate real medical or engineering use. Personal drafts, coursework and source PDFs are not included in this public package.

## Deterministic checker

The 20 included tests invoke the checker as a real CLI. They cover read-only behavior, finding locations, fenced and inline code, quoted markers, supported and unsupported anchors, lexical number comparisons, literal contracts, hashes, malformed input and structured failures.

The tests deliberately preserve the distinction between a pattern observation and a semantic judgment. Equal numeric tokens do not prove preserved meaning. A successful invocation does not approve the writing. The checker leaves correctness and usefulness unassessed.

## Release boundary

The writer instructions are version 0.3.2 and the editor instructions version 0.1.1. Their text is unchanged in combined package 0.4.0; source files are normalized to UTF-8 with LF line endings. The checker remains version 0.1.0.

No model API, paid service, automatic hook or compulsory editor chain is installed. New writing can use the writer directly. Existing prose can use the editor directly. Request a fresh independent review when the work warrants it.
