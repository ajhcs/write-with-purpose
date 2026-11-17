# Write with Purpose

Two Codex skills for clear meaning, useful structure and the author's voice. The language guidance applies across technical explanations, engineering documents, medical writing, assignments, essays and blogs.

| Skill | Use |
| --- | --- |
| [write-with-purpose](skills/write-with-purpose/SKILL.md) | Draft or substantially rework prose. Develop the author's contribution, connect the reasoning and make a distinct reader edit. |
| [edit-with-purpose](skills/edit-with-purpose/SKILL.md) | Correct, polish or substantively improve existing prose according to the request. Preserve effective choices while carrying worthwhile improvements into the actual text. |

The instructions favor familiar, exact words, stable concept names and syntax that makes relationships clear. Numbers stay attached to their entities, units and conditions. Qualifications belong with the claims they limit. Explanations, punctuation and paragraph boundaries should help the reader follow the thought.

Conformance, correctness and usefulness are assessed separately. Meeting a specification does not establish factual accuracy; preserving facts does not establish reader benefit. Source fidelity and factual validation also require separate judgments.

Each skill loads supporting references only when they address the current issue. The editor includes worked examples of simplifying generated prose, a user-approved one-word correction, and a reader rewrite that adds context and joins related thoughts. Both skills use preferred author wording to guide style; lower word counts and shorter sentences are not acceptance criteria by themselves. The package has no mandatory prose template, word blacklist or automatic editing hook. An independent pass uses a fresh context when requested and available; the skill name alone does not establish independence.

For Cole Lyons's prose, both skills load [his approved style reference](skills/edit-with-purpose/references/cole-lyons-style.md). It includes the accepted patient-safety passage, explains the choices to carry forward, and links to the complete approved revision. Each skill includes its own copy of these two references so it can be installed independently; keep the paired copies identical. These author preferences apply unless the current brief asks for a different voice.

## Install for all your projects

Ask Codex:

```text
Use $skill-installer to install skills/write-with-purpose and
skills/edit-with-purpose from ajhcs/write-with-purpose into
~/.agents/skills for the current user.
```

Use one global copy of each skill. If you already have these skills in a legacy location, preserve that copy before replacing or moving it. The installed skills are available on your next turn.

Invoke either skill explicitly when useful:

```text
Use $write-with-purpose to draft this explanation from my notes.
Use $edit-with-purpose to review this draft and preserve the parts that work.
```

## Optional mechanical checker

The writer includes a Python 3 checker using only the standard library:

```text
python skills/write-with-purpose/scripts/check_text.py draft.md
python skills/write-with-purpose/scripts/check_text.py draft.md --source source.md
```

It reports exact duplicate paragraphs, explicit unresolved markers, limited internal Markdown-anchor discrepancies and numeric-token differences. An optional contract can check required literals, an absolute word ceiling, and growth relative to the original draft. It never edits files. By default, exit 0 means the assessment ran, including when it found observations. With `--enforce-contract`, violated declared literals or word limits exit 1. Exit 2 means an input or invocation failure; other observations remain advisory.

These checks do not judge factual correctness, useful repetition, paragraph flow or reader benefit. See [the checker reference](skills/write-with-purpose/references/checks.md) for its exact scope.

## Revision depth and file edits

Infer the depth from the actual request and context. A correction-only request stays narrow. A request to improve the work prompts a search for better reasoning, organization or expression even when the existing prose is adequate; it need not wait for a local repair to fail. A satisfactory original can still stand after comparison. Neither the number of changed words nor the amount of rewriting scores quality.

The four core rules guide depth and whole-work review, author-owned thought development, concrete comparison of consequential alternatives, and investigation of ambiguity according to the deliverable. A model-proposed interpretation is not an accepted author belief. Ordinary editing need not settle every function label; requested annotation research must investigate its relevant disagreements even if no prose change follows. Explanations and practice follow the author's chosen learning task, including direct delivery of a requested worked solution.

For file edits, an exact-span plan can bind the changes to the source hash and reconstruct a separate output while preserving everything outside the named spans:

```text
python skills/edit-with-purpose/scripts/edit_locally.py original.txt --plan edits.json --output edited.txt
python skills/edit-with-purpose/scripts/edit_locally.py original.txt --compare existing-edit.txt
```

The receipt records before/after word counts, inserted and removed tokens, and the original text selected by the plan. It makes expansion and broad replacement visible. It does not enforce a reduction quota or certify source meaning. See [local edits](skills/edit-with-purpose/references/local-edits.md).

Use actual task constraints for code checks. Verify the final scoped body, and rerun a check after an edit makes its receipt stale. Mechanical compliance, source fidelity, voice and usefulness require separate assessments; an instruction to run a checker is not an automatic hook.

## Grammar-checking investigation

A separate [research harness](experiments/grammar/probe.mjs) tests a pinned local grammar engine. A subsequent [paired comparison and fresh editor evaluation](docs/editor-language-comparison.md) covers LanguageTool 6.6, harper.js 3.0.0 and six new editing passages. The records include every before/after, exact edit plan and separate conformance, correctness and usefulness assessment.

LanguageTool flagged 12 of 16 premarked error locations, compared with Harper's nine, on 27 small fixtures. Both repeated their normalized findings across three fresh processes, and both missed errors. The comparison favors LanguageTool for the next diagnostic integration trial, with domain vocabulary and reviewed replacements. Neither engine is an installed skill dependency or automatic correction service. See [findings and sources](docs/grammar-investigation.md).

## Validation and design

The proposed writing harness has a durable [record of accepted foundations](docs/writing-harness/accepted-foundations.md): nine measurement features, the Family → Form → Section hierarchy, observed ranges versus working targets and declared limits, and criteria for keeping reference categories useful. These are design decisions; the measured profiles and form-specific runtime are not implemented yet.

An [initial paragraph-function catalogue](docs/writing-harness/paragraph-functions.md) adds twelve proposed functions, form/section examples, and a [pre-2015 research register](docs/writing-harness/research/pre-2015-writing-evidence.md). A separate [annotation experiment](experiments/paragraph-functions/README.md) checks source spans, registered labels and references, and declared paragraph limits. It does not classify prose or certify editorial quality, and is not installed as a skill dependency.

The [cross-domain genre research and corpus plan](docs/writing-harness/research/genre-synthesis-and-corpus-plan.md) examines existing syntheses and classifications, records an Astra review, and links acquired metadata for 13,053 Longform discovery posts and 393 research-dataset README candidates. These inventories have not yet been screened as writing exemplars.

A [seventeen-form acquisition and measurement pass](experiments/form-corpus-2026-11-16/overview.md) records actual candidate measurements, per-form shortfalls, source/era limitations and independent spot-check corrections. Its [historical library queue](experiments/form-corpus-2026-11-16/library-queue/README.md) and [discovery guide](docs/writing-harness/research/library-discovery-guide.md) support finding influential and editorially selected work beyond open-access collections. These remain research data, not adopted writing profiles or numerical limits.

The [nonmedical discovery expansion](experiments/form-corpus-2026-11-16/domain-expansion/README.md) adds historical business, engineering, law and personal/public-writing leads. Its combined CSV preserves source groups and unresolved forms; it is a library-discovery inventory, not an additional measured or validated corpus.

The [available-copy retrieval results](experiments/form-corpus-2026-11-16/fulltext-retrieval/summary.md) index local source files, identity/completeness checks, unresolved access and a library-import queue. Raw source files and text-layer sidecars stay outside Git on `/workspace`; candidate copies are not yet validated writing exemplars.

The [first common analysis of collected sources](experiments/corpus-analysis-2026-11-16/report.md) reprocesses retained XML, documentation, HTML and PDFs, reviews seventeen additional uploads, and records exploratory distributions, source-bound paragraph-function samples and independent audits. A separate register preserves earlier measurements whose source bytes were not retained. These observations are not adopted writing targets or validated form profiles.

A [held-out test of the three example patterns](experiments/pattern-test-2026-11-16/report.md) adds 19 fully coded texts, 680 prose paragraphs, observed section/function lengths and a second coding of 138 paragraphs. It separates publisher categories, proposed forms and procedure/tool boundary cases, and preserves substantial coding disagreement. Its revised blank templates remain proposals, with working targets and declared limits unset.

The [saved work index](docs/writing-harness/work-index.md) links the source-grounded disagreement review, [Astra's candidate rule revision](docs/writing-harness/research/astra-rule-revision-2026-11-16.md) and its independent audit. The [library expansion](experiments/library-expansion-2026-11-16/README.md) assesses all seventeen forms across six source groups and exports 214 primary retrieval targets, including 154 DOIs, with conditional examples, source evidence and gaps kept separate. The earlier [coding-rule pilot](experiments/rule-calibration-2026-11-16/report.md) did not demonstrate improved agreement; later canonical skill work preserves that finding.

The [canonical implementation and rerun](experiments/canonical-skill-revision-2026-11-16/report.md) integrates the four adjudicated rules, proportional depth selection, conditional function guidance and scoped code-check instructions into both skills. The final source passes 47 Python tests, 15 annotation-prototype tests and both skill validators. An initial twelve-task masked comparison was mostly ties and exposed learning/delivery issues; the report preserves those outputs, narrow fixes and final focused retests. These are development observations, not demonstrated writing superiority. Global installations remain separate.

The [two-Astra debate](experiments/author-feedback-debate-2026-11-16/report.md) preserves independent positions, challenges and exact acceptance of three reference refinements. Those refinements are now implemented in the canonical skills; the debate files remain as-at-decision records. [Alpha.7 implementation and preservation notes](docs/releases/0.6.0-alpha.7.md) distinguish shipped guidance, exploratory coding rules, local source caches and proposed future tests.

```text
python -m unittest discover -s tests -v
```

The previous release included 37 behavioral tests: 20 for the original checker and 17 for exact local edits and change measurement. Six fresh editing contexts tested editor 0.2.0 on new engineering, medical, assignment and blog passages, including two concise controls. Fresh masked readers preferred the five finals that changed; the unchanged control tied. A separate source audit records corrected errors and residual limitations. These are small model-reviewed trials, not human acceptance or a matched no-skill comparison. Earlier reviews were mixed; see [evaluation and limits](docs/evaluation.md).

This package follows [OpenAI's skill guidance](https://learn.chatgpt.com/docs/build-skills) and [portable plugin structure](https://developers.openai.com/plugins/build/plugins). Repository and release documentation stay outside the skill entrypoints. Publishing this repository does not list it in the OpenAI plugin directory.

Candidate package **0.6.0-alpha.7**: writer **0.4.0-alpha.7**, editor **0.3.0-alpha.7**, checker **0.2.0**, local-edit tool **0.1.0**. Alpha.6 implemented the four core rules for development, editing and improvement. Alpha.7 applies the three author-review refinements: Cole-specific illustrative-list preferences, comparison of progression in context, and grounded personal history and author-corrected disclaimers. Scripts are unchanged; the research and coding artifacts are preserved alongside the skills. Alpha.5 narrowed cleanup routing, treated illustrative lists as selections, replaced obscure phrasing with supported actions, learned from preferred author rewrites, provided worked editing examples, an author-approved article reference and optional task briefs, and added opt-in enforcement of declared word limits. Its ten additional checker tests remain in the suite. The earlier model evaluations above describe package 0.5.1. The author reference records Cole's acceptance of one revised article; it does not establish style fit for every future output. The grammar engines remain isolated experiments, not skill dependencies or installed hooks.
