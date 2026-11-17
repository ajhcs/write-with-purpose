# Write with Purpose

Write with Purpose helps you develop an idea and express it clearly while keeping your own point of view. It provides two Codex skills that work on the reasoning behind a piece as well as its wording.

| Skill | When to use it |
| --- | --- |
| [write-with-purpose](skills/write-with-purpose/SKILL.md) | Draft from notes, develop an unsettled idea, or make a substantial rewrite. |
| [edit-with-purpose](skills/edit-with-purpose/SKILL.md) | Correct, polish, or improve an existing draft at the depth the request allows. |

The package includes optional Python helpers for checking declared constraints and applying reproducible file edits. This repository also holds the research toward a broader writing harness, including experiments on document forms and paragraph functions.

**Current package:** 0.6.0-alpha.7. See the [implementation and preservation notes](docs/releases/0.6.0-alpha.7.md).

## Install

Ask Codex:

```text
Use $skill-installer to install skills/write-with-purpose and
skills/edit-with-purpose from ajhcs/write-with-purpose into
~/.agents/skills for the current user.
If either is already installed, preserve the old copy before replacing it.
```

The skills are available on your next turn. Each can be installed independently; keep one user-wide copy of each to avoid competing versions. The helpers require Python 3 and use only its standard library.

## Start with the writing you need

Give Codex the material and enough context to understand what the reader needs. Name a length limit when one applies. If a particular phrase or section order must stay, say so; otherwise leave room for a better arrangement.

**Draft an explanation**

```text
Use $write-with-purpose to turn these notes into a technical explainer.
The reader understands the workflow but is new to the software.
Introduce the technical terms they need to follow the explanation.
```

**Improve an existing piece**

```text
Use $edit-with-purpose to improve this essay.
Look for a stronger argument or arrangement while preserving my position.
Keep the qualifications that affect what I am claiming.
```

**Learn from an edit**

```text
Use $edit-with-purpose to revise this paragraph, then explain one important
choice. Give me a fresh passage to practise the same decision, and let me
attempt it before showing a solution.
```

A punctuation-only request stays local. An improvement request can justify rethinking an adequate passage, including its structure. The skills can also retain an effective original when the alternative loses something important.

## How the skills approach the work

Both skills share four rules:

| Rule | What it means in practice |
| --- | --- |
| Choose the depth that serves the request | Read the relevant whole and look for a worthwhile improvement. A broader revision can be the first useful approach. |
| Develop the author's contribution | Distinguish what the author has stated from a supported connection or a new editorial interpretation. Keep an unadopted thesis provisional. |
| Compare consequential choices in actual prose | Write the transition or passage that makes a different arrangement assessable. Consider what the reader gains and what the revision might lose. |
| Investigate ambiguity to the depth needed | Examine competing readings when they could change the meaning or the edit. A requested annotation study must investigate its disagreements even when no revision follows. |

The supporting references make these decisions more concrete. For example, saying that an author *still needs* to check a result can lose an earlier explanation of why faster output makes those checks more valuable. A smoother sentence can preserve the duty while weakening the argument.

Source review is a separate part of the work. A claim that an argument stayed with someone after reading a report does not establish that they first encountered it there. An appealing rewrite can keep its useful changes while repairing that unsupported addition.

## Work in the author's voice

The package includes [Cole Lyons's style reference](skills/write-with-purpose/references/cole-lyons-style.md), grounded in an approved article and subsequent author feedback. It favors enough context to follow the thought and examples that develop the argument. Cole's preference against long illustrative lists belongs to his profile; required coverage still needs to survive.

For another author, supply their voice instructions and an approved sample when useful. The current brief controls the voice. A sample's structure can help explain a choice without importing its facts or repeating its wording. The [complete approved article](skills/write-with-purpose/references/cole-lyons-patient-safety.md) is preserved as a reference, with its provenance recorded.

## Use the optional helpers

These commands assume a repository checkout and Python 3. Use `python` in place of `python3` if that is how Python 3 is available on your system. Installing the skills does not register an automatic checking or rewriting hook.

### Check a draft

```sh
python3 skills/write-with-purpose/scripts/check_text.py draft.md --source original.md
```

The checker flags exact duplicate paragraphs and explicit unfinished markers. It also compares numeric tokens with the source and inspects simple internal Markdown links. Those observations help locate material to review; matching numbers alone cannot establish that a claim kept its meaning.

For a brief with a 250-word ceiling, save this as `contract.json`:

```json
{"max_words": 250}
```

Then enforce that declared limit:

```sh
python3 skills/write-with-purpose/scripts/check_text.py draft.md --contract contract.json --enforce-contract
```

Contracts can also require exact wording or limit growth relative to the original draft. Counts use whitespace-separated tokens in the raw file, including Markdown and code. The [checker reference](skills/write-with-purpose/references/checks.md) defines the supported contract and counting convention.

By default, exit 0 means the assessment ran, including when it found observations. In enforcement mode, a violated declared constraint returns 1. Invalid input or invocation returns 2. Findings outside the declared contract remain advisory; the helper leaves the draft unchanged.

### Apply or measure file edits

```sh
python3 skills/edit-with-purpose/scripts/edit_locally.py original.txt --plan edits.json --output revised.txt
python3 skills/edit-with-purpose/scripts/edit_locally.py original.txt --compare revised.txt
```

An edit plan binds exact spans to the original file's hash and writes a separate result. The tool refuses to overwrite the source or an existing output. Compare mode measures an already written revision. The [plan schema and worked instructions](skills/edit-with-purpose/references/local-edits.md) explain how to prepare the spans and read the change report.

Neither helper judges whether an argument is sound or whether the author would choose the revision. Those decisions still need a reading of the actual work.

## Research toward a writing harness

The research starts with **Family → Form → Section**: identify the writing's conventions, then examine what each part needs to accomplish. Paragraphs can perform several functions within that structure. A broad label such as “blog post” is insufficient to choose a useful outline or word budget.

The [accepted foundations](docs/writing-harness/accepted-foundations.md) define nine feature groups for describing writing. They also distinguish three kinds of measurement:

| Record | What it tells us |
| --- | --- |
| Observed range | What was measured in a specified collection of examples. |
| Working target | A budget or pattern chosen for the current piece. |
| Declared limit | An actual minimum or maximum set by the author, assignment, or destination. |

An observed median does not become the author's target. Different successful patterns within a form need to remain visible.

The repository contains a proposed twelve-function catalogue and exploratory acquisition work across seventeen forms. The [annotation prototype](experiments/paragraph-functions/README.md) checks supplied source spans and labels against its contract; it does not infer paragraph functions or certify their effectiveness. Form-specific profiles and a complete automated writing runtime remain under development.

The [research and coding index](docs/writing-harness/work-index.md) links the corpus measurements, disagreements and subsequent rule revisions. It also covers the existing datasets and codebooks examined for reuse. Raw full-text corpora remain outside Git; the saved records identify their provenance and local dependencies.

## What the evaluations show

In a [blinded author review](experiments/blind-longform-2026-11-16/review/unblinded-results.md), the alpha.6 writer was preferred in six rated passages, its baseline in three, and the original once. All ten judgments concern passage comparisons, and both rewrite conditions used the writer skill. They do not establish an editor result or a preference for complete rewritten works.

That feedback led to the [two-Astra debate](experiments/author-feedback-debate-2026-11-16/report.md) and the three reference refinements shipped in alpha.7. The updated package has not yet undergone a fresh writing comparison. Separately, the [paragraph-coding pilot](experiments/rule-calibration-2026-11-16/report.md) did not demonstrate better agreement after a rule revision; that finding remains part of the record.

Earlier [editing evaluations](docs/evaluation.md) and the [grammar-engine investigation](docs/grammar-investigation.md) document their own methods and limitations. The investigated grammar engines are separate experiments, not installed skill dependencies.

## Development

Run the portable suites from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s experiments/paragraph-functions -p 'test_*.py' -v
python3 -m unittest discover -s experiments/corpus-analysis-2026-11-16/tests -v
python3 -m unittest discover -s experiments/rule-calibration-2026-11-16/analysis -p 'test_*.py' -v
```

CI runs all 74 tests on Linux and Windows. They check the helpers and research contracts; author preference and writing quality are evaluated separately.

The canonical instructions live in `skills/`. Keep the shared author and structure references identical across both skills so either remains independently installable. Research snapshots preserve the rules and outputs used at each stage; make new revisions in the canonical sources and retain the original experimental records.
