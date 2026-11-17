#!/usr/bin/env python3
"""Fetch a reproducible bounded, citation-ordered Europe PMC sample and measure JATS."""
import concurrent.futures as cf, csv, hashlib, json, re, statistics as st, time, urllib.parse
from datetime import datetime, timezone
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
import requests

OUT=Path(__file__).resolve().parent
CACHE=Path('/workspace/tmp/builderbob/writing-corpus/systematic-review')
CACHE.mkdir(parents=True, exist_ok=True)
BASE='https://www.ebi.ac.uk/europepmc/webservices/rest'
QUERY='TITLE:"systematic review" AND OPEN_ACCESS:Y AND HAS_FT:Y'
PARAMS={'query':QUERY,'format':'json','pageSize':1000,'sort':'CITED desc','resultType':'core'}
TARGET=300
WORD=re.compile(r"\b[^\W_]+(?:[’'\-][^\W_]+)*\b",re.UNICODE)
SENT=re.compile(r'(?<=[.!?])(?:[\"\'”’)]*)\s+(?=[A-Z0-9(])')
EXCLUDE={'caption','fig','fig-group','table-wrap','table-wrap-group','table','supplementary-material','ref-list','list','boxed-text','disp-formula','inline-formula','tex-math','mml:math','xref','label'}
def local(tag): return tag.rsplit('}',1)[-1]
def flat(e, exclusions=()):
    parts=[]
    def visit(n):
        if local(n.tag) in exclusions: return
        if n.text: parts.append(n.text)
        for c in n:
            visit(c)
            if c.tail: parts.append(c.tail)
    visit(e)
    return ' '.join(parts)
def words(s): return WORD.findall(s)
def search():
    p=CACHE/'search.json'
    if not p.exists():
        r=requests.get(BASE+'/search',params=PARAMS,timeout=60);r.raise_for_status();p.write_text(r.text)
    return json.loads(p.read_text())
def fetch(i,item):
    pmc=item.get('pmcid'); title=item.get('title','')
    result={'rank_in_search':i+1,'pmcid':pmc,'pmid':item.get('pmid'),'doi':item.get('doi'),'title':title,'year':item.get('pubYear'),'journal':item.get('journalTitle'),'cited_by_count':item.get('citedByCount'),'source':item.get('source'),'publication_types':item.get('pubTypeList',{}).get('pubType',[]),'is_open_access':item.get('isOpenAccess'),'full_text_url':f'https://europepmc.org/articles/{pmc}' if pmc else None}
    if not pmc: return result,'no_pmcid',None
    if re.search(r'\b(scoping|protocol|overview of reviews|umbrella review|bibliometric|reporting guideline|guidelines|statement|methodolog(?:y|ical))\b',title,re.I): return result,'excluded_title',None
    path=CACHE/(pmc+'.xml')
    try:
        if not path.exists():
            for attempt in range(3):
                try:
                    resp=requests.get(f'{BASE}/{pmc}/fullTextXML',timeout=45)
                    if resp.status_code in (429,500,502,503,504): time.sleep(1+attempt*2);continue
                    resp.raise_for_status();path.write_bytes(resp.content);break
                except requests.RequestException:
                    if attempt==2: raise
                    time.sleep(1+attempt*2)
        if not path.exists(): return result,'fetch_failed',None
        data=path.read_bytes();root=ET.fromstring(data)
        body=root.find('.//body')
        if body is None: return result,'no_body',None
        text=flat(body,{'ref-list','caption','table-wrap','fig','supplementary-material'})
        lower=text.lower()
        # Title is the primary form signal. Verify recognizable search and eligibility methods in body.
        if not re.search(r'\b(systematic(?:ally)?\s+(?:search|literature search)|search(?:ed|es|ing)?\s+(?:of\s+)?(?:the\s+)?(?:electronic\s+)?(?:databases?|literature)|databases?\s+(?:were\s+)?search(?:ed)?|search\s+strateg(?:y|ies))\b',lower): return result,'no_search_method_signal',None
        if not re.search(r'\b(inclusion criteria|eligibility criteria|eligible studies|eligible articles|study selection|selection criteria|studies were included|studies were excluded|inclusion and exclusion)\b',lower): return result,'no_eligibility_signal',None
        paras=[]; sentence_words=[]; sections=[]; section_words=defaultdict(int)
        def walk(n,depth=0,current='Unsectioned'):
            tag=local(n.tag)
            if tag in EXCLUDE: return
            if tag=='sec':
                depth+=1
                t=next((c for c in n if local(c.tag)=='title'),None)
                heading=' '.join(flat(t).split()) if t is not None else '(untitled)'
                current=f'{len(sections)+1}: {heading}'
                sections.append({'id':len(sections)+1,'heading':heading,'depth':depth})
            if tag=='p':
                s=' '.join(flat(n,EXCLUDE).split()); w=words(s)
                if w:
                    segments=[seg for seg in SENT.split(s) if words(seg)]; ns=len(segments); sentence_words.extend(len(words(seg)) for seg in segments); paras.append((len(w),ns,sum(len(x) for x in w)))
                    section_words[current]+=len(w)
                return
            for c in n: walk(c,depth,current)
        walk(body)
        nwords=sum(p[0] for p in paras)
        if nwords<500 or len(paras)<5: return result,'insufficient_main_text',None
        abstract=' '.join(flat(x) for x in root.findall('.//abstract'))
        # Explicit title/abstract evidence only; unknown is retained as its own stratum.
        marker=title+' '+abstract
        if re.search(r'\b(?:systematic review\s*(?:and|with|&)\s*(?:a\s+)?(?:(?:network|pairwise|random[- ]effects|fixed[- ]effects)\s+)?meta[- ]analys(?:is|es)|meta[- ]analys(?:is|es)\s*(?:and|of)\s*(?:a\s+)?systematic review|meta[- ]analys(?:is|es)\s+(?:was|were|is|are)\s+(?:performed|conducted|undertaken)|(?:performed|conducted|undertook)\s+(?:a\s+)?(?:(?:network|pairwise|random[- ]effects|fixed[- ]effects)\s+)?meta[- ]analys(?:is|es))\b',marker,re.I): setting='with_meta_analysis'
        elif re.search(r'\b(?:no meta[- ]analysis|meta[- ]analysis (?:was|could) not|without (?:a )?meta[- ]analysis|meta[- ]analysis (?:was )?not (?:performed|possible|conducted))\b',marker,re.I): setting='without_meta_analysis'
        else: setting='uncertain'
        allbody=list(body.iter()); captions=[x for x in allbody if local(x.tag)=='caption']; refs=root.findall('.//ref-list//ref')
        top_lists=[]
        def collect_lists(n):
            if local(n.tag)=='list': top_lists.append(n); return
            if local(n.tag) in {'fig','table-wrap','caption','supplementary-material'}: return
            for child in n: collect_lists(child)
        collect_lists(body)
        met={'main_words':nwords,'paragraphs':len(paras),'sentences_estimate':sum(p[1] for p in paras),'word_characters':sum(p[2] for p in paras),'sentence_word_counts':sentence_words,'paragraph_word_counts':[p[0] for p in paras],'paragraph_sentence_estimates':[p[1] for p in paras],'sections':sections,'section_words':dict(section_words),'citation_xrefs':sum(local(x.tag)=='xref' and x.get('ref-type')=='bibr' for x in allbody),'figures':sum(local(x.tag)=='fig' for x in allbody),'tables':sum(local(x.tag)=='table-wrap' for x in allbody),'lists':sum(local(x.tag)=='list' for x in allbody),'list_words':sum(len(words(flat(x,{'label','xref'}))) for x in top_lists),'caption_words':sum(len(words(flat(x))) for x in captions),'references':len(refs),'abstract_words':len(words(abstract)),'title_words':len(words(title))}
        result.update({'meta_analysis_setting':setting,'xml_sha256':hashlib.sha256(data).hexdigest(),'full_text_xml_url':f'{BASE}/{pmc}/fullTextXML','screening':'title plus body search and eligibility method signals; machine screened, not human adjudicated'})
        return result,'measured',met
    except (requests.RequestException,ET.ParseError,OSError,ValueError) as e: return result,'error_'+type(e).__name__,None

def dist(vals):
    vals=sorted(vals)
    if not vals: return None
    def q(p): return round(vals[0]+(len(vals)-1)*p,2) if len(vals)==1 else round(vals[int((len(vals)-1)*p)]*(1-((len(vals)-1)*p%1))+vals[min(len(vals)-1,int((len(vals)-1)*p)+1)]*((len(vals)-1)*p%1),2)
    return {'n':len(vals),'min':vals[0],'p25':q(.25),'median':q(.5),'p75':q(.75),'max':vals[-1]}
def main():
    data=search(); items=data['resultList']['result']; rows=[]; metrics=[]; outcomes=Counter()
    # executor.map preserves the retrieved ranking; batches avoid claiming unconsumed results were screened.
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        for start in range(0,len(items),40):
            results=list(pool.map(lambda x:fetch(*x),enumerate(items[start:start+40],start)))
            for row,status,met in results:
                if len(metrics)>=TARGET: break
                row['status']=status;rows.append(row);outcomes[status]+=1
                if met is not None: metrics.append({'pmcid':row['pmcid'],'rank_in_search':row['rank_in_search'],'year':row.get('year'),'meta_analysis_setting':row['meta_analysis_setting'],**met})
            print('screened',len(rows),'measured',len(metrics),flush=True)
            if len(metrics)>=TARGET: break
    (OUT/'manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    (OUT/'metrics.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in metrics))
    keys=['main_words','paragraphs','sentences_estimate','word_characters','citation_xrefs','figures','tables','lists','list_words','caption_words','references','abstract_words','title_words']
    groups={'all':metrics}
    for setting in ['with_meta_analysis','without_meta_analysis','uncertain']: groups[setting]=[x for x in metrics if x['meta_analysis_setting']==setting]
    for era,lo,hi in [('pre_2015',0,2014),('2015_2019',2015,2019),('2020_onward',2020,9999)]: groups[era]=[x for x in metrics if str(x.get('year','')).isdigit() and lo <= int(x['year']) <= hi]
    groups['year_unknown']=[x for x in metrics if not str(x.get('year','')).isdigit()]
    stats={g:{'n':len(v),'metrics':{k:dist([x[k] for x in v]) for k in keys},'sentence_words':dist([p for x in v for p in x['sentence_word_counts']]),'paragraph_words':dist([p for x in v for p in x['paragraph_word_counts']]),'paragraph_sentences':dist([p for x in v for p in x['paragraph_sentence_estimates']]),'section_count':dist([len(x['sections']) for x in v])} for g,v in groups.items()}
    meta={'search_retrieved_at_utc':datetime.fromtimestamp((CACHE/'search.json').stat().st_mtime,timezone.utc).isoformat(),'measurement_run_at_utc':datetime.now(timezone.utc).isoformat(),'provider':'Europe PMC REST API','query':QUERY,'sort':'CITED desc','request_parameters':PARAMS,'provider_hit_count':data['hitCount'],'provider_version':data.get('version'),'candidate_page_size':len(items),'screened':len(rows),'measured':len(metrics),'outcomes':dict(outcomes),'search_url':requests.Request('GET',BASE+'/search',params=PARAMS).prepare().url,'search_cache_sha256':hashlib.sha256((CACHE/'search.json').read_bytes()).hexdigest(),'statistics':stats}
    (OUT/'aggregate.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
