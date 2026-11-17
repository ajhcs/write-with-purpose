# What existing work changes

16 November 2026. This is an adoption proposal, not an installation or a replacement of the accepted foundations. Eight GPT-6.1 Terra scouts and a ninth independent Terra auditor supplied the source map. The parent separately verified two writing-feedback systems. The scout bibliography contains 66 DOI-deduplicated records; the two systems below are supplemental records, not additional independent datasets.

## Existing systems already implement much of this process

**Research Writing Tutor, Iowa State.** The [official description](https://cce.grad-college.iastate.edu/resources/researchwritingoers) connects three modules: understanding writing goals, exploring published writing, and analyzing one's writing against disciplinary research articles. The current page describes 32 disciplines. A [2016 primary paper](https://files.eric.ed.gov/fulltext/EJ1143609.pdf), DOI [10.1558/cj.v33i1.27047](https://doi.org/10.1558/cj.v33i1.27047), describes a sentence-level move/step analysis engine. This is a concrete predecessor for a teaching and feedback harness. Its current access page requests access; an open-source release or downloadable complete gold corpus was not verified. Current disciplinary coverage must not be substituted for historical study counts.

**AcaWriter, University of Technology Sydney.** Its [primary paper](https://www.jowr.org/jowr/article/view/578), DOI [10.17239/jowr-2020.12.01.06](https://doi.org/10.17239/jowr-2020.12.01.06), describes rhetorical feedback customized to different writing contexts. The [official project](https://cic.uts.edu.au/tools/awa/) documents analytical and reflective writing and pilots since 2015. The [open-source release](https://cic.uts.edu.au/open-source-writing-analytics/) links the application, Text Analytics Pipeline and Athanor rhetorical parser. We directly inspected the [application source](https://github.com/uts-cic/acawriter/tree/adc49ed10292852620bcbb09d0549afc75c04253): `FeedbackController.php` loads a feedback schema; `Profiler.php` applies tags, conditions and messages and supports a sentence-word-count check. That is a concrete precedent for form-specific checks and feedback. The application is Apache-2.0; dependency and content terms are separate. This was source inspection, not a deployment or accuracy test.

For Codex, the first useful adaptation is the separation of **analysis → form-specific feedback → author revision**, plus the learning and annotated-example modules. Inspect reusable schemas and examples before deciding whether to port components or run an entire application. A classifier's highlighted cue is a candidate interpretation; it is not proof that a function is present or absent. Fixed rule thresholds in an existing app are not observed writing norms.

## Inherit data before labeling more raw articles

| Harness component | First inheritance | What still needs our work |
| --- | --- | --- |
| Family → Form → Section | BAWE's purpose/stage/network fields; README-specific section codes; DITA procedure fields | Map source categories to our seventeen forms without erasing variants; student assignments are not professional norms |
| Function definitions and annotation | Move-analysis codebooks; MuLMS multilabel sentence roles; SciPara context protocol | Distinguish a complete realization span from a supporting quotation; test our definitions against original schemes |
| Relations and overlap | GUM/eRST linked relations and RSTmulti paired annotations | Align graph spans and paragraphs; measure boundary and label agreement separately |
| Published argument | Webis-Editorials-16's 300 annotated editorials | Resolve release/count semantics and source rights; do not equate argument types with our paragraph functions |
| Mechanics and language | Existing counting libraries and academic vocabulary resources | Pin tokenization and denominators; define technical terms and reader assumptions with the author |
| Learning while writing | Research Writing Tutor and AcaWriter | Preserve the author's ideas and wording; make feedback inspectable and optional |

For each source, retain its release, source document ID, original unit, original labels, attribution targets, uncertainty and rights. Put any proposed equivalence in a separate versioned crosswalk with evidence and counterexamples. A source sentence label or discourse relation must not silently become a paragraph function. Some of these resources were already in our earlier research notes; the new contribution is checking their actual schemas, releases and adoption limits.

Use our collected professional articles as a held-out comparison and for specific gaps. New manual annotation should fill those gaps or test a crosswalk, rather than recreate everything provided by an existing corpus.

## Which of the nine features can this supply?

**F02 section structure and F09 communicative functions** have the most direct existing definitions and annotated observations. **F01 document length, F03 section proportions, F04 paragraph shape, F05 sentence shape and F06 word length** can be computed only where complete, eligible text and the necessary boundaries survive. A sampled paragraph cannot supply a paper's section proportions. **F07 evidence/examples and F08 presentation** have partial annotations in particular schemes; citation roles, argumentative evidence and lists/code are distinct objects.

No inspected source gives the exact requested profiles for all seventeen forms, with audience, discipline, era and prominence controlled. Academic metadiscourse and move studies are extensive; complete professional proposals, decision memos and narrowly defined public/personal writing remain weaker in this map. The 44-study metareview itself pools some article sections and disciplines, illustrating why its means cannot be imported as our form targets.

The immediate next step should be a small schema and boundary compatibility pilot using existing annotations. Report what can be inherited unchanged, what needs a documented conversion, and what needs fresh human judgment. Only then estimate observed distributions for eligible form/audience groups, keeping observations, working targets and author-declared limits separate.
