# Paragraph functions and reusable components

Research note, 15 November 2026. This develops the next research direction in [accepted foundations](accepted-foundations.md). The frameworks below were read as research sources. External skills were inspected as candidate components, not invoked as governing workflows. New candidates have not been benchmarked in this harness or installed by this work.

## Existing guidance can seed the annotations

| Source | Useful contribution | Scope to retain |
| --- | --- | --- |
| [Harvard: Anatomy of a Body Paragraph](https://writingcenter.fas.harvard.edu/anatomy-body-paragraph) | Distinguishes a paragraph's main claim or idea, its evidence, and the author's analysis of that evidence | A useful academic argument pattern. The guide acknowledges structural variation; do not require every paragraph in every form to follow it. |
| [Purdue OWL: On Paragraphs](https://owl.purdue.edu/owl/general_writing/academic_writing/paragraphs_and_paragraphing/index.html) | Focus, continuity between sentences, identifiable topic, and sufficient development | Use as reader questions. Topic sentences can occur in different positions or be implicit. Do not turn its general advice about short paragraphs into a universal sentence minimum. |
| [Manchester Academic Phrasebank](https://www.phrasebank.manchester.ac.uk/about-academic-phrasebank/) | Organizes academic communication through functions and rhetorical moves, including defining, comparing, interpreting, qualifying, and connecting ideas | Extract descriptions of functions and section relationships for our scaffolds. Borrowed sentence stems are not needed to adopt this organizing idea. |
| [Rhetorical Structure Theory](https://www.sfu.ca/rst/01intro/intro.html) | Describes relationships between passages, including background, elaboration, support, and contrast | Relations between spans are distinct from paragraph labels. An analysis may be ambiguous; record alternatives instead of forcing certainty. |

These sources contribute different levels of description. Paragraph pedagogy helps inspect the internal development of a passage. Genre analysis helps explain its role within a section or form. Discourse analysis helps explain how it connects to neighboring material.

## A proposed annotation model

Keep Family → Form → Section as the organizing hierarchy. Describe paragraphs and smaller spans within it using a few separate questions:

1. **What is this passage about?** A short content description grounded in its text.
2. **What does it do here?** A primary communicative function, with optional secondary functions.
3. **Which words perform that work?** Text spans linked to the source document and version.
4. **What does it connect to?** The claim, definition, example, previous passage, or section purpose it develops.
5. **How does it connect?** For example, supports, explains, contrasts, qualifies, or continues a sequence.

A candidate vocabulary can begin with orienting, defining, asserting, supporting, explaining, illustrating, comparing, interpreting, qualifying, instructing, and narrating or reflecting. These are proposed annotation labels, not eleven new accepted measurement features or a closed taxonomy. Permit mixed and unresolved cases and refine the vocabulary from real examples.

An argumentative paragraph might contain a claim, evidence, and interpretation. Its overall job could be to support a section's argument, while its relation to the previous paragraph could be contrast. Labeling it only “evidence paragraph” would discard useful information.

Store observed functions separately from planned functions. A scaffold assigning a paragraph the job “explain the mechanism” does not establish that the resulting prose actually explains it. Likewise, matching a required heading or finding a citation does not establish useful development or evidential support.

Start by annotating a small, diverse set of good examples and having a second reading challenge the assignments. Use the resulting definitions and disagreements to improve the annotation guide. Deterministic checks can validate source spans, identifiers, counts, and reference integrity; functional adequacy needs editorial assessment.

## Components worth reusing or trialing

| Candidate | Component inspected | Proposed use | Important adaptation or limitation |
| --- | --- | --- | --- |
| Installed `write-paper` | [Introduction guide](/home/builderbob/.agents/skills/write-paper/references/section_guides/introduction.md) and [discussion guide](/home/builderbob/.agents/skills/write-paper/references/section_guides/discussion.md) | Seed section-specific move descriptions and alternate academic structures; relates to F02, F03, and F09 | The introduction guide includes fixed radiology-oriented length, paragraph, and citation suggestions. They are unvalidated defaults for our purposes, not corpus measurements or rules for all academic work. Retain the useful functions and independently establish ranges. |
| Installed `check-reporting` | [Skill and checklist-routing workflow](/home/builderbob/.agents/skills/check-reporting/SKILL.md) | Associate an applicable reporting item with manuscript evidence and locations; relates to F07 and F09 | Reporting presence, research quality, and paragraph effectiveness are different assessments. Applicable guideline and manuscript version must remain explicit. |
| Anthropic `doc-coauthoring` | [Skill source](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md), including reader testing | Reuse the idea of posing reader questions to a fresh context that sees only the document | The full workflow asks many questions and imposes repeated conversational stages. Adapt the focused reader test to our process. Model-reader success does not establish human-reader success. |
| K-Dense `scientific-writing` | [Skill](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md), [manuscript scaffold](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/assets/manuscript_scaffold.md), and the schema and validation opening of [consistency checker](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/scripts/check_consistency.py) | Study its placeholders, evidence records, and methods/results consistency interface; relates to F02 and F07 | The checker consumes a structured JSON registry. It does not itself establish that arbitrary manuscript prose was extracted correctly or that its claims are true. The larger workflow has additional policies that would need a deliberate fit assessment. |
| [Vale](https://docs.vale.sh/) | Official documentation on custom rules and markup-aware scopes | Candidate for selected terminology, heading, paragraph, and other explicit conventions; relates to F02, F04–F06, and F08 where a suitable rule exists | A configurable linter, not a general judge of grammar, purpose, or originality. Activate rules by the selected profile rather than imposing one global style. Documentation reviewed; not executed here. |
| [textstat](https://github.com/textstat/textstat) | README documentation for word, sentence, character, and syllable counts | Candidate numerical building blocks for F01 and F04–F06, after our parser selects the intended text | Needs evaluation on abbreviations, quotations, code boundaries, and technical vocabulary. Its readability outputs do not establish audience comprehension. Documentation reviewed; not executed here. |
| LanguageTool | Existing [repository investigation](../grammar-investigation.md) and [paired comparison](../editor-language-comparison.md) | Reuse the existing grammar-diagnostic trial and adapters as supporting editorial checks | Prior fixture results are bounded evidence, and suggestions still need review. It does not identify paragraph purpose or implement our form profiles. |
| Installed writing-style retrieval skill | [Skill source](/home/builderbob/.codex/plugins/cache/openai-curated-remote/write-like-me/0.1.1/skills/write-like-me/SKILL.md) | Potential access to relevant author-approved examples during writing | Retrieval supplies references. It does not compute profiles or classify paragraph functions. Its source handling rules require separate consideration from an offline corpus extractor. |

The strongest immediate reuse is the local section guidance plus established writing pedagogy, followed by a narrow measurement and linting trial. These are complementary components with different responsibilities.

### Provenance of the remote inspection

The GitHub connector returned these blob identifiers for the inspected files. They identify file contents, not a tested release or a repository commit:

| File | Git blob |
| --- | --- |
| Anthropic `doc-coauthoring/SKILL.md` | `a5a69839ef4a161131d80b6daef10037a9686f4a` |
| K-Dense `scientific-writing/SKILL.md` | `446993fcd4716ae54ab74bc2a91e3bc5af5235c7` |
| K-Dense `manuscript_scaffold.md` | `96cdd508ad5caed48bd97a504d3be98287b2250f` |
| K-Dense `check_consistency.py` | `415be5ce6dae79965f00a3c7cada62a9f012e547` |
| textstat `README.md` | `5d1413ec3e50d81a2365a3e4a1ce712d4c6a68cd` |

K-Dense's inspected skill declares MIT and its repository has an MIT license. Anthropic's README describes open-source skill licensing, but exact terms for copied material should be resolved at the selected revision. No third-party implementation or exemplar prose was copied into this project by this research.

The connected plugin catalog was also searched for writing/editing, grammar/prose linting, and named grammar/style capabilities. It did not surface a dedicated paragraph-function analyzer in those results. The search is not exhaustive; the [plugin directory](https://chatgpt.com/plugins) may contain other candidates. The useful candidates above came from installed skills, primary documentation, and public source inspection.

## Keeping families and corpora informative

“Blog post” describes a publication setting broad enough to contain reflection, argument, explanation, instructions, and other forms. Those differences should be retained during sampling. “Non-fiction books” is both too broad for the current purpose and outside the agreed initial scope.

A proposed family should help narrow at least one meaningful expectation: reader task, structural choices, evidence conventions, or relevant feature distributions. Evaluate that usefulness rather than treating every familiar publishing label as a family. A family can share important conventions without having a narrow word-count range.

Select reference writing for contribution, clarity, evidence handling where applicable, and effectiveness in its own form. Keep why the author values a piece as part of its record. Reach, awards, and citations can help find candidates; they do not by themselves define the desired writing qualities.

Preserve diverse successful patterns within a coherent reference group. Keep author, outlet, topic, era, and pattern identifiers so variation can be examined. Do not use the desired sentence or paragraph lengths as the admission criterion and then report the resulting lengths as an independent discovery.

When a distribution contains distinct patterns, show their profiles separately. A concise case-led explainer and an extended mechanism-led explainer can both be valuable examples. Their combined median should not become a compulsory third shape. Test candidate profiles on held-out authors or outlets where practical before treating their ranges as transferable.

This approach makes the conventions explicit while leaving room for the author's contribution and deliberate departures. The accepted nine features describe the writing; they are not an automatic scoring system for whether it is worth reading.
