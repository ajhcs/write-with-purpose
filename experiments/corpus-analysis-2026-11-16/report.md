# First analysis of the collected writing sources

The collection now has a common measurement pass, source-level reviews of all 17 new PDFs, and an independent audit. We can begin describing how particular writing collections vary and testing alternative structural scaffolds. We have not established validated profiles, suitable word limits, or an intended reading level for the seventeen forms.

This report follows the accepted [nine features and Family → Form → Section model](../../docs/writing-harness/accepted-foundations.md). The source documents are research inputs; instructions printed in them do not govern this work. No new forms, numerical targets, or skill behavior have been adopted.

## What was actually analyzed

| Retained source collection | Source/outcome records | Records with positive extracted prose | Interpretation |
| --- | ---: | ---: | --- |
| Scientific XML, including the biomedical essay cache | 3,242 | 3,228 | Structured body paragraphs; predominantly health-related acquisition frames, with provisional form labels |
| Pinned documentation source files | 494 | 494 | Markdown, notebooks, reST and gallery Python; partial source extraction, including short or previously excluded candidates |
| HTML archives, retrieved essays, memos and legal example | 559 | 303 | Includes unavailable outcomes, holds, failures and excluded captures; measured bodies remain provisional |
| Existing and newly supplied PDFs | 80 | 79 | Approximate layout extraction; includes the excluded book and composite reference volume |
| **Total** | **4,375** | **4,104** | **Source records, not verified complete or independent articles** |

The inventory refers to 4,218 extant source paths, including copies. That is a file-path count, not a work count. Identity reconciliation retains two candidate version groups and separately flags eight differently titled essay requests that returned identical response bytes. Those eight remain separate requested works; a repeated landing-page response does not establish shared article identity. None of these duplicate/held records contributes positive prose to the reported 4,104.

The [inventory CSV](results/document-inventory.csv) records every current parser outcome; [coverage.json](results/coverage.json) supplies exact counts. Fifty-five HTML records remain held, representing 54 distinct response hashes; no held bodies were analytically parsed. Fourteen HTML extractions failed; 156 personal retrieval outcomes had no saved file. Fourteen XML records lack usable extracted prose; one PDF lacks an extractable text layer. These statuses are retained rather than silently discarded. Other unacquired business, engineering and legal leads remain in their earlier retrieval manifests and are not fabricated as documents here.

Earlier collections also contain **535 derived measurement records without retained source bytes**: 438 screened procedure/reference pages, seven separate archived-Python pilot pages, 67 reviews of works, 22 screened conceptual papers and one measured conceptual record excluded because it did not match a publisher-index card. These are registered in [legacy-derived-register.json](results/legacy-derived-register.json). Their earlier observations remain available, but cannot be recomputed with the common parser or pooled into this pass. The current identity keys find no links from these records into the new inventory; unresolved identities can still conceal overlap.

## Initial quantitative findings

These comparisons use only structured XML and the previously screened acquisition frames. They do not combine PDF layout blocks, source documentation fragments and XML paragraphs. The era below uses the earliest year reported by retained XML or discovery metadata. It is not a separately verified first-publication date. All reported years and disagreement flags remain in the inventory; 165 XML records have conflicting reported years. In particular, several trial reports have earlier discovery dates than their XML issue dates.

| Selected historical sampling frame | n | Observed minimum prose words | Middle 50% | Median | Observed maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Medical trial reports, earliest reported year before 2015 | 200 | 1,962 | 3,184–4,323 | 3,782.5 | 7,624 |
| MethodsX methods papers, earliest reported year before 2015 | 15 | 456 | 959–1,436 | 1,287 | 2,794 |
| Systematic-review candidates, earliest reported year before 2015 | 113 | 2,353 | 3,622–5,473 | 4,178 | 14,586 |

Quartiles in this table are rounded to whole words; the JSON preserves the calculations. Prose words exclude recognized titles, abstracts, captions, reference lists, administrative sections, lists, code and quotations. Substantive material with those presentation types therefore requires its own budget; this is not the complete visible word count of every document.

The first useful result is the spread. Even within the selected trial-report frame, the longest extracted prose is almost four times the shortest. A single median would obscure that variation. The MethodsX historical subset is both much smaller and confined to one venue; it cannot establish the typical length of a methods paper in another discipline.

The median of each document's median paragraph length is **101 words** for these trial reports, **96** for the fifteen historical MethodsX papers, and **93** for the historical systematic-review candidates. Their corresponding across-document medians of estimated sentence length are **23.75**, **21**, and **22** words. Thus substantially different document lengths can coexist with similar sentence and paragraph summaries. These observations alone cannot choose an audience level, voice, section order or a useful explanation.

Within the one MethodsX acquisition frame, median prose length is 1,287 words for the fifteen earliest-year-before-2015 sources, 1,553.5 for 82 sources in 2015–2019, and 2,424 for 103 later sources. Median estimated sentence length is 21 words in each group. This is a reason to preserve era and venue in profiles; it is not evidence that publication era caused the difference. Selection, subject and publication practices can differ.

All seven frame-by-era cells, paragraph counts, heading counts, extremes, quartiles and constituent records are saved in [exploratory-cohort-statistics.json](results/exploratory-cohort-statistics.json). The 200 trial, 200 MethodsX and 300 systematic-review memberships were independently reconciled. The larger collections of narrative, scoping, case and protocol candidates also have per-document measurements, but their noisy discovery labels have not been promoted into form-wide comparative distributions.

## What the seventeen new PDFs contribute

The [medical review](review/medical-uploads.md) identifies six NEJM Perspectives, one NEJM narrative review, three systematic reviews with meta-analysis, and Greenhalgh and colleagues' longer systematic review. The Perspectives differ in how they combine experience, policy argument, narrative, evidence and qualification. A publisher's Perspective label does not identify one mandatory paragraph sequence. Reporting completed research methods also differs from instructing a reader to perform a task.

The [nonmedical review](review/nonmedical-uploads.md) identifies a physics review with original calculations, a cloud-computing challenges overview, two HBR practitioner essays, a particle-data compilation and a book. The physics review combines synthesis and quantitative analysis. The cloud paper is an overview of research challenges, without the same evidence-selection structure as a systematic review. The HBR essays use different organizing devices: proposed leadership capabilities versus self-assessment questions.

Several distinctions materially change measurement:

- **How Will You Measure Your Life? is the 168-page book**, not the same-named article. It is retained as an attachment and excluded from the initial article corpus. Its two annotated passages are contextual only.
- **Review of Particle Physics is a 786-page reference compilation**, containing local topical reviews and data listings. It needs decomposition into units before an article-level profile. A single whole-file length or paragraph median is unsuitable.
- Three NEJM PDFs start with another article's ending, and some also finish beside a following article's beginning. Reviewers located target DOI markers at the target articles' endings. First-page DOIs and filenames cannot safely define the whole file's identity or boundaries.
- The HBR copies have original publication years of 1998 and 1999 and reprint years of 2004 and 2005. Those are different date fields.
- The cloud PDF extractor produces 32 one-word fragments among 142 apparent prose blocks. Its 8.5-word paragraph median is a layout artifact and must not become a writing target.

All 17 files have hash-verified workspace copies and source reviews. The reviewers selected **36 anchored passages across those files**, including the two contextual passages from the excluded book. The annotations demonstrate how functions can combine; they do not estimate full-document function frequencies. Medical annotations were independently hash-checked; nonmedical page/span hashes were checked by their reviewer. Function assignments are single-reviewer interpretations, with no inter-rater reliability claim.

## Family → Form → Section → contribution prompts

The initial evidence favors multiple inspectable patterns inside a form. These are optional blanks to test with the author, derived from the reviewed sources. They are not new accepted form names, fixed paragraph counts, borrowed wording or voice instructions.

| Family and candidate form | Possible section or unheaded movement | What the author supplies | Candidate functions |
| --- | --- | --- | --- |
| Essays/commentary → argument/perspective | Situation → position → reasons and consequences → conditions | The precise problem; what I think; why; what would change or limit that view | orient, assert, support, explain, qualify |
| Essays/commentary → personal/reflective essay | Encounter or event → tension → interpretation | What happened; what I noticed; why it matters to me; what remains unresolved | narrate, illustrate, interpret, qualify |
| Evidence syntheses → narrative/critical literature review | Scope and distinctions → thematic development → implications | What this review covers; concepts readers must distinguish; how findings relate; where the account is limited | orient, define, compare, explain, interpret, qualify |
| Evidence syntheses → systematic review | Question/eligibility → search and selection → synthesis/results → interpretation | The answerable question; what was eligible; what was done; what was found; what follows and what does not | orient, report, compare, interpret, qualify |
| Explanation/docs → reference | Scope/navigation → local entry | What can be looked up; the exact item; its meaning, conditions and applicable examples | orient, define, report, illustrate, qualify |

For example, the practitioner essays suggest two alternatives for an argument: begin with a concrete case and build a concept, or begin with a self-assessment question and contrast choices. The technical review suggests beginning with a frontier and analytical question, or beginning with a concrete process and connecting it to the larger question. Preserve those alternatives rather than averaging their order.

These prompts make space for the author's knowledge. They should help Cole say what he means before any model supplies connective prose. The sample does not establish that a given function must occupy one paragraph, appear once, or occur in this order.

## What code checks now, and what it cannot decide

| Feature | Implemented observation | Remaining judgment or missing evidence |
| --- | --- | --- |
| F01 Length | Prose tokens; separate XML title, abstract, caption, reference and excluded-administration counts | Correct body boundary, complete article, appropriate budget |
| F02 Structure | Ordered headings, levels and unique section IDs | Functional section identity, suitability, unheaded structure |
| F03 Proportions | Section prose totals and shares | Comparable roles and complete denominator; nested sections cannot be double-counted |
| F04 Paragraph shape | Per-block words, estimated sentences, within-document distributions | Whether a PDF block is a paragraph; whether the paragraph develops its idea |
| F05 Sentence shape | Heuristic segmentation and distributions | Formula/abbreviation handling, rhythm and reader comprehension |
| F06 Word length | Mean token characters | Reader's vocabulary, subject terminology, assumed knowledge; no reading-grade validation |
| F07 Evidence/examples | Explicit XML objects and citation cross-reference occurrences where supported | Whether material supports a claim, example function, evidential quality and sufficiency |
| F08 Presentation | Separate prose/list/code/quote/caption word counts | Correctly zoned tables, equations, sidebars and multimodal meaning |
| F09 Functions | Source hashes, span offsets and catalogue-ID checks; 36 interpreted passages | Function, relations, success and reader effect; no corpus-wide automatic role labeler |

The shared engine is actual executable code, not only a design proposal. The parser corrections and all method definitions are retained. There is still **no validated form profile**: `profile_eligible=false` throughout the joined inventory. This is a conservative release status for using sources as author-facing writing defaults, not a claim that every mechanical observation is useless.

## Coverage across the seventeen proposed forms

The first [acquisition overview](../form-corpus-2026-11-16/overview.md) remains the historical selection account. This pass adds common calculations and source review; it does not manufacture missing form coverage.

| Family | Forms addressed | Present basis and remaining gap |
| --- | --- | --- |
| Essays/commentary | Personal/reflective; argument/perspective; critical review of a work | 303 HTML bodies across all included HTML collections and retained biomedical essay XML are available; individual forms mostly unresolved. NEJM/HBR reviews add contrasting patterns. Critical-review measurements remain derived-only. |
| Explanation/docs | Conceptual explainer; tutorial; how-to/procedure; reference | 494 pinned source files reprocessed, 469 previously retained candidates. Procedure/reference bodies were not retained: 438 main-screen measurements and seven historical pilot pages remain separate legacy evidence. |
| Research reports | Empirical report; methods paper; theory/conceptual; case report; study/review protocol | Trial/method frames have common XML measurements. Case/protocol candidate files were reprocessed but label conflicts persist. Conceptual-paper legacy evidence remains separate; the supplied physics review is a hybrid requiring an explicit decision. |
| Evidence syntheses | Narrative/critical literature review; scoping review; systematic review | All retained XML candidates reprocessed; systematic screened-frame statistics broken out by era. Four reviewed medical uploads clarify systematic structures, while other uploads show narrative/hybrid alternatives. |
| Proposals/decisions | Proposal; decision memo | Three retained proposal PDFs now extracted; six historical decision memos reprocessed. These remain small, context-specific sets with no adopted writing norm. |

Medical/scientific XML and software documentation still dominate. The 36 business, 13 engineering, ten legal and one personal PDFs from prior retrievals were included alongside the new uploads and three earlier proposals, but unresolved identity/completeness and PDF boundaries prevent treating them as confirmed form exemplars. One official legal HTML example was also processed. This work does not meet a several-hundred-verified-examples target for every form and domain.

## What follows from this pass

The next useful pilot is a reviewable slice of actual sources and alternative outlines. The author can compare a narrative opening against a direct argumentative opening, or a thematic review against a methods-led synthesis, before selecting a structure for his own material. The stored section sequences and span functions provide the evidence for that comparison; the full heterogeneous median does not.

Before any numerical profile is adopted, confirm the slice's identities and article boundaries, decide which form each source serves, inspect paragraph extraction, retain domain/audience/era distinctions, and annotate a small set of full sections with a second reader. Only then should an observed distribution inform a chosen working target. Minimum and maximum limits still come from an explicit author/task/destination requirement. Audience vocabulary and technical terminology require their own source-grounded assessment and reader validation.

The [independent source audit](review/independent-audit.md) records eight bounded source checks, all upload hashes and medical passage hashes. It led to fixes for body-nested references, administrative ethics text, documentation line-wrap joins and inline-code preservation. The [aggregate audit](review/aggregate-audit.md) reconciles counts, identity groups and historical-frame medians. Neither audit certifies every source or the effectiveness of the proposed prompts.
