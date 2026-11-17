#!/usr/bin/env python3
"""Build a field/form retrieval ledger without claiming full-text eligibility."""
import csv
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
REPO=ROOT.parent.parent
FIELDS=['business','engineering','law','medicine','personal','physical-sciences']
FIELD_NAMES={'business':'Business and management','engineering':'Engineering and computing','law':'Law and public policy','medicine':'Medicine and health','personal':'Personal and public writing','physical-sciences':'Physical sciences and mathematics'}

def read(p):return json.loads(Path(p).read_text())
def doi_key(v):
    if not v:return None
    return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)','',v.strip(),flags=re.I).casefold().rstrip(' .')
def title_key(v):return ''.join(c for c in html.unescape(v or '').casefold() if c.isalnum())
def authors(v):return v if isinstance(v,list) else [v] if v else []
def source_urls(v):return [x if isinstance(x,str) else x.get('query_url') or x.get('url') or str(x) for x in v or []]
def write_csv(path,rows,keys):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');writer.writeheader()
        for r in rows:
            out={k:json.dumps(r.get(k),ensure_ascii=False) if isinstance(r.get(k),(list,dict)) else r.get(k) for k in keys}
            writer.writerow({k:"'"+v if isinstance(v,str) and v[:1] in '=+-@' else v for k,v in out.items()})

def build():
    contract=read(ROOT/'selection-contract.json');forms={r['id']:r['name'] for r in contract['forms']}
    overrides=read(ROOT/'parent-overrides.json')['records']
    prior=REPO/'experiments/corpus-analysis-2026-11-16'
    inventory=list(csv.DictReader((prior/'results/document-inventory.csv').open()))
    strong_doi=defaultdict(list);strong_title=defaultdict(list)
    for r in inventory:
        if r['has_measurement']=='True' and r['source_format'] in ('xml','html'):
            if r['doi']:strong_doi[doi_key(r['doi'])].append(r['record_id'])
            if len(r['title'].split())>=4:strong_title[title_key(r['title'])].append(r['record_id'])
    for r in read(REPO/'experiments/pattern-test-2026-11-16/results/documents.json'):
        strong_title[title_key(r['title'])].append(r['id'])
        if r.get('doi'):strong_doi[doi_key(r['doi'])].append(r['id'])
    weak_doi=defaultdict(list);weak_title=defaultdict(list)
    for line in (prior/'analysis/pdf-records.jsonl').read_text().splitlines():
        r=json.loads(line);m=r['source_metadata']
        if m.get('doi'):weak_doi[doi_key(m['doi'])].append(r['record_id'])
        if m.get('title'):weak_title[title_key(m['title'])].append(r['record_id'])
    legacy_doi={doi_key(r['doi']) for r in read(prior/'results/legacy-derived-register.json') if r.get('doi')}
    rows=[];cells=[];source_hashes={}
    for field in FIELDS:
        candidate_path=ROOT/field/'candidates.json';coverage_path=ROOT/field/'coverage.json'
        records=read(candidate_path);coverage=read(coverage_path);ids={r['id']:r for r in records}
        assert len(ids)==len(records)
        assert len(coverage)==17 and {c['form_id'] for c in coverage}==set(forms)
        placement={}
        for c in coverage:
            assert len(c['candidate_ids'])==c['provided'] and len(set(c['candidate_ids']))==c['provided']
            if c['status']=='three_targets':assert c['provided']==3
            for cid in c['candidate_ids']:
                assert cid in ids and ids[cid]['form_id']==c['form_id']
                placement[cid]=c['status']
            cells.append(dict(field=field,field_name=FIELD_NAMES[field],**c,form_name=forms[c['form_id']]))
        for raw in records:
            r=dict(raw);key=f'{field}:{r["id"]}'
            correction=overrides.get(key,{})
            if correction:
                r['parent_correction']=correction
                r.update(correction)
            r['branch']=field;r['candidate_key']=key;r['authors']=authors(r.get('authors'))
            r['doi']=doi_key(r.get('doi'));r['form_name']=forms[r['form_id']]
            assert not r['doi'] or re.match(r'^10\.\d{4,9}/\S+$',r['doi']),key
            r['coverage_status']=placement.get(r['id'],'not_counted_alternate')
            r['placement_status']='conditional_analogue' if r['coverage_status']=='conditional_analogue' or 'conditional_analogue' in r.get('form_status','') else 'not_counted_alternate' if r['coverage_status']=='not_counted_alternate' else 'primary_candidate'
            strong=strong_doi.get(r['doi'],[]) if r['doi'] else []
            titles=[r['title'],raw['title'],*r.get('alternate_titles',[])]
            if not strong:strong=[match for title in titles for match in strong_title.get(title_key(title),[])]
            weak=weak_doi.get(r['doi'],[]) if r['doi'] else []
            if not weak:weak=[match for title in titles for match in weak_title.get(title_key(title),[])]
            r['existing_source_matches']=sorted(set(strong or weak))
            if strong:r['existing_copy_status']='retained_body_or_reviewed_reconstruction'
            elif weak:r['existing_copy_status']='retained_PDF_candidate_identity_or_completeness_unresolved'
            elif r['doi'] in legacy_doi:r['existing_copy_status']='legacy_measurements_only_source_copy_needed'
            else:r['existing_copy_status']='no_match_in_retained_source_indices'
            r['copy_match_limit']='Exact DOI or normalized title only; unknown aliases, short titles and different editions can leave undetected overlap.'
            r['library_pull_action']='review_existing_first' if strong else 'review_candidate_or_pull_publisher_copy' if weak else 'pull_complete_source'
            y=r.get('year')
            try:y=int(y)
            except (ValueError,TypeError):y=None
            r['year']=y;r['period']='pre-2015' if y and y<2015 else '2015-2019_supplement' if y and y<2020 else '2020-onward_comparison' if y else 'unknown_date'
            signal=(str(r.get('selection_signal_type',''))+' '+str(r.get('selection_evidence',''))+' '+str(r.get('prominence_tier',''))).casefold()
            if 'no_prominence_evidence' in signal or 'no individual prominence' in signal or 'unquantified' in signal:r['prominence_signal']='relevant_source_without_individual_prominence_evidence'
            elif 'access' in signal and any(x in signal for x in ['publisher','readership']):r['prominence_signal']='publisher_access_signal_not_unique_readers'
            elif r.get('citation_count') is not None:r['prominence_signal']='documented_citation_count_not_readership'
            elif any(x in signal for x in ['award','editorial','bestsell','nobel','pulitzer','asme','longreads']):r['prominence_signal']='named_editorial_award_or_bestseller_signal'
            else:r['prominence_signal']='institutional_or_contextual_selection_no_readership_measure'
            r['identifier_status']='doi_supplied_with_branch_verification_status' if r['doi'] else 'doi_not_identified_or_withheld_see_verification'
            r['work_key']='doi:'+r['doi'] if r['doi'] else 'title:'+title_key(r['title'])+'|'+str(y)+'|'+title_key(';'.join(r['authors']))
            r['source_file']=str(candidate_path.relative_to(REPO))
            rows.append(r)
        for path in (candidate_path,coverage_path):source_hashes[str(path.relative_to(REPO))]=hashlib.sha256(path.read_bytes()).hexdigest()
    assert len(cells)==102
    primary=[r for r in rows if r['placement_status']=='primary_candidate']
    pull=[r for r in primary if r['library_pull_action']!='review_existing_first']
    existing=[r for r in primary if r['library_pull_action']=='review_existing_first']
    conditional=[r for r in rows if r['placement_status']!='primary_candidate']
    keys=['candidate_key','field','form_id','form_name','title','authors','year','period','venue','volume','issue','pages','doi','stable_url','retrieval_locator','selection_signal_type','selection_evidence','citation_count','citation_provider','citation_snapshot','prominence_signal','verification_status','verification_sources','form_status','form_basis','existing_copy_status','existing_source_matches','library_pull_action','placement_status','date_notes','limitations']
    for name,data in [('candidate-ledger.csv',rows),('library-pull-list.csv',pull),('already-retained-review-first.csv',existing),('conditional-and-alternate-candidates.csv',conditional)]:write_csv(ROOT/name,data,keys)
    write_csv(ROOT/'coverage.csv',cells,['field','field_name','form_id','form_name','status','requested','provided','candidate_ids','reason'])
    (ROOT/'candidate-ledger.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'coverage.json').write_text(json.dumps(cells,indent=2,ensure_ascii=False)+'\n')
    unique={}
    for r in pull:unique.setdefault(r['work_key'],r)
    (ROOT/'dois-to-pull.txt').write_text('\n'.join(sorted({r['doi'] for r in pull if r['doi']}))+'\n')
    ris=[]
    for r in unique.values():
        ris.extend(['TY  - GEN','ID  - '+r['candidate_key'],'TI  - '+r['title']])
        ris.extend('AU  - '+a for a in r['authors'])
        if r['year']:ris.append('PY  - '+str(r['year']))
        for tag,key in [('T2','venue'),('VL','volume'),('IS','issue'),('SP','pages'),('DO','doi'),('UR','stable_url')]:
            if r.get(key):ris.append(tag+'  - '+str(r[key]).replace('\n',' '))
        ris.append('KW  - '+r['field']);ris.append('KW  - '+r['form_name'])
        ris.append('N1  - '+('Form provisional; '+r['verification_status']+'; '+r['retrieval_locator']+'; '+r['selection_evidence']).replace('\n',' '))
        ris.extend(['ER  - ',''])
    (ROOT/'library-pull-list.ris').write_text('\n'.join(ris))
    # Append only: preserve any existing pool entries, per search-lit contract.
    bib=ROOT/'references/library.bib';old=bib.read_text() if bib.exists() else ''
    def esc(s):return str(s).replace('\\','\\textbackslash{}').replace('{','\\{').replace('}','\\}').replace('&','\\&')
    entries=[]
    for r in unique.values():
        token=hashlib.sha256(r['work_key'].encode()).hexdigest()[:12];marker='% expansion-key: '+token
        if marker in old:continue
        v=r['verification_status'].casefold()
        api_verified=bool(r['doi'] and ('crossref' in v and 'not independently' not in v or 'pubmed metadata' in v or 'pubmed+europe' in v))
        values={'title':r['title'],'author':' and '.join(r['authors']),'year':r['year'],'howpublished':r.get('venue'),'doi':r['doi'],'url':r.get('stable_url'),'verified':'true' if api_verified else 'false','verified_by':r['verification_status'],'verified_on':'2026-11-16','note':'Retrieval candidate; form and full-text suitability provisional. '+r['retrieval_locator']}
        entries.append(marker+'\n@misc{Library_'+token+',\n'+''.join('  '+k+' = {'+esc(value)+'},\n' for k,value in values.items() if value is not None)+'}\n')
    if entries:
        with bib.open('a') as f:f.write('\n'.join(entries))
    summary=dict(fields=6,forms=17,field_form_cells=102,raw_candidate_records=len(rows),distinct_candidate_work_keys=len({r['work_key'] for r in rows}),primary_placements=len(primary),primary_pull_placements=len(pull),distinct_primary_pull_works=len(unique),doi_pull_count=len({r['doi'] for r in pull if r['doi']}),primary_pull_without_doi=sum(not r['doi'] for r in unique.values()),already_retained_primary_placements=len(existing),conditional_or_uncounted_records=len(conditional),cells_with_three_direct_candidates=sum(c['status']=='three_targets' for c in cells),cell_statuses=dict(Counter(c['status'] for c in cells)),periods_all=dict(Counter(r['period'] for r in rows)),by_field={f:dict(records=sum(r['branch']==f for r in rows),primary_placements=sum(r['branch']==f for r in primary),pull_placements=sum(r['branch']==f for r in pull),three_target_cells=sum(c['field']==f and c['status']=='three_targets' for c in cells)) for f in FIELDS},raw_input_sha256=source_hashes,limits='Bibliographic candidates, not verified writing exemplars. Primary source/API metadata checks are branch-specific; audit rechecks were rate limited. Prominence signals differ and do not establish readership or quality. No PDF acquisition or catalogue adoption in this task.')
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    # A readable 17-form matrix, including gaps and retained copies.
    by_key={r['candidate_key']:r for r in rows}
    text=['# Library retrieval shortlist','', 'All seventeen forms were assessed in each of six source groups. Three direct candidates are supplied where the source search supports them; gaps and conditional analogues remain explicit. All form assignments await full-text review.','', 'Use `library-pull-list.csv` for new or uncertain copies; `already-retained-review-first.csv` avoids requesting known retained bodies. `conditional-and-alternate-candidates.csv` preserves related but non-equivalent examples. Counts of accesses, citations and editorial selections are different signals.','']
    for field in FIELDS:
        text.extend(['## '+FIELD_NAMES[field],''])
        for c in [x for x in cells if x['field']==field]:
            text.extend(['### '+c['form_name'],'',f'Status: {c["status"]}; {c["provided"]}/3 candidate records. '+c['reason'],''])
            for cid in c['candidate_ids']:
                r=by_key[field+':'+cid];identifier='DOI: `'+r['doi']+'`' if r['doi'] else 'DOI not identified/withheld; use the locator below.'
                text.extend(['- **'+r['title']+'** — '+'; '.join(r['authors'])+f' ({r["year"] or "date unresolved"}). '+str(r['venue'])+'. '+identifier,
                    '  - Retrieve: '+r['retrieval_locator'],
                    '  - Selection: '+r['selection_evidence'],
                    '  - Source: '+str(r.get('stable_url')),
                    '  - Copy: '+r['existing_copy_status']+'; '+r['library_pull_action']+'. Form: '+r['form_status']+'.',
                    '  - Limits/version: '+r.get('date_notes','')+' '+r.get('limitations','')])
            text.append('')
    (ROOT/'shortlist.md').write_text('\n'.join(text)+'\n')
    batch=[]
    for field in FIELDS:
        pool=[r for r in pull if r['branch']==field and r['existing_copy_status']=='no_match_in_retained_source_indices']
        wanted=['personal_reflective_essay','argument_perspective','critical_review_of_work'] if field=='personal' else ['argument_perspective','narrative_critical_literature_review','systematic_review']
        selected=set()
        for form in wanted:
            options=[r for r in pool if r['form_id']==form and r['work_key'] not in selected]
            if not options:
                options=[r for r in pool if r['form_id']=='theory_conceptual_paper' and r['work_key'] not in selected]
            if options:
                chosen=max(options,key=lambda r:(r['period']=='pre-2015',r.get('citation_count') or 0))
                selected.add(chosen['work_key']);batch.append(chosen)
    write_csv(ROOT/'first-pull-batch.csv',batch,keys)
    first=['# First retrieval batch','', 'Three candidates per source group to start with contrasting forms. These eighteen are a starting order, not a replacement for the full seventeen-form list. Prefer the exact version and retrieve the complete article, including references and supplements where available. Metadata and attention signals do not establish writing quality.','']
    for field in FIELDS:
        first.extend(['## '+FIELD_NAMES[field],''])
        for r in batch:
            if r['branch']!=field:continue
            first.extend(['- **'+r['title']+'** — '+'; '.join(r['authors'])+f' ({r["year"]}). '+r['form_name']+'.',
                '  - '+('DOI: `'+r['doi']+'`' if r['doi'] else 'No DOI identified: '+r['retrieval_locator']),
                '  - '+str(r['stable_url']), '  - Selection evidence: '+r['selection_evidence']])
        first.append('')
    (ROOT/'first-pull-batch.md').write_text('\n'.join(first)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('raw_input_sha256','by_field','limits')},indent=2))

if __name__=='__main__':build()
