"""Reconcile real files, preserve identity evidence, and export library remainder."""
from collections import Counter
import csv
import io
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile
import retrieve as rt

BUILD=Path('/workspace/build/builderbob/write-with-purpose/library-retrieval-2026-11-16')


def write_csv(path,rows):
    fields=['candidate_key','field','form','title','authors','year','doi','doi_url','publisher_or_locator','status','preferred_format','preferred_file','bundle_file','source_url','selection_basis','version_note','reason_remaining','candidate_files_retained','alternative_doi_from_registry']
    with path.open('w',newline='')as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader()
        for row in rows:
            writer.writerow({k:('\''+str(v)if str(v).startswith(('=','+','-','@'))else v)for k,v in row.items()if k in fields})


def main():
    rows=json.loads((rt.ROOT/'input-manifest.json').read_text())['rows']
    lookup={r['candidate_key']:r for r in rows}
    files={k:[]for k in lookup};records={k:[]for k in lookup};problems=[]
    for p in sorted((rt.CACHE/'records').rglob('result.json')):
        rec=json.loads(p.read_text());k=rec['candidate_key'];records[k].append({'receipt':str(p),**rec})
        for item in rec['files']:
            path=Path(item['path'])
            if not path.exists()or rt.digest(path.read_bytes())!=item['sha256']:
                problems.append({'candidate_key':k,'path':str(path),'reason':'declared_file_missing_or_hash_changed'});continue
            files[k].append(item)
    assert not problems,problems
    inspections={r['path']:r for r in json.loads((rt.ROOT/'file-inspections.json').read_text())}
    manual={r['path']:r for r in json.loads((rt.ROOT/'manual-pdf-decisions.json').read_text())}
    native=json.loads((rt.ROOT/'native-fulltext-decisions.json').read_text())
    if (rt.ROOT/'extra-native-decisions.json').exists():native+=json.loads((rt.ROOT/'extra-native-decisions.json').read_text())
    for f in native:
        assert rt.digest(Path(f['path']).read_bytes())==f['sha256']
        files[f['candidate_key']].append(f)
    ledger=[];export=[];accepted_files={}
    for row in rows:
        k=row['candidate_key'];accepted=[];rejected=[]
        for original in files[k]:
            f=dict(original);path=f['path'];fmt=f['format'];basis=None;priority=0
            if fmt=='pdf':
                inspected=inspections.get(path,{})
                if path in manual:
                    assert manual[path]['sha256']==f['sha256'];basis='source_specific_parent_review';priority=6
                    f['additional_identity_review']=manual[path]
                elif inspected.get('title_author_same_page_hits'):
                    basis='complete_normalized_title_and_author_surname_on_same_front_page';priority=4
                    f['additional_identity_review']=inspected
                elif f.get('source_identity',{}).get('status')=='consistent':basis='skill_front_matter_title_identifier_author_consistent';priority=5
                if basis and k=='business:business_022'and (f.get('page_count')or 0)>40:
                    rejected.append({**f,'disposition':'book_length_copy_not_the_2010_HBR_essay'});continue
                if basis and (f.get('page_count')or 0)>80 and path not in manual:
                    rejected.append({**f,'disposition':'long_document_needs_work_type_extent_review'});continue
            elif fmt=='xml':
                tree=ET.fromstring(Path(path).read_bytes());ids=[''.join(n.itertext()).strip().casefold()for n in tree.findall('.//article-id')if n.get('pub-id-type')=='doi']
                body=tree.find('.//body')
                if row['doi'].casefold()in ids and body is not None:
                    basis='doi_matched_JATS_article_with_body';priority=3
            elif fmt=='html'and f in native:
                basis=f['identity'];priority=2
            elif fmt=='rst'and f.get('origin')=='official_pinned_source':basis='official_registered_commit_and_source_path';priority=2
            elif fmt=='txt'and f.get('origin')=='official_RFC_text':basis='official_RFC_document_identifier_title_date';priority=2
            if basis:
                accepted.append({**f,'selection_basis':basis,'priority':priority})
            else:rejected.append({**f,'disposition':'not_accepted_by_bounded_identity_and_scope_checks'})
        accepted.sort(key=lambda f:(-f['priority'],f['bytes']))
        # Preserve multiple versions in the ledger; deliver one preferred copy per work.
        selected=accepted[0]if accepted else None
        aliases=[]
        for rec in records[k]:
            value=rec.get('resolved_crossref_doi')
            if value and value.casefold()!=row['doi'].casefold():aliases.append(value)
        reason=''if selected else 'No matching complete copy obtained through the attempted public routes; use library access or inspect retained candidates.'
        if k=='business:business_022'and not selected:reason='Requested 2010 HBR essay still needed; existing 168-page Christensen/Allworth/Dillon book is a different work.'
        version_note='Same-work title/author or explicit review corroborated; exact publisher edition and completeness not independently certified for every file. Manuscripts/reprints remain identifiable by source.'if selected else''
        if selected and selected['format']=='rst':version_note='Exact registered source commit; full source-file container retained. Select the requested tutorial/reference entry before paragraph analysis.'
        if selected and selected['format']=='html':version_note='Original full HTML page; surrounding furniture retained, external figure/style assets not mirrored. No PDF layout inferred.'
        out={'candidate_key':k,'field':row['field'],'form':row['form_name'],'title':row['title'],'authors':'; '.join(json.loads(row['authors'])),'year':row['year'],'doi':row['doi'],'doi_url':'https://doi.org/'+row['doi']if row['doi']else'','publisher_or_locator':row['stable_url'],'status':'retrieved'if selected else'remaining','preferred_format':selected['format']if selected else'','preferred_file':selected['path']if selected else'','bundle_file':'','source_url':selected.get('source_url','')if selected else'','selection_basis':selected['selection_basis']if selected else'','version_note':version_note,'reason_remaining':reason,'candidate_files_retained':'; '.join(f['path']for f in files[k]),'alternative_doi_from_registry':'; '.join(sorted(set(aliases)))}
        if selected:
            h=selected['sha256'];title=re.sub(r'[^A-Za-z0-9]+','-',row['title']).strip('-')[:85]
            ext={'pdf':'pdf','xml':'xml','html':'html','rst':'rst','txt':'txt'}[selected['format']]
            name=accepted_files.get(h,{}).get('bundle_file')or f'fulltexts/{row["field"]}/{title}-{h[:10]}.{ext}'
            accepted_files[h]={'bundle_file':name,'path':selected['path'],'sha256':h,'bytes':selected['bytes'],'format':selected['format']}
            out['bundle_file']=name
        export.append(out);ledger.append({'request':row,'selected':selected,'accepted_copies':accepted,'retained_unaccepted_candidates':rejected,'attempt_receipts':[r['receipt']for r in records[k]],'status':out['status']})
    acquired=[r for r in export if r['status']=='retrieved'];remaining=[r for r in export if r['status']=='remaining'];doi=[r for r in export if r['doi']]
    summary={'generated_at_utc':rt.now(),'requested_works':len(rows),'doi_works':len(doi),'doi_retrieved':sum(r['status']=='retrieved'for r in doi),'doi_remaining':sum(r['status']=='remaining'for r in doi),'additional_non_doi_works':sum(not r['doi']for r in export),'additional_retrieved':sum(not r['doi']and r['status']=='retrieved'for r in export),'additional_remaining':sum(not r['doi']and r['status']=='remaining'for r in export),'all_retrieved':len(acquired),'all_remaining':len(remaining),'preferred_format_counts':dict(Counter(r['preferred_format']for r in acquired)),'by_field':{field:{'requested':sum(r['field']==field for r in export),'retrieved':sum(r['field']==field and r['status']=='retrieved'for r in export),'remaining':sum(r['field']==field and r['status']=='remaining'for r in export)}for field in sorted({r['field']for r in export})},'unique_delivered_files':len(accepted_files),'original_source_list_sha256':rt.digest((rt.REPO/'experiments/library-expansion-2026-11-16/library-pull-list.csv').read_bytes()),'source_identity_limits':'Original automatic warnings retained, supplemented by bounded layout/OCR title-author evidence and six explicit source reviews. Same work does not certify exact edition, authenticity or analytical suitability.','routes':'Europe PMC, OpenAlex, Crossref, registered publishers, title/author web searches, public author/institutional repositories, existing local candidates. Unpaywall skipped: no configured real contact email. Access and rate failures are preserved; no claim every possible Internet copy was exhausted.'}
    assert len(rows)==214 and len(doi)==154 and len(acquired)+len(remaining)==214
    summary['source_identity_limits']=f'Original automatic warnings retained, supplemented by bounded layout/OCR title-author evidence and {len(manual)} explicit source reviews. Same work does not certify exact edition, authenticity or analytical suitability.'
    rt.write_json(rt.ROOT/'retrieval-ledger.json',ledger);rt.write_json(rt.ROOT/'summary.json',summary)
    for name,subset in [('all-results.csv',export),('retrieved.csv',acquired),('remaining-doi.csv',[r for r in remaining if r['doi']]),('remaining-additional.csv',[r for r in remaining if not r['doi']]),('remaining-all.csv',remaining),('doi-text-without-pdf.csv',[r for r in acquired if r['doi']and r['preferred_format']!='pdf'])]:write_csv(rt.ROOT/name,subset)
    (rt.ROOT/'remaining-dois.txt').write_text('\n'.join(r['doi']for r in remaining if r['doi'])+'\n')
    ris=[]
    for r in remaining:
        raw=lookup[r['candidate_key']];ris+=['TY  - GEN','ID  - '+r['candidate_key'],'TI  - '+r['title']]
        ris+=['AU  - '+a for a in json.loads(raw['authors'])]
        if r['year']:ris+=['PY  - '+r['year']]
        if r['doi']:ris+=['DO  - '+r['doi']]
        ris+=['UR  - '+r['publisher_or_locator'],'N1  - '+r['reason_remaining'],'ER  - ','']
    (rt.ROOT/'remaining-library-pull.ris').write_text('\n'.join(ris))
    text=['# Remaining library retrievals','',f'The DOI list contains 154 works: {summary["doi_retrieved"]} matched copies obtained, **{summary["doi_remaining"]} remain**. The additional 60 non-DOI works have {summary["additional_retrieved"]} retrieved and {summary["additional_remaining"]} remaining.','', 'These are remaining retrieval requests, not a declaration that every work is paywalled. Blocked hosts, missing public copies, identity/version ambiguity and timeouts are distinguished in the receipts. Registry redirect DOIs are leads, not independently adjudicated aliases.','']
    for field in summary['by_field']:
        subset=[r for r in remaining if r['field']==field]
        text+=['## '+field.replace('_',' ').title(),'',f'{len(subset)} remaining works.','', '| Work | Author(s), year | DOI or locator |','| --- | --- | --- |']
        for r in subset:
            link='['+r['doi']+']('+r['doi_url']+')'if r['doi']else'[Source]('+r['publisher_or_locator']+')'
            text+=['| '+r['title'].replace('|','\\|')+' | '+r['authors'].replace('|','\\|')+'; '+r['year']+' | '+link+' |']
        text+=['']
    (rt.ROOT/'remaining-list.md').write_text('\n'.join(text)+'\n')
    BUILD.mkdir(parents=True,exist_ok=True)
    archive=BUILD/'retrieved-fulltexts.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=5)as z:
        for item in accepted_files.values():z.write(item['path'],item['bundle_file'])
        for name in ('retrieved.csv','remaining-doi.csv','remaining-additional.csv','remaining-library-pull.ris','summary.json'):z.write(rt.ROOT/name,'index/'+name)
    with zipfile.ZipFile(archive)as z:
        assert z.testzip()is None
        for f in accepted_files.values():assert rt.digest(z.read(f['bundle_file']))==f['sha256']
    delivery={'archive_path':str(archive),'archive_sha256':rt.digest(archive.read_bytes()),'archive_bytes':archive.stat().st_size,'unique_fulltext_files':len(accepted_files),'verified_archive_member_hashes':True,'files':list(accepted_files.values())}
    rt.write_json(rt.ROOT/'delivery.json',delivery)
    print(json.dumps({k:v for k,v in summary.items()if k not in ('routes','source_identity_limits','by_field')},indent=2))


if __name__=='__main__':main()
