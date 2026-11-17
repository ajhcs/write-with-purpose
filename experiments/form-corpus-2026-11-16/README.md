# First acquisition and measurement pass across seventeen forms

This experiment responds to the author's request to begin examining several hundred influential, notable, or commonly published examples in each proposed form. The user selected all seventeen forms and explicitly requested GPT-6.1 Terra subagents, up to ten. Nine Terra agents have disjoint ownership; the parent integrates and audits their outputs.

See the [completed first-pass overview](overview.md) for actual per-form coverage, shortfalls, corrections and the historical library-retrieval queue. Several hundred candidates were measured in multiple forms; no claim is made that all seventeen now have several hundred verified exemplars.

## Scope and evidence contract

The working target is at least 200 examples per form (300 for the dedicated systematic-review branch). This is an acquisition budget, not a statistical power calculation or an established writing norm. Report shortfalls explicitly rather than substituting unlike documents.

The family names and form inventory are provisional. Preserve source-provided type, proposed form, classification basis and uncertainty. A publisher label, title match or directory name alone does not certify our form assignment. A broad discovery query is not a collection of eligible writing exemplars.

Keep these stages visible:

1. **Discovered:** metadata records matching a stated search or source collection.
2. **Retrieved:** complete source material was obtained through an appropriate endpoint.
3. **Machine screened:** explicit type/structure/content conditions were applied; this is still provisional classification.
4. **Measured:** the stated body extraction and numerical policy were applied successfully.
5. **Editorially reviewed:** a person/model actually examined stated examples; identify which and who reviewed them.

A record can have measurements while its genre remains uncertain. Counts of measured candidates are not counts of verified examples of a form. Do not sum overlapping document records as independent texts.

## Source selection

Use actual citation counts with their provider, query, ranking scope and retrieval time where available. Raw citation order is a discovery signal and is sensitive to field and age. Retractions/corrections and mislabeled records need screening. Do not call the result the globally most-cited writing in a form.

For documentation and literary/nonacademic writing, distinguish maintained official publication, editorial selection, awards and actual scoped readership metrics. GitHub stars, platform reputation and presence in an archive are not page-level readership. Missing citation/readership data remains missing. “Most written” requires an explicit population and prevalence counts; this selected sample cannot establish global prevalence.

Pre-2015 research was preferred in the earlier literature search. It is not an automatic cutoff on this collection. Preserve publication/version dates and analyze era explicitly. Access time or current documentation text does not establish historical wording.

## Measurements and limits

Use the [nine accepted features](../../docs/writing-harness/accepted-foundations.md). Automated measurement may cover body length, heading structure, section proportions, paragraph and sentence shapes, word-length signals and evidence/presentation objects. State exactly how abstracts, reference lists, captions, tables, code, lists, inline markup, nested paragraphs and sentence boundaries are treated.

Each branch records its parser/counting policy. Branch outputs are **not automatically compatible**: differences in body selection, nested XML handling, markup parsing and sentence splitting can change counts. No cross-branch pooled distributions should be used as profiles before harmonization.

F09 rhetorical-function adequacy, factual support, intended-reader knowledge, originality and voice are not established by mechanical counts. Published high-citation/popularity patterns are descriptive, not causes of writing success. Observed ranges must remain separate from working targets and declared limits. Preserve multiple patterns within forms.

Original source caches stay outside the repository on the verified `/workspace` volume. The repository retains acquisition scripts, source metadata, hashes, derived measurements and reports. Rights/access conditions remain source-specific.

## Ownership

| Directory | Assigned forms |
| --- | --- |
| `essays/` | Personal/reflective essay; argument/perspective |
| `critical-theory/` | Critical review of a work; theory/conceptual paper |
| `explanation-tutorial/` | Conceptual explainer; tutorial |
| `procedure-reference/` | How-to/procedure; reference |
| `empirical-methods/` | Empirical research report; methods paper |
| `case-protocol/` | Case report; study or review protocol |
| `narrative-scoping/` | Narrative/critical literature review; scoping review |
| `systematic-review/` | Systematic review, preserving quantitative-synthesis status separately |
| `proposal-memo/` | Proposal; decision memo |

README and manual remain composite document types and are not extra forms in this count. Machine-derived data and agent source reviews are an initial research pass; author acceptance and human reader evaluation remain separate.

## Historical and library-access steering

During acquisition the author explicitly preferred pre-2015 work, with pre-2020 as an additional possibility, and offered broad library access. The original current-source discoveries are retained as exploratory cohorts. Branch reports distinguish pre-2015, 2015–2019, later, and unknown dates where available. Metadata year, first-online date, source version and retrieval date are different records.

The [library discovery guide](../../docs/writing-harness/research/library-discovery-guide.md) connects category-specific ranking/selection resources to a DOI-based retrieval queue. The queue's access flags are provider metadata, not a determination of entitlement or absence from every archive. Obvious type conflicts should be held before retrieval priorities are presented.
