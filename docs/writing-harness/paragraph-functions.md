# Initial paragraph functions

Version 0.1, 15 November 2026. This is a proposed annotation vocabulary and set of writing prompts, ready to try on examples. It is not a validated taxonomy or an additional set of measurement features. It develops F09 within the [nine accepted features](accepted-foundations.md). The [machine-readable catalogue](paragraph-functions.json) uses the same function names.

## Where functions fit

**Family → Form → Section** organizes the document. Within a section, paragraphs and smaller spans perform functions. A paragraph is a visible unit; a function describes what a passage contributes. One paragraph can perform several functions, and a single function can develop across several paragraphs.

| Level | What it selects | Example |
| --- | --- | --- |
| Family | Broad purpose and reader relationship | Explanation and documentation |
| Form | A recognizable reader task and possible structures | Conceptual explainer |
| Section | A local question or contribution; a printed heading is optional | How the mechanism works |
| Paragraph or span | Work the words perform in that context | Explain a relationship, then illustrate it |
| Relation between spans | How one contribution connects to another | This example illustrates that explanation |

Family and form names remain provisional. Subject, intended audience knowledge, destination, author voice, and applicable reporting requirements are additional context. They cannot be inferred reliably from the family alone. A specialist explainer and a beginner explainer may share functions while needing different definitions and examples.

The same `explain` function can occur in a research Discussion, a technical explainer, or a reflective essay. Its evidence obligations and vocabulary change with the form and audience. Functions are reusable tools, not exclusive paragraph types.

## Twelve starting functions

These definitions are our synthesis. They draw on the [guidelines already inspected](paragraph-functions-and-reuse.md) and the [historical research register](research/pre-2015-writing-evidence.md); no source establishes this exact twelve-part set.

| Function | Reader question | What it contributes | Boundary that matters |
| --- | --- | --- | --- |
| **Orient** | Where are we, and why does this matter here? | Relevant context, a problem, a question, stakes, or a change of direction | Background earns its place by preparing the next thought. An opening location alone does not make a passage orienting. |
| **Define** | What does this term mean here? | A concept's meaning, scope, distinguishing properties, or operational definition | Naming an example does not necessarily define the category. A definition need not use “is defined as.” |
| **Report / describe** | What is present, observed, or recorded? | A state, feature, method already used, result, or faithful summary | Separate reported observations from the author's inference. Reporting what a source claims does not endorse it. |
| **Assert** | What position, hypothesis, or proposal is being put forward? | A proposition for the reader to consider, including recommendations | In this annotation scheme, a factual report is not automatically a separate argumentative assertion. A recommendation also needs reasons and conditions when they matter. |
| **Support** | Why should I accept that claim? | Evidence or reasoning linked to a particular claim | A citation's presence does not show that it supports the claim. An invented example cannot establish an empirical result. |
| **Explain** | How or why does this work? | A mechanism, dependency, reason, or relationship the reader needs | A sequence of events can describe what happened without explaining why. A proposed mechanism must retain its uncertainty. |
| **Illustrate** | What would this look like in a concrete case? | An example, instance, analogy, or worked case that makes an idea recoverable | Identify whether the case is observed, reported, or invented. An analogy helps understanding without proving equivalence. |
| **Compare / contrast** | How are these things alike or different in a relevant respect? | An explicit relationship between alternatives on a stated dimension | Mentioning two things is not a comparison. Distinguish comparison from an unsupported ranking. |
| **Interpret** | What should I understand from this? | An implication, inference, synthesis, significance, or personal reflection | A summary preserving existing claims belongs under report; synthesis that draws a new relationship belongs here. Reflection need not imply a universal lesson. |
| **Qualify** | Under which conditions, and with what limits, does this hold? | Scope, uncertainty, an exception, a concession, or a limitation attached to an identifiable claim | A hedge such as “may” is not evidence that the relevant limitation has been explained. |
| **Instruct** | What should I do, under which conditions, and what should happen? | An action the reader can perform, with prerequisites, sequence, or expected result where needed | A Methods account usually reports what researchers did; it does not automatically instruct the reader to repeat it. Instructions can be paragraphs or list items. |
| **Narrate** | What happened, to whom, and what changed? | An event or experience unfolding through time | Presentation can be nonchronological. A technical procedure has a different reader task even when both use sequences. |

Keep the starting set small by treating **summarize** as a report variant, **reflect** as an interpret variant, and **recommend** as an assert variant. A counterargument or rebuttal may combine assert, support, interpret, and qualify. An introduction, conclusion, transition, and literature review are positions, relationships, or larger structures; they do not each need a thirteenth paragraph function. Introduce a new function only when recurring examples expose a useful distinction these labels cannot capture.

## How forms select combinations

These are possible patterns, not observed frequencies, obligatory orders, or quotas. A plus sign means functions can share a paragraph; an arrow indicates one possible progression. Paragraph boundaries remain an authorial choice.

| Provisional family | Form | Section or local contribution | Possible functions |
| --- | --- | --- | --- |
| Essays and commentary | Personal / reflective essay | An experience; its significance | Narrate + describe → interpret; qualify any broader inference |
| Essays and commentary | Argument / perspective | Develop a reason; address an objection | Assert → support + explain → qualify or compare |
| Explanation and documentation | Conceptual explainer | Establish the problem; explain the mechanism | Orient → define → explain + illustrate → qualify |
| Explanation and documentation | Tutorial | Prepare the learner; guide an exercise; make sense of the result | Orient → instruct + illustrate → explain |
| Explanation and documentation | How-to / procedure | Prerequisites; actions; verification or exceptions | Orient + qualify → instruct → describe the expected result |
| Explanation and documentation | Reference entry | Meaning; behavior; options and limits | Define → describe + compare + qualify; examples when useful |
| Research reports | Empirical article | Introduction; Methods; Results; Discussion | Orient + assert; report + explain; report + compare; interpret + support + qualify |
| Research reports | Study / review protocol | Rationale; planned methods | Orient + support; report the proposed design + explain its choices + qualify |
| Evidence syntheses | Systematic review | Eligibility / synthesis methods; results; discussion | Define + report + explain; report + compare; interpret + qualify |
| Evidence syntheses | Scoping review | Scope; mapped evidence; gaps | Define + report; report + compare; interpret + qualify |
| Evidence syntheses | Narrative / critical review | Thematic analysis; evaluation | Report + compare → interpret + support + qualify |
| Proposals and decisions | Decision memo | Options; recommendation; conditions | Compare + support → assert + explain → qualify |

A meta-analysis is a synthesis method that can be used within a systematic review, not a compulsory section or a label interchangeable with every review. A README or manual can compose several forms: orientation, a tutorial, procedures, and reference entries. Give each part its own section purpose; avoid one paragraph recipe for the entire container.

For academic work, select the relevant discipline, study type, and reporting guideline before making obligations. Results and Discussion can be separate or combined. The applied-linguistics corpus in Yang and Allison (2003) documents alternative configurations; it does not justify imposing one configuration on every field. [Publisher abstract](https://www.sciencedirect.com/science/article/pii/S0889490602000261)

## Function cards for learning and drafting

The catalogue includes one short elicitation prompt per function. Codex can use it to ask for the missing thought without taking over the paragraph:

```text
Family: explanation and documentation
Form: conceptual explainer
Section question: Why can a short queue still involve a long wait?
Audience: understands a queue; has not studied queueing theory

ORIENT: State the puzzle you want the reader to notice.
DEFINE: Distinguish the two measures that the puzzle confuses.
ILLUSTRATE: Supply a concrete case; mark it invented or observed.
EXPLAIN: Connect the case to the mechanism in your own words.
QUALIFY: State the conditions under which your explanation holds.

Ordering option A: puzzle → distinction → case → mechanism → limits
Ordering option B: case → puzzle → distinction → mechanism with limits
```

These are blanks for contributions, not copied sentence stems. Codex should recover answers from the author's notes first, then ask one useful question at a time. A short paragraph may combine several cards. The [annotated example](../../experiments/paragraph-functions/examples/queue-explainer.txt) is original synthetic material for testing the data format, not a writing-quality benchmark or an approved voice sample.

## Annotation rules

1. Record the form, section purpose, audience assumptions, and source version before assigning functions.
2. Keep planned functions separate from observed functions. An assigned task is not evidence that the prose accomplishes it.
3. Mark exact passages, permitting several functions per paragraph and an unresolved assessment. For detailed annotation, record smaller spans rather than forcing a sentence containing two moves into one label.
4. Record the connected passage and relation separately. Initial relation names are `supports`, `explains`, `illustrates`, `contrasts`, `qualifies`, `elaborates`, and `follows`. These are local conveniences informed by discourse analysis, not a full RST implementation. `follows` records a proposed progression, not causal proof or necessarily chronological order.
5. Ask what the passage adds for this reader. Length, a heading, a connective, or a citation cannot establish the function's success. Check unity and development in context, including justified repetition and implicit connections.
6. Let the second reading disagree. Record alternative labels and reasons before changing definitions. A model's confident label does not count as independent human agreement.

The initial code prototype records paragraph spans and their functions. Nested or overlapping subspans, multiple annotation rounds, and relation semantics remain outside that prototype.

## What code can check

| Assessment | Deterministic checks | Editorial or empirical assessment still needed |
| --- | --- | --- |
| Annotation integrity | **Implemented:** catalogue version and function IDs; section, evidence, and relation references; unique IDs; source hash; exact, ordered, nonoverlapping spans | Whether the selected span performs the labeled work; whether the supplied section boundary is meaningful |
| F04 paragraph size | **Implemented:** whitespace-token counts on each annotated span; explicit minimum / maximum constraints with their stated source | Whether the size is appropriate; whether these are the right paragraph boundaries |
| Planned versus observed roles | **Implemented:** display the supplied labels side by side and flag differences for review | Whether the observed labels are accurate or the difference improves the piece |
| F01–F06 and F08 measurements | **Future:** markup-aware body/section counts, sentence segmentation, character counts, distribution summaries, heading/list/code structure | Appropriate ranges; sentence-parser errors; readability and audience knowledge |
| F07 evidence and examples | **Implemented:** referenced evidence IDs exist. **Future:** resolve citation/figure identifiers and expected source locations | Source truth, entailment, representative examples, completeness, inferential strength |
| Vocabulary and audience | **Future:** profile-specific terminology checks; acronym and definition candidates; flag departures from the chosen glossary | Whether a reader understands the term, definition, or compressed relationship |
| Role-specific completeness | **Future:** check declared fields for a comparison's alternatives/dimensions, an instruction's prerequisites/result, or a qualification's target | Whether those fields correctly represent the prose and are adequate for the reader |
| Voice and originality | **Future:** surface exact phrase overlap with reference material and changes to protected author wording | Originality, plagiarism, meaningful similarity, voice fit, and whether the author has learned |

Code can validate a structured declaration without establishing that the declaration faithfully describes the prose. Keep three outputs separate: **mechanical findings**, **proposed editorial judgments**, and **author/reader feedback**. Never collapse them into a single “writing quality” score. Grammar diagnostics from the existing investigation can be another advisory input.

Observed ranges remain **unestimated** for this catalogue. Set no default paragraph minimum, maximum, sentence count, or readability grade. When measurements become available, retain sample size, selection criteria, source texts, annotation/parser versions, observed minimum/maximum, median and spread. Working targets and explicit limits remain separate decisions.

## Initial Codex run

1. Read the relevant form/section card and the author's notes. Show a compact paragraph map with its purpose, expected functions, and any declared limits. Make alternatives visible where they change the piece.
2. Help the author fill the missing contributions. In coaching mode the author writes first; in drafting mode Codex uses the notes. Preserve distinctive observations and phrasing through either route.
3. Draft with `write-with-purpose`; use `edit-with-purpose` for targeted repairs. Load a relevant academic/reporting component only for the selected form.
4. Propose observed annotations against the actual draft and run the read-only prototype. It currently needs an explicit annotation JSON file; it does not discover paragraph functions automatically.
5. Inspect source fidelity and the reader's actual task separately. Present local revision choices with their reasons, then recheck changed text. A successful mechanical run is not an editorial acceptance decision.

From the repository root:

```sh
python3 experiments/paragraph-functions/check_annotations.py \
  experiments/paragraph-functions/examples/queue-explainer.txt \
  experiments/paragraph-functions/examples/queue-explainer.annotations.json
python3 -m unittest discover -s experiments/paragraph-functions -p 'test_*.py' -v
```

The experiment is separate from installed skills. See its [interface and limits](../../experiments/paragraph-functions/README.md). The next empirical step is to annotate contrasting examples, measure disagreements, and revise the catalogue before fitting numerical profiles. A profile earns its place when it explains useful differences that remain visible in held-out authors and outlets.
