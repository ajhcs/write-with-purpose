# NEJM Perspective holdout: local source audit and preliminary structural test

This is a **five-article, fully paragraph-coded pilot**, not a validated genre profile. The original comparison, “Dead Man Walking” (2013), is excluded from the holdout. We located five other publisher-labeled Perspective PDFs, all 2017–2019; this falls short of the requested 8–12 independent pieces and provides no pre-2015 holdout. The six attachments were supplied together, so independence here means different articles, not a random sample or independence from the source selection process. No network was used.

The retained inventory contains 3,242 XML records, all paths present and parsed. Journal-title and journal-id metadata matching identified 19 NEJM records; none had a publisher Perspective subject or a NEJMp DOI. Five editorials have NEJMe DOIs, and “Long Covid Defined” has the NEJMsb DOI; their publisher category remains unconfirmed. The others have NEJMoA or NEJMc DOIs. No XML record was added to the Perspective holdout on this metadata alone. This is a search of the retained collection, not evidence that no NEJM Perspective XML exists elsewhere. The six labeled PDF receipts, raw hashes, 19 XML metadata matches, source paths and two traceable selected passages per PDF are in `inventory.json`. The personal text cache stores exact copies of the prior per-page extraction. Passage offsets are Unicode code points, end-exclusive, and their hashes were checked. The attachment classifications and original publication years were taken from prior visual/source review receipts. The derived page text remains an extraction, not a facsimile.

## Test of the prior sequence

The proposed sequence was experiential reaction/case → wider evidence and qualification → responsibility/action → stakes. It is a possibility suggested by one article, not a required pattern. These observations are individual reviewers’ interpretations; paragraph labels use IDs from the proposed twelve-function catalogue. Section roles are descriptions, not new catalogue functions. All 15 PDF pages were rendered and visually inspected to establish target-article boundaries and reading order.

| Article and year | Provisional functional movement | Test and counterpattern |
| --- | --- | --- |
| Repealing the ACA without a Replacement (2017) | Policy transition and position; reported coverage and reform record; possible repeal effects and tradeoffs; policymaker recommendation; human stakes | Opens with a policy position and aggregate claims rather than an encounter. Qualification and personal political experience appear, but the order and evidence are not the proposed patient-case progression. |
| Resisting the Suppression of Science (2017) | Doctor–patient communication experience; wider problem of science rejection and suppression; explanations and possible responses; qualified call to improve communication | Case-to-wider-problem and action elements recur, but the ending explicitly recognizes uncertainty about the correct response. The opening is a recurring experience rather than a single developed patient case. |
| The Other End of the Stethoscope (2017) | Father's diagnosis and call; family and hospital experience; recovery and reflection on medicine | Experience-led, but closing is personal reflection on purpose and mortality, not a policy prescription or evidence review. It is a counterexample to treating wider empirical evidence and explicit action as obligatory. |
| Tragedy, Perseverance, and Chance (2017) | Patient story and development history; investigators and trial experience; treatment, technical limits and cost debate; reflection on perseverance | Narrative and qualification recur, but its historical development and concluding reflection do not reduce to a specific professional duty or action. |
| Hypertension Hot Potato (2019) | Recall and scale; manufacturing, supply and clinical response; regulatory and health-system challenges; proposed preparation | Event and system-led, with no personal encounter required. It ends in recommendations for institutions and clinicians, rather than returning to a particular patient's story. |

These differences support retaining optional, reorderable moves and distinct variants rather than adopting a fixed Perspective template. Five convenience-selected pieces from one narrow period cannot establish frequency or a general convention. Absence above means not apparent in the reviewed article movement, not proof that no sentence performs the function. Paragraphs carry multi-function annotations as hypotheses, not consensus. The earlier selected passage offsets remain in the inventory as historical examples; complete coding is linked separately.

## Source and measurement limits

All five holdouts are fully coded at paragraph level by one analyst per article. Original PDFs were rendered; article columns, continuation fragments and paragraph breaks were inspected, and adjacent articles, duplicated pull quotes, graphics, captions, disclosures and references were excluded. The coding records retain page coordinates, source and normalized-text hashes, offsets, paragraph roles and proposed functions. Normalized full text and rendered pages remain in the private cache. The shared `metrics.py` word tokenizer is used throughout; inline superscript citation numerals remain and may affect counts. One line-wrapped compound in the ACA article has a spelling ambiguity without affecting its token count.

| Article | Main-body word tokens | Paragraphs | Coding record |
| --- | ---: | ---: | --- |
| Repealing the ACA without a Replacement | 1,296 | 12 | [Coding](aca-science/NEJMp1616577-coding.json) |
| Resisting the Suppression of Science | 1,292 | 10 | [Coding](aca-science/NEJMp1702362-coding.json) |
| The Other End of the Stethoscope | 922 | 8 | [Coding](narratives/NEJMp1707514-coding.json) |
| Tragedy, Perseverance, and Chance | 1,537 | 13 | [Coding](narratives/NEJMp1711886-coding.json) |
| Hypertension Hot Potato | 1,316 | 11 | [Coding](arb/article.json) |

These are descriptive measurements of this convenience-selected 2017–2019 set, not limits or a recommended length. Prior approximate PDF counts were unsuitable because they included layout artifacts and neighboring material. Paragraph hashes and word counts were independently checked against retained body text. A second reviewer has not yet adjudicated the function labels or section boundaries, and the small set cannot establish a pre-2015 convention.
