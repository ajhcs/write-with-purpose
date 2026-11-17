#!/usr/bin/env python3
"""Measure every locally cached JATS XML file; never fetch source material."""
import csv, hashlib, json, re, sys, traceback
from collections import Counter, defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
from metrics import measure_document, word_tokens, summarize

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent/'form-corpus-2026-11-16'
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache')
ROOTS={k:CACHE/k for k in ('case-protocol','empirical-methods','narrative-scoping')}
ROOTS['systematic-review']=Path('/workspace/tmp/builderbob/writing-corpus/systematic-review')
ROOTS['biomedical-essays']=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16')
OUTCACHE=CACHE/'analysis'/'xml'
ADMIN={x.casefold() for x in ['acknowledgment','acknowledgments','acknowledgement','acknowledgements','author contributions','authors contributions',"authors' contributions",'author contribution','author information','authors information','funding','funding information','funding statement','financial support','data availability','data availability statement','availability of data','availability of data and materials','declarations','declaration','ethics approval and consent to participate','ethics approval','ethical approval','ethics statement','ethics statements','consent for publication','patient consent for publication','competing interest','competing interests','conflict of interest','conflicts of interest','declaration of interests','declaration of competing interests','footnotes','associated data','pre-publication history','prepublication history','supplementary material','supplementary information','supplementary materials','abbreviations']}
OMIT={'fig','fig-group','table-wrap','table-wrap-group','caption','disp-formula','inline-formula','tex-math','mml:math','supplementary-material','boxed-text','ref-list','fn-group','alternatives','media','graphic','table','label'}
META_KEYS={'form','stratum','status','reason','retrieval_stage','classification_basis','search_query','search_order','search_rank','source_rank','rank_in_search','cited_by_count','citation_count','citation_snapshot_utc','source_publication_types','publication_types','source_type','jats_type','publisher_article_type','publisher_subject_labels','measured','supplement_pre2015','xml_status','year','publication_year','first_publication_date','source_sha256','xml_sha256','discovery_source','source_url','full_text_url'}
def tag(e):return e.tag.rsplit('}',1)[-1] if isinstance(e.tag,str) else ''
def text(e, skip_xrefs=False, omit=()):
    if e is None:return ''
    def rec(n):
        s=n.text or ''
        for c in n:
            if tag(c) not in omit and not (skip_xrefs and tag(c)=='xref'):s+=rec(c)
            s+=c.tail or ''
        return s
    return ' '.join(rec(e).split())
def find(e,path):return e.find(path) if e is not None else None
def manifests():
    idx=defaultdict(list)
    paths=[BASE/'case-protocol/manifest.jsonl',BASE/'systematic-review/manifest.jsonl']
    for p in paths:
        for line in p.read_text().splitlines():
            row=json.loads(line); pmc=row.get('pmcid')
            if pmc:idx[(p.parent.name,pmc.upper())].append({'manifest':str(p.relative_to(BASE)),**{k:v for k,v in row.items() if k in META_KEYS}})
    p=BASE/'empirical-methods/manifest.csv'
    with p.open(newline='') as f:
        for row in csv.DictReader(f):
            if row.get('pmcid'):idx[('empirical-methods',row['pmcid'].upper())].append({'manifest':str(p.relative_to(BASE)),**{k:v for k,v in row.items() if k in META_KEYS and v}})
    for p in sorted((BASE/'narrative-scoping').glob('*-candidates.json')):
        for row in json.loads(p.read_text()):
            if row.get('pmcid'):idx[('narrative-scoping',row['pmcid'].upper())].append({'manifest':str(p.relative_to(BASE)),**{k:v for k,v in row.items() if k in META_KEYS}})
    for filename in ('candidates.jsonl','measurements.jsonl'):
        p=BASE/'essays'/filename
        for line in p.read_text().splitlines():
            row=json.loads(line); pmc=row.get('pmcid')
            if pmc:
                keys=('form_candidate','source_query','source_rank','pubYear','firstPublicationDate','citedByCount','pubTypeList','retrieved_utc','sha256','extraction_status','error','article_type')
                idx[('biomedical-essays',pmc.upper())].append({'manifest':str(p.relative_to(BASE)),**{k:row[k] for k in keys if k in row}})
    return idx

def classify(title,typ,cats,metadata):
    signal=' '.join([title,typ,*cats]).lower()
    forms=[]
    for pattern,label in [(r'\b(?:systematic review|meta.analysis)\b','systematic_review'),(r'\bscoping review\b','scoping_review'),(r'\bnarrative review\b','narrative_review'),(r'\b(?:study protocol|review protocol|protocol)\b','protocol'),(r'\bcase (?:report|series|study)\b','case_report'),(r'\b(?:methods?|methodology)\b','methods_signal')]:
        if re.search(pattern,signal):forms.append(label)
    if 'protocol' in forms:forms=[x for x in forms if x not in {'systematic_review','scoping_review','narrative_review'}]
    if not forms and typ=='research-article':forms=['research_article_unspecified']
    if not forms and typ=='review-article':forms=['review_unspecified']
    return {'labels':forms or ['unspecified'],'basis':'provisional title and JATS type/category signals; protocol suppresses review label; no semantic verification','source_manifest_forms':sorted({str(x.get('form') or x.get('stratum')) for x in metadata if x.get('form') or x.get('stratum')})}

def process(path,cohort,metadata):
    raw=path.read_bytes(); sha=hashlib.sha256(raw).hexdigest(); root=ET.fromstring(raw)
    # JATS from these caches normally has no default namespace. Strip namespaces for consistent paths.
    for e in root.iter():
        if isinstance(e.tag,str):e.tag=tag(e)
    front=find(root,'./front/article-meta'); journal=find(root,'./front/journal-meta')
    ids=front.findall('./article-id') if front is not None else []
    doi=next((text(x) for x in ids if x.get('pub-id-type','').lower()=='doi'),'')
    doi=re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)','',doi.strip(),flags=re.I).lower().rstrip(' .') or None
    pmcid=next((text(x) for x in ids if x.get('pub-id-type','').lower() in ('pmc','pmcid')),'')
    pmcid=('PMC'+pmcid if pmcid and not pmcid.upper().startswith('PMC') else pmcid.upper()) or path.stem.upper()
    title=text(find(front,'./title-group/article-title'))
    authors=[]
    groups=front.findall('./contrib-group') if front is not None else []
    author_nodes=[a for group in groups for a in group.findall('./contrib') if a.get('contrib-type')=='author' or (not a.get('contrib-type') and group.get('content-type')=='author')]
    for a in author_nodes:
        name=find(a,'./name'); collab=find(a,'./collab')
        val=' '.join(filter(None,[text(find(name,'./given-names')),text(find(name,'./surname'))])) if name is not None else text(collab)
        if val:authors.append(val)
    dates=[]
    for d in (front.findall('./pub-date') if front is not None else []):
        y=text(find(d,'./year')); m=text(find(d,'./month')); day=text(find(d,'./day'))
        if y:dates.append({'year':y,'month':m or None,'day':day or None,'type':d.get('pub-type') or d.get('publication-format') or d.get('date-type')})
    years=[int(d['year']) for d in dates if re.fullmatch(r'\d{4}',d['year'])]
    cats=[text(x) for x in (front.findall('./article-categories//subject') if front is not None else []) if text(x)]
    typ=root.get('article-type','');body=find(root,'./body')
    r={'source_path':str(path),'source_sha256':sha,'pmcid':pmcid,'doi':doi,'title':title,'authors':authors,'journal':text(find(journal,'./journal-title-group/journal-title')) or None,'first_publication_year':min(years) if years else None,'publication_dates':dates,'source_article_type':typ or None,'source_categories':cats,'source_cohorts':[cohort],'source_manifest_metadata':metadata,'form':classify(title,typ,cats,metadata),'body_present':body is not None,'status':None,'exclusion_reasons':[],'extraction_limitations':['JATS structure and exact administrative headings may not identify all non-body or administrative prose','Automated form signals are provisional; no rhetorical functions or evidence roles inferred','Inline formula text and cross-reference display text excluded; sentence segmentation is heuristic','Preformatted text is excluded from prose and counted separately; it is not assumed to be code']}
    if body is None:r.update(status='excluded',exclusion_reasons=['no body element']);return r
    blocks=[];sections=[];admin=[];seq=0
    def add(kind, content, sid, **kw):
        if content:blocks.append({'kind':kind,'text':content,'section_id':sid,**kw})
    def walk(n,sid='__unsectioned__',level=0,kind=None):
        nonlocal seq
        t=tag(n)
        if t=='sec':
            heading=text(find(n,'./title')); clean=heading.strip().rstrip(':').strip().casefold()
            if clean in {'references','bibliography'}:return
            if clean in ADMIN:
                admin.append(n);return
            seq+=1; childid=f's{seq}'; sections.append({'id':childid,'parent_id':sid if sid!='__unsectioned__' else None,'heading':heading,'level':level+1})
            add('heading',heading,childid,heading_level=level+1)
            for c in n:
                if tag(c)!='title':walk(c,childid,level+1)
            return
        if t in OMIT:return
        if t=='list-item':
            # A list item is one block per direct paragraph; nested lists retain separate items.
            for c in n:walk(c,sid,level,'list_item')
            if n.text and n.text.strip():add('list_item',' '.join(n.text.split()),sid)
            return
        if t in ('disp-quote','speech'):kind='quote'
        if t=='preformat':return
        if t=='code':add('code',text(n,True,OMIT),sid);return
        if t=='p':
            add(kind or 'paragraph',text(n,True,OMIT|{'list','list-item','disp-quote','speech','code','preformat','p'}),sid)
            # nested special blocks are handled once, never as ordinary prose
            for c in n:
                if tag(c) in {'list','disp-quote','speech','code','preformat','p'}:walk(c,sid,level,kind)
            return
        for c in n:walk(c,sid,level,kind)
    walk(body)
    captions=[x for x in body.iter('caption')]
    caption_text=[text(x,True,{'caption'}) for x in captions]
    for s in caption_text:add('caption',s,'__captions__')
    refs=list(root.findall('./back//ref-list/ref'))+list(root.findall('./body//ref-list/ref'))
    # Object counts are explicit JATS elements, not inferred evidence roles.
    objects={'figures':len(list(body.iter('fig'))),'tables':len(list(body.iter('table-wrap'))),'references':len(refs),'bibliographic_xrefs':sum(x.get('ref-type')=='bibr' for x in body.iter('xref')),'external_links':len(list(body.iter('ext-link'))),'lists':len(list(body.iter('list')))}
    m=measure_document(blocks,objects)
    r['metrics']=m;r['sections']=sections
    r['separate_words']={'title':len(word_tokens(title)),'abstract':sum(len(word_tokens(text(x,True))) for x in (front.findall('./abstract') if front is not None else [])),'captions':sum(len(word_tokens(s)) for s in caption_text),'references':sum(len(word_tokens(text(x,True))) for x in refs),'excluded_administrative':sum(len(word_tokens(text(x,True,OMIT|{'title'}))) for x in admin),'preformatted':sum(len(word_tokens(text(x,True))) for x in body.iter('preformat'))}
    r['excluded_administrative_headings']=[text(find(x,'./title')) for x in admin]
    if m['prose_paragraphs']==0:r.update(status='excluded',exclusion_reasons=['no extracted body prose paragraphs'])
    else:r['status']='measured_provisional_form'
    cache=OUTCACHE/cohort/(path.stem+'.json');cache.parent.mkdir(parents=True,exist_ok=True)
    cache.write_text(json.dumps({'source_path':str(path),'source_sha256':sha,'pmcid':pmcid,'blocks':blocks},ensure_ascii=False)+'\n')
    r['text_cache_path']=str(cache)
    return r

def main():
    index=manifests(); rows=[]
    for cohort,root in ROOTS.items():
        for path in sorted(root.glob('*.xml')):
            try:r=process(path,cohort,index.get((cohort,path.stem.upper()),[]))
            except Exception as e:r={'source_path':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_cohorts':[cohort],'pmcid':path.stem,'status':'error','exclusion_reasons':[f'{type(e).__name__}: {e}']}
            rows.append(r)
    with (HERE/'xml-records.jsonl').open('w') as f:
        for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    good=[r for r in rows if r['status']=='measured_provisional_form']
    summary={'files_total':len(rows),'by_root':dict(Counter(r['source_cohorts'][0] for r in rows)),'status':dict(Counter(r['status'] for r in rows)),'body_present':sum(r.get('body_present',False) for r in rows),'errors':[{'source_path':r['source_path'],'reason':r['exclusion_reasons']} for r in rows if r['status']=='error'],'excluded':[{'source_path':r['source_path'],'reason':r['exclusion_reasons']} for r in rows if r['status']=='excluded'],'prior_four_root_files':sum(r['source_cohorts'][0]!='biomedical-essays' for r in rows),'duplicates_by_pmcid':sum(n-1 for n in Counter(r['pmcid'] for r in rows).values() if n>1),'duplicates_by_sha256':sum(n-1 for n in Counter(r['source_sha256'] for r in rows).values() if n>1),'prose_words':summarize([r['metrics']['prose_words'] for r in good]),'form_labels':dict(Counter(label for r in good for label in r['form']['labels']))}
    (HERE/'xml-summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:summary[k] for k in ('files_total','by_root','status','body_present','duplicates_by_pmcid')},indent=2))
if __name__=='__main__':main()
