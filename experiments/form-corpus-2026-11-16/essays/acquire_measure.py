#!/usr/bin/env python3
"""Retrieve a bounded Europe PMC citation-ranked OA sample; emit metadata and derived metrics only."""
import concurrent.futures as cf, csv, datetime as dt, hashlib, json, re, statistics as stats, sys, threading, time
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
CACHE=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16')
CACHE.mkdir(parents=True,exist_ok=True)
BASE='https://www.ebi.ac.uk/europepmc/webservices/rest/'
UA={'User-Agent':'WritingFormResearch/1.0 (research corpus; polite access)'}
QUERIES={'personal_reflective':'PUB_TYPE:"Personal Narrative" AND OPEN_ACCESS:Y AND LANG:eng SORT_CITED:y', 'argument_perspective':'PUB_TYPE:Editorial AND OPEN_ACCESS:Y AND LANG:eng SORT_CITED:y'}
WORD=re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*|\d+(?:[.,]\d+)*",re.UNICODE)
SENT=re.compile(r'(?<=[.!?])\s+(?=[A-Z“"(])')
lock=threading.Lock(); next_req=0

def fetch(url,params=None):
 global next_req
 with lock:
  wait=max(0,next_req-time.monotonic()); time.sleep(wait);next_req=time.monotonic()+0.4
 r=requests.get(url,params=params,headers=UA,timeout=35); r.raise_for_status();return r

def txt(e): return ' '.join(' '.join(e.itertext()).split())
def tag(e): return e.tag.rsplit('}',1)[-1]
def process(item):
 pmcid=item['pmcid']; url=BASE+pmcid+'/fullTextXML'; p=CACHE/(pmcid+'.xml')
 result={k:item.get(k) for k in ['form_candidate','id','pmid','pmcid','title','authorString','journalTitle','pubYear','firstPublicationDate','citedByCount','pubTypeList','isOpenAccess','source_query','source_rank']}
 result.update(fulltext_url=url, retrieved_utc=None, sha256=None, extraction_status='failed', error=None)
 try:
  if p.exists(): raw=p.read_bytes()
  else: raw=fetch(url).content; p.write_bytes(raw)
  result['retrieved_utc']=dt.datetime.fromtimestamp(p.stat().st_mtime,dt.timezone.utc).isoformat(); result['sha256']=hashlib.sha256(raw).hexdigest()
  root=ET.fromstring(raw); journal=root.find('./front/journal-meta/journal-title-group/journal-title'); result['journalTitle']=txt(journal) if journal is not None else result.get('journalTitle'); body=root.find('./body')
  if body is None: result['extraction_status']='no_body';return result
  blocked={'fig','fig-group','table-wrap','table-wrap-group','list','disp-formula','code','preformat','boxed-text','supplementary-material','ref-list','fn-group','ack','caption'}
  paragraphs=[]; heading=[]; secwords={}; counts={'fig':0,'table-wrap':0,'list':0,'code':0,'disp-quote':0,'xref':0,'ext-link':0,'inline-quote':0}
  def walk(node,sec='unheaded',depth=0):
   t=tag(node)
   if t in counts: counts[t]+=1
   if t=='sec':
    title=next((txt(x) for x in node if tag(x)=='title'),'unheaded');sec=title or 'unheaded';depth+=1
    if title: heading.append({'depth':depth,'title':title})
   if t in blocked:return
   if t=='p':
    text=txt(node); words=WORD.findall(text)
    if words:
     sentences=[x for x in SENT.split(text) if x.strip()]; lengths=[len(WORD.findall(x)) for x in sentences]
     # Names and citation numbers are merely presentations, not verified support.
     paragraphs.append({'words':len(words),'sentences':len(sentences),'sentence_words':lengths,'characters_per_word_sum':sum(map(len,words)),'first_person_tokens':sum(w.casefold() in {'i','me','my','mine','myself','we','our','us','ours','ourselves'} for w in words),'quotation_marks':text.count('“')+text.count('"')})
     secwords[sec]=secwords.get(sec,0)+len(words)
    for d in node.iter():
     if d is not node and tag(d) in counts:counts[tag(d)]+=1
    return
   for c in node:walk(c,sec,depth)
  walk(body)
  refs=root.findall('./back/ref-list/ref'); words=sum(x['words'] for x in paragraphs)
  result.update(extraction_status='measured' if words else 'no_prose', article_type=root.get('article-type'), license=txt(root.find('.//permissions')) if root.find('.//permissions') is not None else None, body_prose_words=words, paragraph_count=len(paragraphs), paragraph_words=[x['words'] for x in paragraphs], paragraph_sentences=[x['sentences'] for x in paragraphs], sentence_words=[n for p in paragraphs for n in p['sentence_words']], character_count_in_words=sum(x['characters_per_word_sum'] for x in paragraphs), first_person_tokens=sum(x['first_person_tokens'] for x in paragraphs), quotation_marks=sum(x['quotation_marks'] for x in paragraphs), headings=heading, section_words=secwords, reference_entries=len(refs), presentation_counts=counts, eligibility='not_manually_screened', extraction_notes='Body paragraphs only; exclude list, table, figure, formula, box, captions, acknowledgments and references; nested inline text retained. Section labels may repeat; sentence counts approximate.')
 except Exception as e: result['error']=str(e)[:250]
 return result

def main():
 candidates=[]; discovery={}
 for form,query in QUERIES.items():
  r=fetch(BASE+'search',{'query':query,'format':'json','pageSize':1000,'resultType':'core'}).json(); hits=r['resultList']['result']; hits=[x for x in hits if x.get('pmcid') and x.get('isOpenAccess')=='Y']
  # One author/journal or article type is not assumed representative; ranking is citation count at retrieval.
  limit=300 if form=='personal_reflective' else 300
  selected=hits[:limit];discovery[form]={'query':query,'total_query_hits':r['hitCount'],'page_returned':len(hits),'selected_for_retrieval':len(selected),'selected_order':'Europe PMC SORT_CITED:y; descending citation count, ties API order','retrieved_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
  for rank,x in enumerate(selected,1):x.update(form_candidate=form,source_query=query,source_rank=rank);candidates.append(x)
 (ROOT/'discovery.json').write_text(json.dumps(discovery,indent=2)+'\n')
 with (ROOT/'candidates.jsonl').open('w') as out:
  for x in candidates: out.write(json.dumps({k:x.get(k) for k in ['form_candidate','id','pmid','pmcid','title','authorString','journalTitle','pubYear','firstPublicationDate','citedByCount','pubTypeList','isOpenAccess','source_query','source_rank']},ensure_ascii=False)+'\n')
 with (ROOT/'measurements.jsonl').open('w') as out, cf.ThreadPoolExecutor(max_workers=6) as pool:
  futures=[pool.submit(process,x) for x in candidates]
  for i,f in enumerate(cf.as_completed(futures),1):
   out.write(json.dumps(f.result(),ensure_ascii=False)+'\n');out.flush()
   if i%25==0: print(f'{i}/{len(futures)} complete',flush=True)
if __name__=='__main__':main()
