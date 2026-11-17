# Public argument labels and the twelve paragraph functions

16 November 2026. This is a proposed crosswalk for the user's own harness, not a change to the source catalogue or evidence that a mapping is valid. The [machine-readable crosswalk](argument-crosswalk.json) gives every exact label, source definition, unit, possible functions, conditions and validation checks. Multiple harness functions can coexist; neither source's units are paragraphs.

## Webis-Editorials-16

The [2016 codebook in the paper, section 3](https://aclanthology.org/C16-1324.pdf#page=4) defines six mutually exclusive types for short proposition spans. It describes testimony, statistics and anecdote as evidence types, but the released scheme does **not** identify their claim targets. That missing relation prevents automatically inferring the harness's `support`, which requires a connection to an identifiable claim. The paper explicitly notes that units may have multiple types despite its single-label design.

| Original type | Possible harness functions | Decision boundary |
| --- | --- | --- |
| `common-ground` | `orient`, `report` | Only where the passage prepares context or reports material; presumed shared knowledge is not proof of truth. |
| `assumption` | `assert`, `report`, `interpret` | Overlaps several functions: an opinion, observation and inference are different things; ordinary declaratives are not automatically assertions. |
| `testimony` | `report`, `support` | Attribute the proposition; support needs a claim and a reasoned connection. |
| `statistics` | `report`, `support` | A numeric observation can be reported; a target and connection are required for support. |
| `anecdote` | `report`, `illustrate`, `narrate`, `support` | A single event is not automatically narrative; illustration needs a recoverable idea, narration development through time, and support a claim connection. |
| `other` | None determinable | Outside this argument taxonomy does not mean functionless; retain for open review. |

The release also uses `continued`, `no-unit`, `par-sep` and `title` as structural/process markers. Inspecting the 300 files in `annotated-txt/split-by-portal-final` found 25,933 `continued` and 16,399 `no-unit` rows. These are segments, not 42,332 additional argumentative units. The README says a line represents a unit **or** paragraph separator, but actual records also contain `continued` segments and occasional fourth modification fields; [paper section 4.2](https://aclanthology.org/C16-1324.pdf#page=5) says to merge continuations through the following terminal class. Preserve original rows, punctuation and paragraph boundaries, validate each merge and compare reconstructed text to XMI before computing paragraph measures. Final-unit counts in the paper and raw rows differ; they must not be silently equated. The paper reports overall κ 0.56 and much weaker agreement for `common-ground` and `other`; majority/adjudicated labels are not independent gold truth.

## Argumentative microtexts

The [source DTD](https://raw.githubusercontent.com/peldszus/arg-microtexts/master/corpus/arggraph.dtd) and [annotation guidelines](https://angcl.ling.uni-potsdam.de/pdfs/ArgGuidelinesEnglish.pdf) distinguish the text-bearing `edu`, argument node `adu`, and structural `joint`. `pro` and `opp` are ADU dialectical roles, while document stance `pro`, `con`, `unclear` answers the trigger question. The same spelling `pro` therefore has distinct meanings at different levels. An opponent's statement need not be endorsed by the author.

| Original edge | What it represents | Harness consequence |
| --- | --- | --- |
| `seg` | EDU/joint grounding to an ADU | Structure only; no paragraph-function inference. |
| `sup` | Support between ADUs | Preserve source, target and role; possible `support`, subject to editorial review. |
| `exa` | Support by example | Possible `support` and/or `illustrate`; the two contributions are distinct. |
| `add` | Additional premise in a multi-premise relation | Preserve its relation context; do not assume an independent argument. |
| `reb` | Attack on a proposition | Preserve attack polarity; a refutation is not automatically `qualify`. |
| `und` | Attack on an inference/edge | Preserve edge-to-edge target; a conditional exception may qualify, but not every attack does. |

The main claim is a graph concept rather than a guaranteed verbatim span: the guidelines allow an inferred inserted `[MC]`. Keep that status explicit and never fabricate a quote or paragraph alignment. Graph constraints, IDs, endpoint types and segmentation can be checked mechanically; validity of the argument, function, attribution, and claim connection requires review. These short elicited texts, including translations, are not representative professional-publishing norms.

## Practical adoption

Keep source labels and their layers as metadata and generate only review candidates, with unresolved and multiple functions allowed. Link every function candidate to original spans and any argument targets; never manufacture missing links. Test reconstruction on actual files and preserve continuation, punctuation, and non-argumentative text before measuring. Separately evaluate whether paragraph coding is useful for the chosen form and reader; neither source establishes a universal length target or quality score.
