#!/usr/bin/env python3
"""Collect Europe PMC metadata and derive body-only metrics; XML stays outside repository."""
import concurrent.futures,datetime,hashlib,json,re,statistics,time,xml.etree.ElementTree as ET
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/case-protocol'); CACHE.mkdir(parents=True,exist_ok=True)
BASE='https://www.ebi.ac.uk/europepmc/webservices/rest'
QUERIES={'clinical_case':'PUB_TYPE:"Case Reports" AND OPEN_ACCESS:Y SORT_CITED:y','study_protocol':'TITLE:"study protocol" AND OPEN_ACCESS:Y SORT_CITED:y','review_protocol':'TITLE:"systematic review protocol" AND OPEN_ACCESS:Y SORT_CITED:y'}
TODAY=datetime.date.today().isoformat(); WORD=re.compile(r"\b[^\W_]+(?:[’'-][^\W_]+)*\b",re.UNICODE)
def local(tag): return tag.rsplit('}',1)[-1]
def content(e): return ' '.join(' '.join(e.itertext()).split())
def words(s): return WORD.findall(s)
def get(url, **kw):
 for n in range(3):
  try:
   r=requests.get(url,timeout=40,**kw)
   if r.status_code in (429,500,502,503,504): time.sleep(1+n); continue
   return r
  except requests.RequestException:
   time.sleep(1+n)
 return None
def candidate(r, group):
 title=r.get('title','').lower(); typ='; '.join(r.get('pubTypeList',{}).get('pubType',[])).lower()
 if group=='clinical_case': return 'case report' in typ
 if group=='review_protocol': return 'protocol' in title and ('systematic review' in title or 'meta-analysis' in title)
 return 'protocol' in title and ('study protocol' in title) and not any(x in title for x in ('systematic review','scoping review','meta-analysis','review protocol'))
def metrics(root):
 body=next((e for e in root.iter() if local(e.tag)=='body'),None)
 if body is None:return None
 # Count excluded content separately before deriving prose metrics.
 captions=[content(e) for e in body.iter() if local(e.tag)=='caption']
 reference_count=sum(local(e.tag)=='ref' for e in root.iter())
 abstract_words=sum(len(words(content(e))) for e in root.iter() if local(e.tag)=='abstract')
 counts={tag:sum(local(e.tag)==tag for e in body.iter()) for tag in ['fig','table-wrap','list','list-item','code','preformat','disp-quote']}
 counts['citation_xrefs']=sum(local(e.tag)=='xref' and e.get('ref-type')=='bibr' for e in body.iter())
 # Remove non-body content that is sometimes embedded within the body.
 for p in list(body.iter()):
  for c in list(p):
   if local(c.tag) in ('ref-list','abstract','ack','app-group','supplementary-material','fig','table-wrap','caption'): p.remove(c)
 ps=[e for e in body.iter() if local(e.tag)=='p']; texts=[content(e) for e in ps]
 ws=[len(words(t)) for t in texts]; sentences=[max(1,len(re.findall(r'[.!?]+(?:["”’\)]|\s|$)',t))) if t else 0 for t in texts]
 # Section text is assigned to closest enclosing section, avoiding nested section double-counting.
 sections=[]
 def walk(e,depth=0):
  if local(e.tag)=='sec':
   title=next((content(x) for x in e if local(x.tag)=='title'),'')
   def own(x):
    return sum((len(words(content(c))) if local(c.tag)=='p' else own(c)) for c in x if local(c.tag)!='sec')
   role=next((label for label in ('introduction','background','methods','methodology','case presentation','case report','discussion','results','conclusion','limitations','ethics') if label in title.lower()),'other_or_unheaded')
   sections.append({'heading_category_heuristic':role,'depth':depth+1,'words':own(e)})
   depth+=1
  for c in e: walk(c,depth)
 walk(body)
 toks=[w for t in texts for w in words(t)]
 sentence_words=[len(words(v)) for t in texts for v in re.split(r'(?<=[.!?])\s+',t) if words(v)]
 return {'abstract_words':abstract_words,'caption_words':sum(len(words(x)) for x in captions),'reference_count':reference_count,'sentence_words_approx':sentence_words,'body_words_in_paragraphs':len(toks),'body_paragraphs':len(ps),'paragraph_words':ws,'paragraph_sentences':sentences,'sentence_count_approx':sum(sentences),'word_characters_total':sum(len(w) for w in toks),'section_count':len(sections),'sections':sections,'body_elements':counts}
def work(pair):
 group,r=pair; pmc=r.get('pmcid'); meta={'stratum':group,'title':r.get('title'),'authors':r.get('authorString'),'doi':r.get('doi'),'pmid':r.get('pmid'),'pmcid':pmc,'canonical_url':('https://doi.org/'+r['doi']) if r.get('doi') else ('https://pmc.ncbi.nlm.nih.gov/articles/'+pmc+'/' if pmc else None),'source_publication_types':r.get('pubTypeList',{}).get('pubType',[]),'citation_count':r.get('citedByCount'),'first_publication_date':r.get('firstPublicationDate'),'publication_year':r.get('pubYear'),'search_query':QUERIES[group],'search_order':'Europe PMC SORT_CITED:y','retrieved_date_utc':TODAY,'discovery_source':'Europe PMC REST search','classification_basis':('NLM/Europe PMC Case Reports publication type; clinical reporting scope' if group=='clinical_case' else 'Publisher title identifies '+ ('systematic review protocol' if group=='review_protocol' else 'study protocol') + '; prospective status not independently verified')}
 if not pmc: meta['retrieval_stage']='no_pmcid'; return meta
 path=CACHE/(pmc+'.xml')
 if not path.exists():
  res=get(BASE+'/'+pmc+'/fullTextXML')
  if res is None or res.status_code!=200:
   meta['retrieval_stage']='fulltext_failed'; meta['http_status']=res.status_code if res is not None else None; return meta
  path.write_bytes(res.content)
 data=path.read_bytes();meta['source_sha256']=hashlib.sha256(data).hexdigest()
 try: root=ET.fromstring(data)
 except ET.ParseError: meta['retrieval_stage']='xml_parse_failed'; return meta
 meta['jats_article_type']=root.get('article-type');meta['rights']=next(({'type':e.get('license-type'),'href':e.get('{http://www.w3.org/1999/xlink}href')} for e in root.iter() if local(e.tag)=='license'),None)
 m=metrics(root)
 if not m or not m['body_words_in_paragraphs']:meta['retrieval_stage']='body_missing'; return meta
 meta['retrieval_stage']='body_measured';meta['metrics']=m; return meta
if __name__=='__main__':
 allrows=[]; info={}
 for group,q in QUERIES.items():
  res=get(BASE+'/search',params={'query':q,'format':'json','pageSize':1000,'resultType':'core','cursorMark':'*'})
  if res is None: info[group]={'error':'search failed'};continue
  d=res.json(); results=d.get('resultList',{}).get('result',[]); candidates=[r for r in results if candidate(r,group)]
  # Cited-ranked eligible discovery; retrieve 350 to allow for missing full texts.
  candidates=candidates[:250];info[group]={'query':q,'hit_count':d.get('hitCount'),'response_sort':d.get('request',{}).get('sort'),'search_results_returned':len(results),'candidate_count':len(candidates),'target_measured':200}
  with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool: rows=list(pool.map(work,[(group,r) for r in candidates]))
  # Preserve all attempts, marking first 200 measured as analysis cohort.
  n=0
  for row in rows:
   row['included_in_cohort']=row['retrieval_stage']=='body_measured' and n<200
   if row['included_in_cohort']:n+=1
  allrows.extend(rows);info[group]['measured_in_cohort']=n
  print(group,n,'attempts',len(rows),flush=True)
 (ROOT/'manifest.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in allrows))
 (ROOT/'search.json').write_text(json.dumps(info,indent=2,ensure_ascii=False)+'\n')
