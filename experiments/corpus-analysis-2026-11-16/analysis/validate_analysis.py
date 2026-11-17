#!/usr/bin/env python3
"""Check retained-source identity, counts and aggregate arithmetic offline."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from metrics import summarize

ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate():
    rows = list(csv.DictReader((ROOT / 'results/document-inventory.csv').open()))
    counts = json.loads((ROOT / 'results/coverage.json').read_text())
    assert len(rows) == counts['inventory_records_including_unavailable_and_held']
    assert len({r['record_id'] for r in rows}) == len(rows)
    assert sum(r['has_measurement'] == 'True' for r in rows) == counts['measured_source_records_before_work_dedup']
    assert all(r['profile_eligible'] == 'False' for r in rows)
    hashes = {}
    for r in rows:
        if not r['source_path']:
            continue
        path = Path(r['source_path'])
        if path.is_file():
            if path not in hashes:
                hashes[path] = digest(path)
            if r['source_sha256']:
                assert hashes[path] == r['source_sha256'], str(path)
    assert len(hashes) == counts['retained_unique_source_paths']
    metrics_checked = 0
    for name in ('xml', 'docs', 'html', 'pdf'):
        for line in (ROOT / 'analysis' / f'{name}-records.jsonl').read_text().splitlines():
            r = json.loads(line)
            m = r.get('metrics') or r.get('approximate_metrics')
            if not m:
                continue
            assert sum(m['paragraph_word_counts']) == m['prose_words']
            assert len(m['paragraph_word_counts']) == m['prose_paragraphs']
            assert sum(m['section_words'].values()) == m['prose_words']
            assert len(m['sentence_word_counts']) == m['estimated_sentences']
            metrics_checked += 1
    index = {r['record_id']: r for r in rows}
    membership = Counter()
    for cell in json.loads((ROOT / 'results/exploratory-cohort-statistics.json').read_text()):
        members = [index[key] for key in cell['record_ids']]
        assert len({r['linked_work_id'] for r in members}) == cell['n_distinct_linked_works']
        membership[cell['sampling_frame']] += len(members)
        for key, expected in cell['statistics'].items():
            values = [float(r[key]) for r in members if r[key] != '']
            assert summarize(values) == expected, (cell['sampling_frame'], key)
    assert membership == {'screened_RCT': 200, 'screened_MethodsX': 200, 'screened_systematic_review': 300}
    attachments = json.loads((ROOT / 'results/attachment-review-index.json').read_text())
    assert len(attachments) == 17
    assert len({r['source_sha256'] for r in attachments}) == 17
    assert sum(r['scope_disposition'] == 'excluded_book' for r in attachments) == 1
    assert sum(r['scope_disposition'] == 'split_composite_before_profile' for r in attachments) == 1
    catalogue = json.loads((ROOT.parent.parent / 'docs/writing-harness/paragraph-functions.json').read_text())
    function_ids = {f['id'] for f in catalogue['functions']}
    annotations_checked = 0
    for kind in ('medical', 'nonmedical'):
        review = json.loads((ROOT / 'review' / f'{kind}-uploads.json').read_text())
        for document in review['documents']:
            for annotation in document.get('spans') or document.get('annotations') or []:
                labels = annotation.get('functions') or annotation.get('observed_functions')
                assert labels and set(labels) <= function_ids
                annotations_checked += 1
    assert annotations_checked == counts['manual_review']['passage_annotations']
    legacy = json.loads((ROOT / 'results/legacy-derived-register.json').read_text())
    assert len(legacy) == counts['legacy_derived_only_records']
    assert sum(r['prior_screen_included'] for r in legacy) == counts['legacy_derived_records_in_prior_screened_samples']
    receipt = {
        'status': 'passed', 'source_paths_hashed': len(hashes),
        'metric_records_with_reconciled_arithmetic': metrics_checked,
        'inventory_records': len(rows), 'reviewed_attachments': len(attachments),
        'annotations_with_registered_function_ids': annotations_checked,
        'screened_frame_membership': dict(membership),
        'limits': 'Byte identity and arithmetic only; not semantic identity, extraction completeness, writing quality, comprehension or adopted profile validation.',
        'artifact_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.suffix in ('.py', '.json', '.jsonl', '.csv', '.md') and p.name != 'validation.json'},
    }
    (ROOT / 'results/validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'artifact_sha256'}, indent=2))


if __name__ == '__main__':
    validate()
