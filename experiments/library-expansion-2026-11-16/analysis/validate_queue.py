"""Validate export integrity and coverage accounting; no network calls."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
def read(p):return json.loads(Path(p).read_text())

rows=read(ROOT/'candidate-ledger.json');summary=read(ROOT/'summary.json');cells=read(ROOT/'coverage.json')
assert len(rows)==summary['raw_candidate_records']
assert len({r['candidate_key'] for r in rows})==len(rows)
assert len(cells)==102 and len({(c['field'],c['form_id']) for c in cells})==102
assert len({c['form_id'] for c in cells})==17
assert Counter(c['status'] for c in cells)==summary['cell_statuses']
for relative,sha in summary['raw_input_sha256'].items():
    p=ROOT.parent.parent/relative
    assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,p
for row in rows:
    assert row['title'] and row['authors'] and row['retrieval_locator'] and row['verification_sources'],row['candidate_key']
    assert row.get('doi') or row.get('stable_url'),row['candidate_key']
primary=[r for r in rows if r['placement_status']=='primary_candidate']
pull=[r for r in primary if r['library_pull_action']!='review_existing_first']
conditional=[r for r in rows if r['placement_status']!='primary_candidate']
assert len(primary)==summary['primary_placements']
assert len(pull)==summary['primary_pull_placements']
assert len(conditional)==summary['conditional_or_uncounted_records']
assert len({r['form_id'] for r in primary})==17
csvrows=list(csv.DictReader((ROOT/'library-pull-list.csv').open()))
assert {r['candidate_key'] for r in csvrows}=={r['candidate_key'] for r in pull}
expected_doi={r['doi'] for r in pull if r['doi']}
assert set((ROOT/'dois-to-pull.txt').read_text().splitlines())==expected_doi
assert len(expected_doi)==summary['doi_pull_count']
ris=(ROOT/'library-pull-list.ris').read_text()
assert ris.count('TY  - ')==ris.count('ER  - ')==summary['distinct_primary_pull_works']
assert '{None}' not in (ROOT/'references/library.bib').read_text()
for c in cells:
    if c['status']=='three_targets':assert c['provided']==3
    for cid in c['candidate_ids']:
        r=next(r for r in rows if r['candidate_key']==c['field']+':'+cid)
        assert r['form_id']==c['form_id']
        if c['status']=='conditional_analogue':assert r['placement_status']=='conditional_analogue'
receipt=dict(status='export_and_accounting_checks_passed',candidate_rows=len(rows),primary_retrieval_rows=len(pull),coverage_cells=len(cells),primary_forms_present=17,three_candidate_cells=summary['cells_with_three_direct_candidates'],doi_lines=len(expected_doi),ris_records=ris.count('ER  - '),prominence_signals=dict(Counter(r['prominence_signal'] for r in rows)),copy_states=dict(Counter(r['existing_copy_status'] for r in rows)),limits='Checks exact stored identifiers, source-file freshness, references and export counts. Not a fresh verification of every citation, source-copy completeness, form eligibility, readership or writing quality.',artifact_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='validation.json' and '__pycache__' not in p.parts})
(ROOT/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='artifact_sha256'},indent=2))
