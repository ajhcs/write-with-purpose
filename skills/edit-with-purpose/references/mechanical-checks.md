# Mechanical checks

Check the final text against the brief's actual limits and exact wording requirements. If the writer skill is available in a configured skill root, use its read-only Python 3 checker for its supported contracts. Otherwise use an appropriate available counter or comparison. Report a verification limit when it affects the result.

```text
python <writer-skill>/scripts/check_text.py <edited.txt> [--source <before-or-source.txt>] [--contract <contract.json>] [--enforce-contract]
```

The supported contract keys are `max_words`, `max_growth_words`, and `protected_literals`. To check no growth, use `{"max_growth_words": 0}` with the original draft as `--source`. For required exact wording, use `{"protected_literals": [{"text": "required wording", "min_count": 1}]}`. Match the contract to the actual brief. Preserve the meaning of an idea through the wording that best serves the piece when its wording is flexible.

The checker counts whitespace-separated tokens in the entire raw UTF-8 input, including markup and code, excluding an initial BOM. Check a scoped body separately when other material is excluded. For requirements such as a minimum length, paragraph count, or specific placement, check them directly in the intended format.

In enforcement mode, exit 0 means the declared checks passed, exit 1 signals a declared violation, and exit 2 signals invalid input or invocation. In advisory mode, exit 0 means the assessment ran. Read `contract_enforcement` and the relevant observations. Exact duplicates, unfinished markers, limited anchor discrepancies, and source-number differences are review leads. Interpret them within the brief's coverage and the source's meaning.

Match the report's `input.sha256` to the bytes checked. Rerun the applicable checks after edits and confirm that the checked text matches the delivered chat or export scope. Read for attribution, placement, qualifications, and implications separately.

Treat an available grammar engine's findings and replacements as suggestions. Verify technical terms and deliberate choices against the text. When reporting a reproducible grammar check, record the engine version, dialect, dictionary, configuration, and input hash.
