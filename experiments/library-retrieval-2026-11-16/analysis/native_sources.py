"""Explicit official source downloads and reviewed full-HTML registrations."""
import concurrent.futures
import csv
import json
from pathlib import Path
import retrieve as rt

ACCEPT_HTML={
    'medicine:medicine-methods_paper-3','medicine:medicine-procedure_how_to-1',
    'medicine:medicine-tutorial-2','medicine:medicine-theory_conceptual_paper-1',
    'medicine:medicine-scoping_review-1','medicine:medicine-conceptual_explainer-3',
    'medicine:medicine-case_report-2','medicine:medicine-conceptual_explainer-2',
    'law:law_w2177794968','law:law_w2058917614',
    'personal:p01','personal:p08','personal:p10','personal:p11','personal:p12',
    'physical-sciences:psm_02','physical-sciences:psm_03',
    'physical-sciences:psm_29','physical-sciences:psm_31',
}


def raw_source(row):
    directory=rt.CACHE/'records'/rt.key(row)/'native';directory.mkdir(exist_ok=True)
    result=directory/'result.json'
    if result.exists():return json.loads(result.read_text())
    rec={'candidate_key':row['candidate_key'],'doi':row['doi'],'title':row['title'],'field':row['field'],'form':row['form_name'],'started_at_utc':rt.now(),'files':[],'attempts':[],'status':'not_retrieved'}
    url=row['stable_url'].replace('github.com/','raw.githubusercontent.com/').replace('/blob/','/').split('#')[0]
    data,final,ct=rt.request(url,rec,'official_pinned_source_corrected_url_construction')
    if data and len(data)>100 and not data.lstrip().startswith(b'<'):
        p=directory/'source.rst';p.write_bytes(data)
        rec['files'].append({'path':str(p),'format':'rst','sha256':rt.digest(data),'bytes':len(data),'source_url':final,'origin':'official_pinned_source','identity':'Exact registered repository, commit and path; whole file retained. A source-file container may contain several requested reference entries.','scope_note':'Source, not a publisher-rendered PDF; source-file sections remain to select before paragraph analysis.'})
        rec['status']='downloaded_source'
    rec['finished_at_utc']=rt.now();rt.write_json(result,rec);return rec


def main():
    rows=list(csv.DictReader((rt.REPO/'experiments/library-expansion-2026-11-16/library-pull-list.csv').open()))
    selected=[];seen=set()
    for h in json.loads((rt.CACHE/'html-inspections.json').read_text()):
        k=h['candidate_key']
        if k not in ACCEPT_HTML or k in seen or not h['possible_fulltext_for_review']:continue
        row=next(r for r in rows if r['candidate_key']==k)
        if row['doi']and not h['doi_match']:continue
        if not h['author_in_page']or h['paywall_marker']:continue
        seen.add(k)
        selected.append({'candidate_key':k,'path':h['path'],'format':'html','sha256':h['sha256'],'bytes':Path(h['path']).stat().st_size,'source_url':h['source_url'],'origin':'retained_public_full_page','identity':'citation_doi_matches_requested_work'if row['doi']else'registered_source_url_title_author_context_review','scope_note':'Original complete HTML page retained, including references and surrounding page furniture. Body extraction is provisional; this is not a validated paragraph corpus.','body_prose_words_approximate':h['prose_words'],'review_basis':'Inspected beginning/end, metadata, article context and absence of access barrier; actual page furniture may remain. Not an independent check of source truth.'})
    rt.write_json(rt.ROOT/'native-fulltext-decisions.json',selected)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        rr=list(pool.map(raw_source,[r for r in rows if 'github.com/'in r['stable_url']and '/blob/'in r['stable_url']]))
    print(json.dumps({'registered_full_html_works':len(selected),'official_pinned_sources':sum(r['status']=='downloaded_source'for r in rr)}))


if __name__=='__main__':main()
