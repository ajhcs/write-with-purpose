# Write with Purpose

Write with Purpose helps you develop an idea or revise a draft for the people who will read it. Both Codex skills check whether the finished text makes the author's point and whether the evidence and qualifications still support it.

| Skill | When to use it |
| --- | --- |
| [write-with-purpose](skills/write-with-purpose/SKILL.md) | Draft from notes, develop an unsettled idea, or make a substantial rewrite. |
| [edit-with-purpose](skills/edit-with-purpose/SKILL.md) | Correct, polish, or improve an existing draft at the depth the request allows. |

The package includes optional Python helpers for checking declared constraints and applying reproducible file edits. This repository also holds the research toward a broader writing harness, including experiments on document forms and paragraph functions.

The latest documented release is 0.6.0-alpha.7. [Implementation and preservation notes](docs/releases/0.6.0-alpha.7.md)

## Install

Ask Codex:

```text
Use $skill-installer to install skills/write-with-purpose and
skills/edit-with-purpose from ajhcs/write-with-purpose into
~/.agents/skills for the current user.
If either is already installed, preserve the old copy before replacing it.
```

The skills are available on your next turn. Each can be installed independently; keep one user-wide copy of each to avoid competing versions. The helpers require Python 3 and use only its standard library.

## Describe the writing you want to review

Give Codex the material, the intended reader, and what you want the reader to understand or do. Say how you'll judge the result and name any binding limits, required wording, or fixed section order. Give Codex room to make editorial choices within those constraints. [Prompting GPT-6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra)

**Draft an explanation**

```text
Use $write-with-purpose to turn these notes into an explanation for
clinic managers who are new to our scheduling export. A manager should
be able to tell which records the export includes and when to check
the original schedule. Use only the supplied notes and keep the body
under 250 words.
```

**Improve an existing piece**

```text
Use $edit-with-purpose to strengthen this recommendation for a review
committee. A committee member should be able to say what I propose,
what evidence supports it, and what would change my recommendation.
Preserve my position and keep each qualification with the claim it limits.
```

**Learn from an edit**

```text
Use $edit-with-purpose to revise this paragraph, then explain one important
choice. Give me a fresh passage to practise the same decision, and let me
attempt it before showing a solution.
```

A punctuation-only request stays local. For a substantial review, name the question that deserves deeper reasoning, such as why two sources differ or which condition would change a recommendation. Use Medium for a quick survey, High for a contested issue that spans several sources, and consider Extra High when several issues interact. On work that splits cleanly, ask Codex to use subagents as needed for independent source questions or a fresh reader review. [Reasoning effort and parallel work](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra#match-reasoning-effort-to-the-task)

For a rendered report or handout, share a sample layout and specify where it will be read. Tell Codex what must remain legible at that size and which links or controls a reader needs to use. Ask it to inspect the export and correct any problems it finds. Reserve project instructions in `AGENTS.md` for conventions a future task would need, such as controlled terminology or a required reporting template.

## How the skills approach the work

Both skills use the brief to decide which editorial checks matter.

| Rule | What it means in practice |
| --- | --- |
| Scope | Make the specified correction or look across the whole piece for improvements when the brief opens up the reasoning or structure. |
| Author's contribution | Build from the author's position and actual reasons. A new interpretation stays provisional until the author adopts it. |
| Consequential changes | Compare the actual passage in context and see what a reader can understand or do after the change. |
| Ambiguity | Resolve competing readings when they change a claim or action. In an annotation study, retain relevant disagreements for investigation. |

The supporting references make these decisions more concrete. For example, saying that an author *still needs* to check a result can lose an earlier explanation of why faster output makes those checks more valuable. A smoother sentence can preserve the duty while weakening the argument.

Read the final prose as a whole and review source fidelity, factual support, and declared limits. An argument can be memorable after reading a report even if the author first encountered it elsewhere. The rewrite can preserve that distinction while keeping useful changes.

## Work in the author's voice

Cole Lyons's profile draws on an approved article and subsequent author feedback, including a comparison with his posted interoperability response. It favors enough context to follow the thought and examples that develop the argument. Required coverage takes priority over a preference for short illustrative lists. [Cole Lyons's style reference](skills/write-with-purpose/references/cole-lyons-style.md)

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

That feedback led to the three reference refinements documented in alpha.7. [Two-Astra review](experiments/author-feedback-debate-2026-11-16/report.md)

The paragraph-coding pilot did not demonstrate better agreement after a rule revision. [Paragraph-coding pilot](experiments/rule-calibration-2026-11-16/report.md)

Earlier [editing evaluations](docs/evaluation.md) and the [grammar-engine investigation](docs/grammar-investigation.md) document their own methods and limitations. The investigated grammar engines are separate experiments, not installed skill dependencies.

## Development

Run the portable suites from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s experiments/paragraph-functions -p 'test_*.py' -v
python3 -m unittest discover -s experiments/corpus-analysis-2026-11-16/tests -v
python3 -m unittest discover -s experiments/rule-calibration-2026-11-16/analysis -p 'test_*.py' -v
```

The 74 tests cover the helpers and research contracts. CI runs those suites on Linux and Windows. Assess author preference and writing quality using the delivered prose.

The canonical instructions live in `skills/`. Keep the shared author and structure references identical across both skills so either remains independently installable. Research snapshots preserve the rules and outputs used at each stage; make new revisions in the canonical sources and retain the original experimental records.
