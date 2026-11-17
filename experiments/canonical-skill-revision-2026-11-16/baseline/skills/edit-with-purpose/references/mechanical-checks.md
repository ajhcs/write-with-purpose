# Mechanical checks

For a requested exact check, reuse the existing `write-with-purpose/scripts/check_text.py` helper when it is available in a known configured skill root. Read its usage or run `--help` if needed. If it is unavailable, identify the unavailable mechanical check and continue the editorial work. The editor has no required service or helper installation.

```text
python <writer-skill>/scripts/check_text.py <edited.txt> [--source <before-or-source.txt>] [--contract <contract.json>] [--enforce-contract]
```

The helper reports exact duplicate prose paragraphs, explicit unresolved markers, limited internal Markdown-anchor discrepancies and source-number differences. Checker 0.2.0 also checks declared `max_words` and `max_growth_words` limits. For a no-growth requirement use `{"max_growth_words": 0}` with the original draft as `--source`. `--enforce-contract` exits 1 when a declared literal or word limit fails, 2 for unavailable inputs, and 0 when the declared checks pass; unrelated observations remain advisory. Counts are whitespace-separated tokens in the entire raw artifact, including markup/code, with an initial UTF-8 BOM excluded. Check the installed helper's supported flags; do not claim enforcement if an older helper cannot run the requested check. It does not judge semantic correctness, paragraph flow, useful repetition or reader benefit. Its input hashes identify the bytes checked.

Use contracts for actual obligations. A selected explanation need not retain every source number, and a justified omission is not a reason to restore a fact mechanically. Interpret findings in context; retain good writing where an observation has no editorial consequence. Check the delivered bytes again if changes make an earlier receipt stale. The helper is read-only, with no automatic repair loop.

When a local spelling or grammar engine is available, record its version, dialect, dictionary and configuration with the input hash. Treat its spans and replacements as proposals. A spelling suggestion can name a different technical concept; verify the intended term before accepting it. Preserve deliberate punctuation and repetition when they serve the passage. A clean grammar report does not settle sentence meaning or reader benefit. Such an engine is not a required dependency of this skill.
