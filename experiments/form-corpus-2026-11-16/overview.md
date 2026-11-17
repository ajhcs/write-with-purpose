# Seventeen-form acquisition: completed first pass

Nine GPT-6.1 Terra subagents performed separate acquisition/measurement tasks; the parent checked reports and records and commissioned a bounded cross-branch audit. The request was to begin identifying structural and language characteristics from several hundred notable/influential/common works per form. This pass advances that request but **does not establish 200 verified exemplary works in every form**, representative genre distributions, or adopted writing profiles.

**Domain correction:** the scholarly acquisition below is predominantly medical/health research, while documentation is predominantly software. The author explicitly requested business, engineering, law and personal writing. The [cross-domain expansion](domain-expansion/README.md) adds historical retrieval candidates; the [sampling note](../../docs/writing-harness/research/cross-domain-sampling.md) explains how to keep context, form, audience and era distinct. The original biomedical library queue must not be used as a project-wide default selection.

## Actual coverage

Numbers below are branch-specific records and must not be added into a unique corpus total. Source collections and forms can overlap. Machine screening, mechanical measurement and editorial suitability are distinct. Linked reports contain the distribution tables and exact policies.

| Family | Proposed form | Actual measured/screened coverage | Principal limit |
| --- | --- | --- | --- |
| Essays/commentary | Personal/reflective essay | [2 provisionally reviewed examples](essays/summary.md); 221 mixed-form single-author extracts and 297 indexed narrative bodies available | Only two have a provisional form decision; indexing demonstrably misclassifies some articles |
| Essays/commentary | Argument/perspective | [2 provisionally reviewed examples](essays/summary.md); same single-author pool and 293 indexed editorial bodies available | Shared author pool is not an additional independent collection or a source of general argument norms |
| Essays/commentary | Critical review of a work | [67 source-label/product-identified reviews](critical-theory/summary.md) | Mainly scientific/medical book reviews; little coverage of literary/art/film criticism |
| Explanation/docs | Conceptual explainer | [222 source-typed candidates](explanation-tutorial/summary.md) with approximate source measurements | Two software-documentation projects; source includes/templates not rendered |
| Explanation/docs | Tutorial | [247 source-typed candidates](explanation-tutorial/summary.md) with approximate source measurements | Current software/ML/robotics sources; page purpose unaudited and formats differ |
| Explanation/docs | How-to/procedure | [222 mechanically measured/title-screened pages](procedure-reference/summary.md) | Four software projects; page-by-page reader-task confirmation outstanding |
| Explanation/docs | Reference | [216 mechanically measured/title-screened pages](procedure-reference/summary.md) | Same four-project ecosystem; no page-readership ranking |
| Research reports | Empirical report | [200 machine-screened measured reports](empirical-methods/summary.md) | Pre-2015 medical randomized trials only |
| Research reports | Methods paper | [200 machine-screened measured papers](empirical-methods/summary.md) | One journal, MethodsX; 15 through 2014, 82 in 2015–2019, 103 later |
| Research reports | Theory/conceptual paper | [22 source-label-screened measurements](critical-theory/summary.md), in two distinct collections | Mainly psychology; cannot infer form from conceptual title matches alone |
| Research reports | Case report | [200 primary indexed candidates](case-protocol/summary.md), of which 31 have matching JATS case-report type | Publisher/index labels disagree; additional attempts/supplements are recorded separately |
| Research reports | Study/review protocol | [200 study and 200 review-protocol title candidates](case-protocol/summary.md) | These are strata of one proposed form, not two extra forms; prospective intent unresolved |
| Evidence syntheses | Narrative/critical literature review | [336 distinct measured candidate records](narrative-scoping/summary.md) across overlapping exploratory/historical samples | Biomedical title-based screen, not broader critical synthesis; dates need source-basis care |
| Evidence syntheses | Scoping review | [313 distinct measured candidate records](narrative-scoping/summary.md) across overlapping samples | Same narrow indexing and title constraints; limited pre-2015 coverage |
| Evidence syntheses | Systematic review | [300 distinct measured candidates](systematic-review/summary.md), including 112 before 2015 | Automated title/search/eligibility-method signals; not full semantic eligibility review |
| Proposals/decisions | Proposal | [5 discovered leads; 0 measured/confirmed complete](proposal-memo/summary.md) | Accessible full narratives scarce; available PDFs lack a local extractor; no abstract substitution |
| Proposals/decisions | Decision memo | [6 selected published primary transcriptions measured](proposal-memo/summary.md) | Historical US foreign-policy setting only; attachments/redactions not complete original packages |

The case/protocol branch also retains a separate 161-measurement pre-2015 supplement and quota-overflow attempts. The narrative/scoping branch preserves both the original and historical-query cohorts and their overlap. Keep their reported selection units rather than pooling all rows.

## What the measurements begin to reveal

The scripts record body-word counts, headings/sections, paragraph lengths, heuristic sentence lengths, character lengths, and evidence/presentation objects where the source representation supports them. Section-level arrays make it possible to examine relative allocation instead of only total length. Several branch reports give document-level distributions and era-specific tables.

There is already clear evidence that discovery labels require examination: highly cited research appeared under book-review indexing, a systematic review appeared under personal narrative indexing, and protocol titles alone did not establish prospective work. Full-text structure improves triage without replacing a reader's assessment.

These data do not yet support direct comparisons of median lengths across all forms. Prose/list/code inclusion, administrative-section removal, headings, sentence splitting, source formats and document units differ. Source-typed documentation measurements are partial source extractions; empirical/review measurements use structured XML; literary extraction has incomplete-body uncertainty. Some branches pool paragraph observations, while others weight each article's median equally. All of this must be harmonized before author-facing ranges are derived.

The current software documentation is retained as a contemporary exploratory cohort. It is not evidence about historical wording. Historical research reports and citation metadata can address the preferred older periods, while library access can fill important omissions in the public-source collections.

## Library and notable-work selection

The [library queue](library-queue/README.md) preserves **400 DOI discovery records**, then holds 26 known or precautionary type conflicts. The remaining **374 unheld provisional candidates** comprise **186 with first-publication dates through 2014** and **188 from 2015–2019**. The [275-item library-first CSV](library-queue/library-first.csv) comprises unheld records whose Europe PMC metadata says `inPMC=N`; 147 have first-publication dates through 2014. All entries in the original queue have the provider's `isOpenAccess=N` flag. Neither flag establishes paywall status, absence from every archive, library entitlement or actual form eligibility.

The [DOI shortlist](library-queue/shortlist.md) excludes holds and shows both indexed year and first-publication date. Citations are ranked within the recorded Europe PMC query/period, not normalized across fields or equivalent to Web of Science/Scopus counts. The queue does not claim confirmed exemplar quality. No article bodies from this queue have been retrieved.

Additional leads: [600 pre-2015 criticism/theory records](critical-theory/summary.md) from three named periodicals and [467 Longform-linked essay candidates](essays/summary.md), 305 with displayed pre-2015 dates. These are discovery pools, not additional verified or necessarily unique works. The [library discovery guide](../../docs/writing-harness/research/library-discovery-guide.md) connects scholarly citation resources, historical editorial lists, ASME/Pulitzer selections, annual essay anthologies and scoped readership resources to the relevant forms.

Start retrieval with a small diverse historical batch to establish form and extraction boundaries, then expand the screened strata. Broad library access allows selecting works by purpose and documented influence rather than accepting access availability as an eligibility rule.

## Independent checks and corrections

The [Terra cross-branch audit](explanation-tutorial/cross-branch-audit.md) records concrete samples and limits. It is a spot audit rather than a corpus-wide error estimate. Findings prompted these corrections:

- Empirical/methods durable rows now include source hashes and retrieval/citation snapshots. Administrative body sections are removed through an explicit heading screen and retained as excluded counts. The sampled PMC1904193 changed from 2,696 to 2,580 words, accounting for 116 administrative words.
- Narrative/scoping rows now retain source hashes and date-basis qualifications. Administrative sections are excluded; the sampled PMC10954893 changed from 10,856 to 10,697 words, accounting for 159 administrative words.
- Procedure/reference JSONL rows now persist the final inclusion flag, title-screen status and exclusion reason. Their aggregates read these flags; mechanical acceptance alone is not final inclusion.
- Obvious and precautionary library type conflicts are held and excluded from retrieval-priority exports and the shortlist. The complete 400-row discovery record remains intact.

Some provenance and measurement qualifications remain. Critical/theory fingerprints are extracted-text hashes rather than raw XML hashes; raw source was not retained in that branch. Procedure/reference records hash HTML but do not retain source HTML for readback. Record completion order is not citation rank. Sentence and paragraph boundaries need targeted validation, and semantic paragraph functions remain unassessed.

The parent additionally parsed saved machine-readable artifacts, checked reported counts against records, inspected source-cache examples and link/whitespace consistency, and verified that the held queue records are absent from retrieval CSVs. These bounded checks do not establish form correctness, representative sampling, human-reader benefit or writing quality.
