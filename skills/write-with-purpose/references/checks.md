# Advisory checks

Check the final text within the scope the brief counts. Use the destination's counting convention when it specifies one. For a saved UTF-8 artifact, the optional read-only checker uses Python 3 and its standard library.

```text
python <skill>/scripts/check_text.py <draft.md> [--source <source.md>] [--contract <contract.json>] [--enforce-contract]
```

## Declare actual requirements

The contract accepts these three keys. Include only the ones the brief requires.

```json
{"protected_literals": [{"text": "required wording", "min_count": 1}], "max_words": 250, "max_growth_words": 0}
```

- `protected_literals` counts case-sensitive, nonoverlapping occurrences in the raw text. Supply nonempty text and a positive minimum, which defaults to one. Use this for an exact wording obligation.
- `max_words` caps whitespace-separated tokens in the entire raw artifact, including markup and code, with an initial UTF-8 BOM excluded.
- `max_growth_words` caps the final count minus the source count. For a no-growth brief, set it to zero and pass the original draft as `--source`. Both caps take nonnegative integers.

Isolate the actual body if headings, notes, references, or other material are excluded from its count. Use an appropriate separate check for other obligations, such as a minimum length, paragraph count, or required placement. An available counter can still verify length when the helper is unavailable.

## Interpret the result

Review the relevant check statuses and findings. The checker reports duplicate prose paragraphs, explicit unfinished markers, limited internal Markdown-anchor discrepancies, and number differences when given a source. These observations point to places worth reading. Check whether a repetition serves two readers' needs or a number change reflects an accurate conversion or justified selection.

With `--enforce-contract`, exit 0 means the declared limits and literals passed and exit 1 means they were violated. Invalid input or invocation exits 2. In advisory mode, exit 0 means the assessment ran. Inspect `contract_enforcement` separately from other observations.

Use `input.sha256` to identify the checked bytes and verify the source and contract records when they matter. After edits, rerun applicable checks on the delivered artifact or scoped body. Verify separately that the checked text is what appears in chat or in the export. Review placement, attribution, meaning, and usefulness by reading the actual result.
