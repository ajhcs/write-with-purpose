# Write with Purpose

Two Codex skills for clear meaning, useful structure and the author's voice. The language guidance applies across technical explanations, engineering documents, medical writing, assignments, essays and blogs.

| Skill | Use |
| --- | --- |
| [write-with-purpose](skills/write-with-purpose/SKILL.md) | Draft or substantially rework prose. Select the contribution, connect the reasoning and make a distinct reader edit. |
| [edit-with-purpose](skills/edit-with-purpose/SKILL.md) | Review an existing draft. Compare concrete revisions, preserve effective writing and check the revised meaning against supplied evidence. |

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

## Validation and design

```text
python -m unittest discover -s tests -v
```

The release includes 20 behavioral tests for the checker. The skill instructions also received separate conformance, source-fidelity and reader reviews; results were mixed. See [evaluation and limits](docs/evaluation.md).

This package follows [OpenAI's skill guidance](https://learn.chatgpt.com/docs/build-skills) and [portable plugin structure](https://developers.openai.com/plugins/build/plugins). Repository and release documentation stay outside the skill entrypoints. Publishing this repository does not list it in the OpenAI plugin directory.

Package version: **0.4.0**. Runtime instructions retain writer **0.3.2** and editor **0.1.1**; this combined release normalizes line endings and adds publication, installation and test documentation.
