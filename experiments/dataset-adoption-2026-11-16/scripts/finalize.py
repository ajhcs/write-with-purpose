"""Consolidate acquisition receipts and verify derived research artifacts."""
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[1]

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block:=stream.read(1024*1024):h.update(block)
    return h.hexdigest()


def main():
    records=[]
    for filename in ['acquisition.json','followup-acquisition.json','identity-corrections.json']:
        d=json.loads((BASE/filename).read_text())
        for r in d['records']:
            item=dict(r,receipt_file=filename)
            if item['id']=='scidtb-paper':
                item.update(status='rejected_wrong_identity',superseded_by='scidtb-paper-correct',
                            identity_note='D18-1388 is a different paper. The corrected SciDTB P18-2071 PDF is separately retained.')
            if item['id']=='echr':item['resolved_by']='echr-main'
            records.append(item)
    # A research agent retrieved this same original guide independently; retain its receipt too.
    guide=Path('/workspace/repos/builderbob/.writing-corpus-cache/dataset-adoption-2026-11-16/scientific-codebooks/MuLMS-AZ_Guidelines.pdf')
    if guide.exists():
        records.append({'id':'mulms-guide-independent','type':'codebook','status':'downloaded','local_path':str(guide),
                        'download':{'requested_url':'https://raw.githubusercontent.com/boschresearch/mulms-az-codi2023/main/annotation%20guidelines/MuLMS-AZ_Guidelines.pdf','sha256':sha(guide),'bytes':guide.stat().st_size},
                        'receipt_file':'scientific agent message and crosswalk; duplicate guide is not an independent codebook'})
    checked=0
    for r in records:
        if r['status']!='downloaded':continue
        p=Path(r['local_path'])
        assert p.exists(),str(p)
        assert sha(p)==r['download']['sha256'],r['id']
        checked+=1
    failures=[r for r in records if r['status']=='unavailable' and not r.get('resolved_by')]
    (BASE/'acquisition-index.json').write_text(json.dumps({
        'created_utc':datetime.now(timezone.utc).isoformat(),'purpose':'Downloaded bytes and access outcomes; package contents and analysis readiness require source-specific inspection.',
        'artifact_records':len(records),'downloaded_records':checked,
        'downloaded_bytes_including_reused_and_duplicate_artifacts':sum(r['download']['bytes'] for r in records if r['status']=='downloaded'),
        'remaining_endpoint_failures':[r['id'] for r in failures],
        'warning':'Multiple codebooks, converted annotations and overlapping releases are not independent samples. Rejected wrong-identity paper is excluded from acquired-codebook counts.',
        'records':records},indent=2)+'\n')
    text='# Remaining access and format gaps\n\nThese are unresolved endpoints after the current attempts, not proof of a paywall. Original failures and later resolutions remain in the [acquisition index](acquisition-index.json).\n\n| Resource | Outcome | Next route |\n| --- | --- | --- |\n'
    for r in failures:
        route='Authoritative data release or maintainer-provided copy' if r['id'].startswith('build-') else 'Institutional author version or library article access'
        text+='| '+r['id']+' | '+r.get('error','Unavailable').replace('|','/')+' | '+route+' |\n'
    text+='\nBUILD definitions and source code were downloaded, but its train/dev files returned 401. The existing [research access list](../prior-work-reuse-2026-11-16/paywalled-research.md) supplies exact article citations and DOIs. Moreno & Swales: **10.1016/j.esp.2017.11.006**. The complete Nathan thesis is downloaded even though its separate options article endpoint failed.\n\nSciPara\'s source archive and pickle are downloaded, but the pickle is unopened and no usable annotation rows are claimed. An interoperable text/JSON/CSV export and clear rights would resolve that format gap. The semantic essay extension is downloaded, but its underlying AAE text release and custom terms are not acquired through that extension.\n\nCoreSC/ART and DrInventor methods papers are downloaded; complete annotated corpus releases and their operative terms were not established in this acquisition. Licensed RST-DT/PDTB source text is not reconstructed from placeholders. The public PDTB annotation manual is downloaded. No claim of exhaustive access to every resource in the earlier bibliography is made.\n'
    (BASE/'remaining-access.md').write_text(text)
    funcs={x['id'] for x in json.loads((REPO/'docs/writing-harness/paragraph-functions.json').read_text())['functions']}
    d=json.loads((BASE/'crosswalk.json').read_text());rows=d['records']
    assert len(rows)==159 and len({r['id'] for r in rows})==159
    for r in rows:
        assert r['mapping_kind'] in {'conditional','partial','none','relation_only'}
        assert all(c['function_id'] in funcs for c in r['function_candidates'])
        if r['mapping_kind'] in {'none','relation_only'}:assert r['function_candidates']==[]
    for item in d['source_reviews']:assert sha(BASE/item['path'])==item['sha256']
    with (BASE/'crosswalk.csv').open(newline='') as stream:csvrows=list(csv.DictReader(stream))
    assert len(csvrows)==159 and [r['id'] for r in csvrows]==[r['id'] for r in rows]
    for a,b in zip(rows,csvrows):
        assert b['candidate_functions']=='; '.join(c['function_id'] for c in a['function_candidates'])
    profiles=json.loads((BASE/'source-profiles.json').read_text())['profiles']
    gum=next(r for r in profiles if r['dataset']=='GUM/eRST')
    for label,n in gum['all_relation_attribute_counts'].items():
        assert n==gum['primary_attachment_label_counts'].get(label,0)+gum['secondary_edge_label_counts'].get(label,0)
    readme=next(r for r in profiles if r['dataset']=='READMEClassifier')
    assert readme['raw_rows']-readme['excluded_rows']==readme['coded_rows']==4226
    assert readme['active_file_ids']==393 and readme['bundled_markdown_files']==441
    for p in BASE.rglob('*.json'):json.loads(p.read_text())
    receipt={'verified_utc':datetime.now(timezone.utc).isoformat(),'artifact_hashes_verified':checked,
             'comparison_rows':len(rows),'mapping_kinds':dict(Counter(r['mapping_kind'] for r in rows)),
             'source_review_hashes_verified':len(d['source_reviews']),'json_csv_rows_agree':True,
             'source_profile_count':len(profiles),'gum_primary_secondary_reconcile':True,
             'scope':'Transport hashes, structure, observed counts and metadata consistency only. Function mappings and writing norms remain unvalidated.'}
    (BASE/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__=='__main__':main()
