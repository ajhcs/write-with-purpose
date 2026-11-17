# Collected-source analysis

Started from the author's 15 November 2026 request to analyze the collected writing examples and 17 new PDF attachments. The directory identifier follows the host's UTC date. Read [the findings](report.md) first.

This is a reproducible exploratory analysis, with source review and bounded independent audits. It does not install a writing harness, validate a writing profile, or adopt targets. It uses the existing nine features and Family → Form → Section organization.

- [Coverage and counts](results/coverage.json)
- [Document inventory](results/document-inventory.csv): source/outcome grain, statuses, dates, measurements, candidate identity links; not a list of confirmed complete works.
- [Selected-cohort statistics](results/exploratory-cohort-statistics.json): all observed extremes, quartiles and medians, with constituent record IDs.
- [Attachment index](results/attachment-review-index.json), [medical review](review/medical-uploads.md), [nonmedical review](review/nonmedical-uploads.md).
- [Source/arithmetic audit](review/independent-audit.md) and [aggregate audit](review/aggregate-audit.md).
- [Legacy derived-only register](results/legacy-derived-register.json): earlier measurements whose source bytes were not retained; no pooling with current calculations.
- [Candidate version links](results/linked-versions.json) and [different-title response collisions](results/response-collisions.json).
- [Three-source comparison](comparisons/nejm-hbr-systematic.json) and [blank writing templates](comparisons/three-writing-templates.txt): one NEJM Perspective, one HBR practitioner argument and one systematic review, with eight source-anchored paragraph samples. Interpretations and scaffolds remain proposals; no new taxonomy or writing limits are adopted. Rebuild with `medsci-pdf-python experiments/corpus-analysis-2026-11-16/analysis/compare_three.py`.

Recompute offline from the retained workspace caches:

```bash
python3 experiments/corpus-analysis-2026-11-16/analysis/analyze_xml.py
python3 experiments/corpus-analysis-2026-11-16/analysis/analyze_docs.py
python3 experiments/corpus-analysis-2026-11-16/analysis/analyze_html.py
medsci-pdf-python experiments/corpus-analysis-2026-11-16/analysis/analyze_pdf.py
python3 experiments/corpus-analysis-2026-11-16/analysis/build_analysis.py
medsci-python -m unittest discover -s experiments/corpus-analysis-2026-11-16/tests -v
python3 experiments/corpus-analysis-2026-11-16/analysis/test_docs_parser.py
python3 experiments/corpus-analysis-2026-11-16/analysis/validate_analysis.py
```

The documentation parser uses the existing system-Python `markdown_it` installation; the PDF parser uses the existing `medsci-pdf-python` runtime. The PDF pass expects the stable attachment copies recorded in `inputs/attachments-manifest.json`. Original attachments remain untouched. No network request or installation is required in this environment. Full source texts and normalized text blocks remain in workspace caches outside this repository. See [measurement definitions](method-note.md) and the individual `analysis/*-methods.md` files for parser-specific scope and limitations.
