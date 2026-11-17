# Authorities, definitions, and measurement sources

Research follow-up to the user's request for official authorities and usable definitions. Sources were checked in this session. This note maps the existing seventeen-form proposal to external sources; it does not adopt new categories or implement checks.

## What authority means here

There is useful authority within domains. This search has not located one official classification establishing our five families and seventeen forms across all writing. Separate four uses:

- **Controlled vocabularies:** stable labels and scope notes for discovery/cataloguing, such as NLM MeSH and Library of Congress Genre/Form Terms (LCGFT).
- **Standards and structured formats:** defined document components, such as OASIS DITA and NISO JATS.
- **Reporting/methodology guidance:** what a particular kind of research must describe, such as Cochrane, PRISMA and CARE.
- **Destination or institutional guidance:** conventions and requirements within a journal, funder, project, or educational context.

Authority is scoped. An institutional teaching guide is not an international standard. A document schema is not evidence that its contents are adequate. A catalogue label does not certify an exemplary work. Current vocabulary coverage is not proof that a term existed before 2015.

## Primary sources and practical uses

| Source | Status and useful definitions | Discovery or measurement use | Boundary |
| --- | --- | --- | --- |
| [NLM publication types with scope notes](https://www.nlm.nih.gov/mesh/pubtypes.html) | Government-maintained vocabulary: Essay, Personal Narrative, Comment, Review, Scoping Review, Systematic Review, Technical Report, Clinical Trial Protocol, etc. | Candidate labels and definitions; PubMed publication-type fields where applicable; NLM catalogue discovery | Health/science indexing scope; not all vocabulary entries are usable PubMed article filters, and indexing may be incomplete |
| [LCGFT](https://www.loc.gov/aba/publications/FreeLCGFT/freelcgft.html) | Library of Congress genre/form vocabulary with cataloguing instructions | Broader literary/nonmedical discovery using verified catalogue terms | Catalogue units may be whole collections/books rather than the individual essays we want. Resolve individual term records before treating a label as an exact match |
| [OASIS DITA 1.2 information types](https://docs.oasis-open.org/dita/v1.2/os/spec/archSpec/dita_technicalContent_InformationTypes.html) | Historical formal standard defining concept, reference and task models | Typed source documents; inspect prerequisites, steps, results, examples and topic structure | Technical task-support context; a concept topic is not an exact synonym for every conceptual essay |
| [Diátaxis](https://diataxis.fr/) | Practitioner framework defining tutorial, how-to, reference and explanation through reader needs | Classify documentation pages, compare task/learning/lookup/understanding purposes | Useful framework, not an ISO standard or measured optimum |
| [ISO/IEC/IEEE 26514:2022 official preview](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec-ieee%3A26514%3Aed-1%3Av1%3Aen) | Formal software user-information standard; supersedes ISO/IEC 26514:2008 | Candidate source for documentation terminology and applicable requirements | Official preview/scope checked; full normative text not audited here. No new clause-level obligations or universal length rules asserted |
| [NISO JATS article-type](https://jats.nlm.nih.gov/articleauthoring/tag-library/1.4/attribute/article-type.html) | Standardized metadata attribute with suggested article types and descriptions | Discover publisher-labeled research articles, reviews, case reports and commentaries in XML | Optional, accepts arbitrary text, and preserves publisher variation; not a closed universal genre taxonomy |
| [NISO JATS word-count and counts](https://jats.nlm.nih.gov/publishing/tag-library/1.4/element/word-count.html) | Defines document/component word-count metadata and specific counts for figures, tables, references and other objects | Reuse structured counts where supplied; extract consistent components for recomputation | Word-count is described as approximate. Availability and counting scope need checking; do not silently mix publisher counts with our own |
| [ICMJE manuscript preparation](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html) | Medical editorial recommendations for manuscript organization and reporting | Original research often uses IMRAD; route to design-specific reporting guidance and separate abstract/body counting | Explicitly allows different structures for other article types; not universal across disciplines |
| [Cochrane Handbook](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-01) | Methods authority for systematic reviews of interventions | Eligibility definitions, evidence workflow and review-method distinctions | Its primary scope is intervention reviews. It does not supply general essay metrics |
| [PRISMA and extensions](https://www.prisma-statement.org/home), [PRISMA-ScR](https://www.prisma-statement.org/scoping) | Reporting guidance for systematic and scoping reviews | Reporting items to annotate and supporting examples; distinguish review forms | Checklist coverage differs from methodology quality, paragraph quality and section word budgets. ScR is a 2018 extension |
| [CARE checklist](https://www.care-statement.org/checklist) | Consensus clinical case-report reporting guidance | Case-report components and reader questions; locate examples using the publication type | Clinical reporting scope; cannot impose it on every use of “case study” |
| [NSF proposal preparation](https://www.nsf.gov/funding/preparing-proposal) | Funder-specific requirements and section purposes | Defines project-summary and project-description expectations; source of declared page limits | Program solicitation can override general rules. NSF limits do not characterize all proposals; pages are not a fixed word count |
| [MIT Communication Lab policy memo](https://mitcommlab.mit.edu/broad/commkit/policy-memo/) | Institutional practitioner/teaching guidance | Recommendation, context, evidence and implementation as a local structure | Policy memo is one kind of decision-oriented memo; its page advice is scoped institutional guidance |
| [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | Platform-owner documentation | Reader needs: project purpose/usefulness, getting started, help and maintainers | Does not require universal section headings or establish an ideal README length |

## Crosswalk to the existing candidate forms

“Partial” means a nearby category or context-specific authority, not a verified equivalent. Preserve the original external label alongside ours.

| Proposed form | Best starting anchor | Fit |
| --- | --- | --- |
| Personal / reflective essay | NLM Essay and Personal Narrative; LCGFT for broader discovery | Partial: personal narrative is experience-centered; reflection and literary quality require screening |
| Argument / perspective | NLM Comment and Editorial; publisher article-type definitions | Partial: comments may concern another work; editorials can depend on authorship role |
| Critical review of a work | JATS book-review/product-review where applicable; literary catalogue vocabulary | Partial: a work review differs from a research-literature synthesis |
| Conceptual explainer | Diátaxis explanation; DITA concept | Good technical-context anchors; wider public explanation needs a local definition |
| Tutorial | Diátaxis tutorial | Direct operational definition through learning purpose |
| How-to / procedure | Diátaxis how-to; DITA task | Direct task-oriented anchors; distinguish learning from accomplishing a known task |
| Reference | DITA reference; Diátaxis reference | Direct documentation anchors; specify lookup unit |
| Empirical research report | JATS research-article; ICMJE and applicable study-design guidance | Useful discovery/structure anchors; metadata does not prove an empirical contribution |
| Methods paper | Selected journal's methods article-type definition | No single universal mapping verified here; technical report is broader |
| Theory / conceptual paper | Selected disciplinary journal's article-type definition | No universal one-to-one controlled type verified here |
| Case report | JATS case-report; NLM Case Reports; CARE for clinical reporting | Strong clinical anchors; distinguish other disciplinary case studies |
| Study or review protocol | NLM Clinical Trial Protocol for that subtype; appropriate protocol-reporting guidance | Partial: clinical study and review protocols need separate applicable profiles |
| Narrative / critical literature review | NLM Review; JATS review-article; publisher definitions | Broad discoverability; inspect review purpose/methods to identify subtype |
| Scoping review | NLM Scoping Review; PRISMA-ScR | Direct research/review anchors; historical indexing can be incomplete |
| Systematic review | NLM Systematic Review; Cochrane; PRISMA | Strong scoped definitions and discovery routes; meta-analysis remains a method setting |
| Proposal | Relevant funder's solicitation and preparation guide; NSF as one example | Strong only after destination/type is selected |
| Decision memo | Recipient's template; MIT policy-memo guidance as an initial model | Partial: no general cross-domain standard verified here |

README and manual remain composite document types. GitHub supplies README-specific reader needs. DITA and the applicable user-information standard can describe manual components. Neither implies one outline for every complete manual.

## Definitions versus metrics

| Desired information | Best evidence source | What follows |
| --- | --- | --- |
| Recognized name and category boundary | Vocabulary scope note, formal type definition, or explicit operational framework | Reusable search terms and eligibility rules |
| Required parts / declared maximum | Selected destination's rules, adopted standard, applicable reporting guidance | Potential conformance checks with source/version/scope |
| Typical total and section lengths, paragraph/sentence distributions | Comparable complete texts with the selected form, audience and subject | Measured observed distributions; not automatic limits |
| Figure/table/reference counts | Structured full text and count metadata, verified/recomputed consistently | F07/F08 observations; distinguish reference-list count from citation occurrences |
| Paragraph functions and their relationships | Annotated examples with reviewed assignments | F09 observations, including mixed/unresolved cases |
| Audience knowledge / vocabulary | Intended-reader definition, disciplinary terminology resources, actual reader feedback | Assumed/explained terminology and editorial assessment; a reading-grade score is insufficient |

These authorities mostly define types, components and obligations. This search has not found authority-endorsed universal min/median/max sentence or paragraph lengths for all seventeen forms. Existing corpus findings remain the route to descriptive ranges. Publisher limits remain declared constraints for that destination.

## Small, reproducible discovery examples

The [PubMed help](https://pubmed.ncbi.nlm.nih.gov/help/) distinguishes the broader systematic-review filter from the exact publication-type field. A query template is:

```text
TOPIC AND systematic[sb]
```

For an exact indexed type and a historical interval:

```text
TOPIC AND "Systematic Review"[pt] AND 2010:2014[dp]
```

These are documented query patterns, not executed searches or counted results in this step. Replace `TOPIC` with the actual subject. Exact `[pt]` searching can miss older or incompletely indexed work; a missing label does not prove ineligibility. Confirm methods in the full text. Likewise, a repository's `/tutorial/` path or DITA topic type is an initial selection signal whose reader task still needs checking.

## Recommended next decision

Keep our five families as navigation and attach source-backed definitions to individual forms. For one form at a time, agree on a short definition, inclusion/exclusion examples, discovery labels and measurement unit. Test those decisions on a few real works before expanding the schema or implementing further tools. The crosswalk is research support for that discussion, not an adopted replacement taxonomy.
