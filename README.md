# Write with Purpose

Two Codex skills for clear meaning, useful structure and the author's voice. The language guidance applies across technical explanations, engineering documents, medical writing, assignments, essays and blogs.

| Skill | Use |
| --- | --- |
| [write-with-purpose](skills/write-with-purpose/SKILL.md) | Draft or substantially rework prose. Select the contribution, connect the reasoning and make a distinct reader edit. |
| [edit-with-purpose](skills/edit-with-purpose/SKILL.md) | Edit the existing wording through targeted word, clause and sentence changes. Preserve unaffected language and check revised meaning against supplied evidence. |

The instructions favor familiar, exact words, stable concept names and syntax that makes relationships clear. Numbers stay attached to their entities, units and conditions. Qualifications belong with the claims they limit. Explanations, punctuation and paragraph boundaries should help the reader follow the thought.

Conformance, correctness and usefulness are assessed separately. Meeting a specification does not establish factual accuracy; preserving facts does not establish reader benefit. Source fidelity and factual validation also require separate judgments.

Each skill loads supporting references only when they address the current issue. The package contains no bundled writing samples, mandatory prose template, word blacklist or automatic editing hook. An independent pass uses a fresh context when requested and available; the skill name alone does not establish independence.

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

It reports exact duplicate paragraphs, explicit unresolved markers, limited internal Markdown-anchor discrepancies and numeric-token differences. An optional contract can check required literals. It never edits files. Exit 0 means the assessment ran, including when it found observations; exit 2 means an input or invocation failure.

These checks do not judge factual correctness, useful repetition, paragraph flow or reader benefit. See [the checker reference](skills/write-with-purpose/references/checks.md) for its exact scope.

## Targeted edits and concision

Editing a paragraph means inspecting it as a whole and repairing particular parts. The editor first considers deletions, then makes the smallest changes that resolve the identified problem. Connections can require coordinated changes to adjacent sentences. Substantial rewriting follows an explicit request or a demonstrated organizational problem.

For file edits, an exact-span plan can bind the changes to the source hash and reconstruct a separate output while preserving everything outside the named spans:

```text
python skills/edit-with-purpose/scripts/edit_locally.py original.txt --plan edits.json --output edited.txt
python skills/edit-with-purpose/scripts/edit_locally.py original.txt --compare existing-edit.txt
```

The receipt records before/after word counts, inserted and removed tokens, and the original text selected by the plan. It makes expansion and broad replacement visible. It does not enforce a reduction quota or certify source meaning. See [local edits](skills/edit-with-purpose/references/local-edits.md).

## Grammar-checking investigation

A separate [research harness](experiments/grammar/probe.mjs) tests a pinned local grammar engine. It demonstrates useful spelling and punctuation findings, missed syntax problems and technical-vocabulary false positives. It is not installed as an automatic correction service. See [findings and sources](docs/grammar-investigation.md).

## Validation and design

```text
python -m unittest discover -s tests -v
```

The release includes 37 behavioral tests: 20 for the original checker and 17 for exact local edits and change measurement. Earlier skill instructions also received separate conformance, source-fidelity and reader reviews; results were mixed. See [evaluation and limits](docs/evaluation.md).

This package follows [OpenAI's skill guidance](https://learn.chatgpt.com/docs/build-skills) and [portable plugin structure](https://developers.openai.com/plugins/build/plugins). Repository and release documentation stay outside the skill entrypoints. Publishing this repository does not list it in the OpenAI plugin directory.

Package version: **0.5.0**. Writer **0.3.2**, editor **0.2.0**, advisory checker **0.1.0**, local-edit tool **0.1.0**. The grammar engine is an isolated experiment, not a skill dependency or installed hook.
