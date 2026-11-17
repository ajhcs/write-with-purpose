"""Independent offline readback of request partitions and real delivered bytes."""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]


def read_csv(name):
    with (ROOT/name).open()as f:return list(csv.DictReader(f))


def main():
    summary=json.loads((ROOT/'summary.json').read_text());delivery=json.loads((ROOT/'delivery.json').read_text())
    allrows=read_csv('all-results.csv');got=read_csv('retrieved.csv');left=read_csv('remaining-all.csv');doi=read_csv('remaining-doi.csv');additional=read_csv('remaining-additional.csv')
    keys=lambda rows:{x['candidate_key']for x in rows}
    assert len(keys(allrows))==214
    assert keys(got).isdisjoint(keys(left))and keys(got)|keys(left)==keys(allrows)
    assert len(got)==summary['all_retrieved']and len(left)==summary['all_remaining']
    assert len(doi)==summary['doi_remaining']and len(additional)==summary['additional_remaining']
    assert sum(bool(x['doi'])for x in got)==summary['doi_retrieved']
    assert len(set((ROOT/'remaining-dois.txt').read_text().splitlines()))==len(doi)
    archive=Path(delivery['archive_path']);assert hashlib.sha256(archive.read_bytes()).hexdigest()==delivery['archive_sha256']
    with zipfile.ZipFile(archive)as z:
        assert z.testzip()is None
        for row in got:
            data=z.read(row['bundle_file']);assert data==Path(row['preferred_file']).read_bytes()
            if row['preferred_format']=='pdf':assert data.startswith(b'%PDF-')and len(data)>=10240
        assert len({x['bundle_file']for x in got})==delivery['unique_fulltext_files']
    ledger=json.loads((ROOT/'retrieval-ledger.json').read_text())
    for row in ledger:
        f=row['selected']
        if f:assert f['sha256']==hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()
        if row['request']['candidate_key']=='business:business_022':assert row['status']=='remaining'
    original=REPO/'experiments/library-expansion-2026-11-16/library-pull-list.csv'
    assert hashlib.sha256(original.read_bytes()).hexdigest()==summary['original_source_list_sha256']
    result={'status':'pass','validated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requested_rows':len(allrows),'retrieved_works':len(got),'remaining_works':len(left),'doi_retrieved':summary['doi_retrieved'],'doi_remaining':len(doi),'additional_retrieved':summary['additional_retrieved'],'additional_remaining':len(additional),'unique_fulltext_archive_members':delivery['unique_fulltext_files'],'archive_crc':'pass','all_selected_hashes_and_archive_mappings':'pass','original_shortlist_csv_unchanged':True,'book_not_counted_as_HBR_essay':True,'scope':'Mechanical partitions, actual retained bytes, archive integrity and declared provenance; not independent semantic or publication-authenticity certification.'}
    (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
