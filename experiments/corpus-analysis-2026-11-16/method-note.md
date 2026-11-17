# Measurement method

The parser supplies ordered, normalized blocks and is responsible for source-specific extraction, block roles, heading levels and section boundaries. The core does not fetch sources, determine a document's main-text boundary, remove references, detect captions or infer object counts. Parser omissions, PDF extraction errors and differing source markup limit comparisons. A parser should record unavailable object counts as null rather than zero; supplied `object_counts` pass through unchanged, and absent keys remain absent.

Word tokens are Unicode letter/digit sequences with internal apostrophes, periods or hyphens; punctuation and standalone underscores are excluded. This treats contractions, hyphenated compounds and decimals as single tokens, and counts numeric tokens. Mean word characters includes internal punctuation. Each nonblank `paragraph` is a prose paragraph; headings, list items, code, quotations and captions are counted separately, and their words are excluded from prose and section totals. Text in an unrecognized kind is not counted. Sentence segmentation is an estimate, independently within each paragraph. It protects decimals, common abbreviations and initials, and attaches immediately following numeric bracketed or parenthetical citations to the preceding sentence. Abbreviation ambiguity, references, unusual citation formats and extraction errors can alter sentence counts; review source text before interpreting fine differences.

Section totals and shares use prose words only. Explicit `section_id` values are aggregated as supplied; parsers must assign distinct IDs to distinct sections even if headings repeat. Without an ID, each heading receives an index-based ID; prose before a heading uses `__unsectioned__`. Heading sequence retains the text, ID and supplied level; maximum depth is zero if no numeric levels are supplied. Blank paragraphs are excluded. Empty distributions have null summaries; quartiles use linear interpolation at positions `(n - 1) * p`. These are descriptive observations, not limits or targets.

- **F01:** prose word count describes the supplied paragraph scope; title, abstract and references require parser-provided boundaries and separate reporting.
- **F02:** heading count, depth and sequence describe supplied headings, not inferred functional sections.
- **F03:** section prose totals and shares describe the parsed sections.
- **F04:** paragraph word and estimated sentence counts and the median paragraph word count describe nonblank prose paragraphs.
- **F05:** estimated sentence counts and word-count distributions describe heuristic segmentation.
- **F06:** mean token character length is descriptive, including internal punctuation; it is not a reading-level measure.
- **F07:** supplied object counts are inventory evidence only. Examples, citations, placement, and support relationships require source-specific extraction or assessment.
- **F08:** prose, list, code, quote and caption word totals describe the supplied presentation categories.
- **F09:** communicative functions are unassessed. Mechanical measurements do not establish roles, writing quality, evidence strength, reader comprehension or suitability.
