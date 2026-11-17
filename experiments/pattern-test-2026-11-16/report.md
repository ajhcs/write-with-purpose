# Testing the three writing patterns on held-out sources

The pilot supports reusable section jobs and alternative ways of developing them. It does not support promoting the original examples into fixed paragraph sequences. It also exposes a measurement limit: independently assigning paragraph functions is appreciably less reproducible than counting words in a specified source span.

We inspected and fully coded **19 texts, containing 680 main-prose paragraphs**, excluding the three original development examples. A second model coder independently labeled **138 paragraphs** without seeing the first function labels. All source and normalized-span hashes and common-tokenizer counts reconcile. The [aggregate audit](review/aggregate-audit.md) states exactly what these checks establish.

## Sample and form boundaries

| Source group | Fully coded texts | Prose paragraphs | Scope |
| --- | ---: | ---: | --- |
| NEJM publisher Perspectives | 5 | 54 | Supplied articles from 2017–2019; publisher category contains arguments, reflection and narrative/explanatory hybrids |
| HBR practitioner arguments | 4 | 251 | *Managing Oneself*, *Using the Balanced Scorecard as a Strategic Management System*, *The Power of Talk*, *Customers as Innovators*; original dates 1995–2002, specific retained versions/reprints |
| HBR procedure/tool boundary cases | 2 | 88 | *Designing Services That Deliver* and *The House of Quality*; measured separately from arguments |
| Systematic reviews | 8 | 287 | Biomedical-origin XML collection; eight deterministic length-rank selections from 113 previously screened historical candidates |

The systematic-review selection used old exploratory length ranks 5, 20, 33, 48, 61, 76, 89 and 104 before full reading/coding. Selection covered different lengths, not fit to the proposed template. All eight passed the subsequent form screen. Earliest reported years are 2008–2014; one record has an unresolved 2014/2015 date discrepancy. These are availability and purposive samples, not representative samples of a population or proof of exemplary quality. The initial internal sample aims were larger; the actual completed denominators above govern the findings.

One additional HBR candidate, *Manufacturing: The New Case for Vertical Integration*, remains excluded from measurements: 60 of 62 candidate OCR units are uncorrected. The book *How Will You Measure Your Life?* remains outside the agreed scope. No new sources were downloaded for this pilot.

The independent NEJM reader classified two articles as arguments, one as personal reflection, one as narrative history, and the ARB recall article as an unresolved explanation/argument hybrid. Accordingly, the five-article NEJM figures below describe a **publisher cohort**, not one validated form. Likewise, the two HBR procedure/tool articles do not enter the four-argument statistics. This distinction prevents a platform or publisher label from quietly becoming a broad writing family.

## What repeats and what varies

**NEJM Perspectives.** The second reader found narrative openings in **3/5**, identifiable outside evidence in **4/5**, explicit responsibility/recommendation in **3/5**, and a qualified closing in **3/5**. These are interpreted presence counts with their own criteria, not automatic tests of quality or of the entire proposed sequence. The ACA argument opens with policy and a position; the science-suppression argument begins with clinical experience. Thus even the two clearly eligible arguments offer different entry points. The personal essay ends in reflection, while the CAR-T history develops discovery and perseverance. In primary paragraph coding, report, interpret and qualify occur somewhere in all five; this does not require three separate sections or a qualification at the ending.

**HBR practitioner arguments.** All **4/4** have an opening professional proposition; **3/4** state the author's research or organizational work early; **2/4** end with an explicit qualification or unresolved condition. None follows the strict complete definition → example → explanation → application sequence throughout all components. The original worksheet was optional: this stricter stress test asked whether its order deserved promotion into a general rule. It does not. *Managing Oneself* proceeds through self-assessment questions; *Balanced Scorecard* develops management processes; *Power of Talk* explains communication practices; *Customers as Innovators* develops a toolkit argument through cases, challenges and value capture. All four have primary-coded examples and explanations, with varying order, number and placement. The detailed operational definitions and source assessments are in the [HBR report](hbr/report.md).

**Systematic reviews.** All **8/8** have the functional jobs of introduction, methods, results and discussion, even where a heading is absent. Primary coding finds orientation in each introduction, reporting and explanation in each methods account, reporting and comparison in each results account, and interpretation and qualification in each discussion. A separately assigned conclusion role occurs in **6/8**, not always under a printed Conclusion heading. Qualifications also occur in Methods and Results; they are not confined to a final limitations section. Actual research methods are coded as report/explain, not instructions to the reader.

The full systematic pattern remains more variable than a checklist of headings suggests. One review reports that formal quality assessment was not done; another refers search details to an external protocol; some provide no distinct formal risk-of-bias tool in the body; two abandon planned quantitative synthesis or use different synthesis approaches. A missing research/reporting detail is recorded as missing, not inferred to be optional because other papers omit it. Review design and applicable reporting requirements remain separate from descriptive writing patterns.

## Observed length ranges

Words use the same `metrics.py` token rule across all groups. Counts describe main prose, excluding recognized front matter, references, sidebars, tables, figures and separately handled lists or displayed dialogue. Inline citations and quotations can remain within prose. The PDF texts were reconstructed from source order with page/bounding-box traces; line-break hyphenation and typography still introduce modest uncertainty. These are source-specific observations, not complete visible-document word counts or writing limits.

| Group | n texts | Body minimum / median / maximum | Middle half of pooled paragraph lengths | Paragraph minimum / median / maximum |
| --- | ---: | ---: | ---: | ---: |
| NEJM publisher Perspectives | 5 | 922 / 1,296 / 1,537 | 86–142 | 42 / 115.5 / 220 |
| HBR practitioner arguments | 4 | 4,169 / 5,806.5 / 7,302 | 64–112.5 | 6 / 89 / 268 |
| Systematic reviews | 8 | 2,681 / 4,078 / 7,203 | 70.5–152.5 | 13 / 108 / 453 |

The two HBR boundary cases have 2,511 and 3,199 prose words. They remain outside the practitioner-argument row. In particular, adding their shorter procedural paragraphs to that row would change its apparent shape for a classification reason.

Paragraph quartiles here pool paragraphs within the stated group. Longer articles contribute more paragraphs. The [statistics](results/statistics.json) additionally retain distributions of each document's median, so equal-document weighting can be inspected. The eight systematic reviews were deliberately selected across old length ranks; their measured extremes are neither the extremes of the entire earlier collection nor estimates of population limits. Earlier aggregate measurements used different extraction boundaries and must not be silently combined with these reconstructed counts.

**Systematic-review section budgets** can be described more specifically because the eight sources have comparable functional roles:

| Functional role | Present | Observed words: minimum / median / maximum | Middle half of observed word shares |
| --- | ---: | ---: | ---: |
| Introduction | 8/8 | 192 / 510.5 / 1,261 | 8.8%–15.6% |
| Methods | 8/8 | 305 / 675.5 / 1,465 | 14.6%–21.6% |
| Results | 8/8 | 286 / 1,168 / 3,601 | 23.0%–45.9% |
| Discussion | 8/8 | 659 / 1,480 / 1,958 | 25.2%–37.7% |
| Separately assigned conclusion | 6/8 | 61 / 164 / 279 | 2.5%–6.1%, conditional on presence |

These roles use disjoint paragraph assignments: separately assigned conclusion paragraphs are not counted again as discussion. A printed Discussion section may contain both roles. Reported quartiles and medians are calculated independently across documents; the columns are not a single document budget and do not have to add to 100%. External protocols, appendices, tables and lists also affect how much a paper places in main prose. The 305-word methods observation therefore cannot establish adequate methods reporting or a safe drafting minimum.

Comparable local section records are retained for the NEJM and HBR samples, but we have not established equivalent section jobs across their variants. Their word budgets should follow a selected variant rather than be pooled under a generic “section.” The two HBR procedure/tool boundary packets preserve source-heading inventories but have incomplete normalized section mappings; no section-role budgets are asserted for them.

## Paragraph functions: useful observations, uncertain assignments

The following are the primary coder's whole-paragraph lengths where a function was tagged. Each cell gives **median [middle 50%]; tagged paragraphs**. A paragraph may appear in several rows: the values are not separate allocations that can be added together.

| Tagged function | NEJM publisher cohort | HBR arguments | Systematic reviews |
| --- | ---: | ---: | ---: |
| Report | 116 [87.75–141.25]; n=34 | 98 [68.5–127]; n=43 | 104 [64–143]; n=218 |
| Explain | 117.5 [104.75–143.5]; n=16 | 91 [72.25–119.5]; n=110 | 142 [97–202]; n=53 |
| Qualify | 135.5 [108.75–149.5]; n=16 | 89 [66.25–107]; n=30 | 122.5 [89.75–182]; n=116 |

The JSON supplies minimum/maximum, source-document counts, all twelve functions, and distributions of per-document medians. These function-conditioned figures are **provisional annotations**, not calibrated linter thresholds. Whole-paragraph length includes the other jobs performed by that paragraph; it does not measure how many words were spent solely qualifying or explaining.

The second coding reviewed every NEJM paragraph and six evenly spaced targets per systematic-review and HBR text, with source context. First function labels were withheld. Different analysts supplied primary labels for different articles, so the primary corpus itself is not one uniform coder's style of annotation. Both passes are model judgments, not human-reader validation.

| Review group | Exact complete function-set matches | Mean label-set overlap (Jaccard) |
| --- | ---: | ---: |
| NEJM | 23/54 | 0.72 |
| Systematic reviews | 25/48 | 0.80 |
| HBR, including boundary cases | 7/36 | 0.60 |

Exact-set mismatch can be one extra label rather than a wholly different reading. Nevertheless, the disagreement is substantial. We should not hide it by calling the primary labels consensus or letting a model's single function judgment trigger automatic rewriting. The original annotations remain frozen; [coding-agreement.json](results/coding-agreement.json) preserves both sets and reasons rather than silently adjudicating them.

For the next annotation pass, require an identifiable claim target for support and qualification, distinguish faithful summary from a new interpretation, and state which concept an example illustrates. The existing twelve labels can stay while their boundaries receive contrasting examples and a small adjudicated test set. Link validity is computable; whether the relationship is correct remains an editorial assessment.

## Changes to the blank templates

The [revised blanks](templates-after-pilot.txt) retain alternative routes and local paragraph jobs:

- **Argument/perspective:** choose a position, problem or encounter as the opening; develop reasons/evidence and explain the connection; place qualifications beside the claims they limit; close with the consequence, recommendation or question the argument earns. A narrative opening and professional call to action are choices, not universal slots.
- **Practitioner argument:** choose a question-led, framework/process-led or case-led organization. Develop local sections with the definitions, examples, explanations and application the reader needs. Avoid requiring the complete same sequence in every section or an isolated early research section.
- **Systematic review:** retain question/rationale, actual methods, findings, interpretation and limits as jobs; make printed headings, subsections and a separate conclusion depend on the destination and report design. Keep what the study did distinct from guidance to readers. Never supply a missing method or result merely to complete the scaffold.

At this stage a range record should retain its reference cohort, source versions, counting scope, sample sizes, quantiles and annotation status. Working targets and declared minimum/maximum limits remain **unset** until a particular writing task supplies them. The result is inspectable reference material and better choices for a writing session, not a deterministic measure of writing quality or an installed form-specific harness.

## Reproducibility

Run `python3 experiments/pattern-test-2026-11-16/analysis/summarize_test.py` to reconcile source hashes, spans, shared-tokenizer counts, group membership, exact-copy exclusion of the development examples, registered section references and the second-coding comparisons. Individual source reconstruction/coding scripts and provenance are in [NEJM](nejm/documents.json), [HBR](hbr/documents.json) and [systematic](systematic/README.md). Full source text and rendered pages stay in the private workspace cache; repository records contain metadata, offsets, interpretations and measurements. The [validation receipt](results/validation.json) and independent audit establish bounded identity and calculation checks, not extraction completeness, semantic correctness, readership benefit or population norms.
