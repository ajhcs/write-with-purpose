# Evaluation and limits

The package separates three questions:

| Question | Evidence |
| --- | --- |
| Conformance | Does the writing meet the actual brief, terminology, coverage and format requirements? |
| Correctness | Are the claims, relationships and quantities supported? A faithful paraphrase can still preserve an incorrect source. |
| Usefulness | Does the passage help its reader understand, act, decide or follow the intended experience with a reasonable amount of effort? |

## Skill behavior

Development covered engineering decisions, fictional medical summaries, assignments and explanatory blog passages. Instructions were revised after specific author feedback on unclear connections, repeated explanation, choppy sentences and unnecessary endings.

The editor 0.1.1 development round used eight known regression cases: four criticized passages, two exact paragraphs explicitly praised by the author, and two passages from a response praised overall. These approval levels were recorded separately. Some cases share facts or text.

Eight fresh editing contexts received only a draft, brief, common prose preferences and the editor instructions. All first proposals were saved before sources arrived. Each editor then checked the relevant source packet. A separate source auditor checked masked pairs for conformance and source fidelity. Two additional source-blind readers assessed usefulness through recovery questions and pairwise comparison.

All eight final edits met their briefs and preserved the selected source claims. The source phase narrowed one unsupported claim about the absence of a requirement. The model readers preferred four edits, two originals and two ties; one passage remained unchanged.

Those preferences did not consistently match the author's feedback. Some edits shortened an explicitly liked explanation, retained an unwanted closing observation or reduced a handoff's findability. These are usefulness limitations even where conformance and source fidelity hold. An edit remains a proposal for the author to judge.

An earlier editor version left all four criticized passages substantively unchanged and expanded a passage from a praised response. Its first-stage outputs were retained, and that round stopped before source checking. The retest changed instructions, the author-preference summary and the harness together; it does not isolate the effect of any one change.

These are known development examples, with one editing trajectory per case, overlapping material and model readers. They are not a randomized no-skill comparison, an unseen benchmark or a human comprehension study. They do not validate real medical or engineering use. Personal drafts, coursework and source PDFs are not included in this public package.

## Deterministic checker

The 20 included tests invoke the checker as a real CLI. They cover read-only behavior, finding locations, fenced and inline code, quoted markers, supported and unsupported anchors, lexical number comparisons, literal contracts, hashes, malformed input and structured failures.

The tests deliberately preserve the distinction between a pattern observation and a semantic judgment. Equal numeric tokens do not prove preserved meaning. A successful invocation does not approve the writing. The checker leaves correctness and usefulness unassessed.

## Release boundary

Combined package 0.4.0 retained writer 0.3.2 and editor 0.1.1 with UTF-8 LF normalization. Package 0.5.0 retains the writer and original checker, and revises the editor to 0.2.0 with targeted edits as its default. An exact-span local-edit tool verifies the source snapshot and reconstruction, reports lexical change measurements and preserves existing files. Seventeen additional CLI tests cover its behavior, bringing the Python suite to 37 tests.

Two private worked examples exercise the new editing approach using known feedback. Ten named changes reduce a telemedicine paragraph from 211 to 167 whitespace-separated words, a net reduction of 44 words (20.853%). The meaning check adds observations alongside measurements to cover qualitative findings; the earlier nine-change, 165-word proposal is preserved. A previously praised balance paragraph remains byte-identical at 56 words. These examples were prepared by the parent editor, not fresh blinded agents, and do not demonstrate an autonomous success rate or human preference for the new edit. They illustrate auditable local changes and appropriate restraint. The personal text is not published.

The separate grammar experiment uses 15 synthetic fixtures, a pinned Harper 3.0.0 engine and normalized findings. Three fresh local processes produced identical normalized payload hashes. Accepted domain words removed the two vocabulary flags tested. The same probe exposes missed agreement and sentence-boundary problems and an optional heading-style suggestion. Repeatability is distinct from accuracy and editorial value; the experiment does not establish broad grammar coverage.

No model API, paid service, automatic hook or compulsory editor chain is installed. The grammar experiment's Node dependencies are separate from the installed skills. New writing can use the writer directly. Existing prose can use the editor directly. Request a fresh independent review when the work warrants it.
