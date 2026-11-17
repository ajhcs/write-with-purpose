#!/usr/bin/env python3
"""Fetch candidate metadata and OA JATS; compute reproducible bounded features."""
import concurrent.futures as cf, csv, json, re, time, statistics, pathlib, hashlib, os, requests, xml.etree.ElementTree as ET
from datetime import datetime, timezone
D=pathlib.Path(os.environ.get('CORPUS_OUTPUT',pathlib.Path(__file__).resolve().parent));D.mkdir(parents=True,exist_ok=True)
C=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/empirical-methods'); C.mkdir(parents=True,exist_ok=True)
API='https://www.ebi.ac.uk/europepmc/webservices/rest'
QUERIES={'empirical':'OPEN_ACCESS:y AND FIRST_PDATE:[1900-01-01 TO 2014-12-31] AND (PUB_TYPE:"Randomized Controlled Trial") SORT_CITED:y','methods':'OPEN_ACCESS:y AND JOURNAL:MethodsX SORT_CITED:y'}
if os.environ.get('CORPUS_FORM') in QUERIES: QUERIES={os.environ['CORPUS_FORM']:QUERIES[os.environ['CORPUS_FORM']]}
W=re.compile(r"\b[^\W_]+(?:['’\-][^\W_]+)*\b",re.UNICODE)
S=re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9(])')
def text(e): return ' '.join(''.join(e.itertext()).split()) if e is not None else ''
def get_candidates(kind,q):
 p=C/(kind+'-search.json')
 if p.exists(): return json.loads(p.read_text())
 r=requests.get(API+'/search',params={'query':q,'format':'json','pageSize':1000,'resultType':'core'},timeout=80);r.raise_for_status(); j=r.json();p.write_text(json.dumps(j));return j
def prose_paragraphs(node):
 for child in node:
  if child.tag in {'fig','table-wrap','caption','list','disp-formula','supplementary-material','boxed-text','ref-list','fn-group'}: continue
  if child.tag == 'p': yield child
  else: yield from prose_paragraphs(child)

def clean_para(p):
 x=ET.fromstring(ET.tostring(p))
 for parent in x.iter():
  for child in list(parent):
   if child.tag in {'xref','fig','table-wrap','disp-formula','inline-formula','supplementary-material','label','caption'}:
    i=list(parent).index(child);tail=child.tail or '';parent.remove(child)
    if i: parent[i-1].tail=(parent[i-1].tail or '')+tail
    else: parent.text=(parent.text or '')+tail
 return text(x)
def work(item):
 kind,x=item;p=x.get('pmcid'); out={'form':kind,'pmcid':p,'title':x.get('title',''),'year':x.get('firstPublicationDate',''),'journal':x.get('journalTitle') or x.get('journalInfo',{}).get('journal',{}).get('title',''),'cited_by_count':x.get('citedByCount',0),'source_type':'; '.join(x.get('pubTypeList',{}).get('pubType',[])),'doi':x.get('doi',''),'source_url':'https://europepmc.org/articles/'+str(p),'status':'','reason':''}
 out['citation_snapshot_utc']=datetime.fromtimestamp((C/(kind+'-search.json')).stat().st_mtime,timezone.utc).isoformat()
 if not p:out.update(status='excluded',reason='no PMCID');return out
 if kind=='methods' and not re.search(r'\b(methods?|methodology|technique|approach|assay|procedure|algorithm|workflow|software|tool|pipeline|step.by.step)\b',out['title'],re.I):out.update(status='excluded',reason='title lacks explicit method contribution cue');return out
 if kind=='methods' and re.search(r'\b(review|protocol)\b',out['title'],re.I):out.update(status='excluded',reason='possible review or prospective study protocol');return out
 f=C/(p+'.xml')
 try:
  if not f.exists():
   r=requests.get(f'{API}/{p}/fullTextXML',timeout=22);r.raise_for_status();f.write_bytes(r.content)
  out['xml_sha256']=hashlib.sha256(f.read_bytes()).hexdigest();out['xml_retrieved_utc']=datetime.fromtimestamp(f.stat().st_mtime,timezone.utc).isoformat()
  root=ET.parse(f).getroot(); body=root.find('./body'); typ=root.get('article-type',''); cats=[text(e) for e in root.findall('.//article-categories//subject')];out['jats_type']=typ;out['jats_category']='; '.join(cats)
  if body is None:out.update(status='excluded',reason='no body');return out
  if kind=='empirical' and typ!='research-article':out.update(status='excluded',reason='not JATS research-article');return out
  if kind=='methods' and typ not in ('research-article','methods-article'):out.update(status='excluded',reason='not eligible JATS article type');return out
  pars=[]; sections=[]
  for sec in body.findall('./sec'):
   title=text(sec.find('./title')); ps=[clean_para(z) for z in prose_paragraphs(sec) if clean_para(z)]; sections.append({'heading':title,'words':sum(len(W.findall(z)) for z in ps),'paragraphs':len(ps)});pars+=ps
  # Include unsectioned direct body paragraphs, avoid counting nested paragraphs twice.
  for p0 in body.findall('./p'):pars.append(clean_para(p0))
  pars=[z for z in pars if z];words=[w for p0 in pars for w in W.findall(p0)]; sent=[s for p0 in pars for s in S.split(p0) if s.strip()]; headings=' '.join(s['heading'] for s in sections).lower()
  if len(words)<300:out.update(status='excluded',reason='less than 300 extracted prose words');return out
  if kind=='empirical' and not (re.search(r'method|patient|trial|participant|design',headings) and re.search(r'result|finding',headings)):
   out.update(status='excluded',reason='no visible methods/design and results headings');return out
  out.update(status='measured',reason=('PubMed randomized controlled trial; JATS research-article with methods/design and results headings' if kind=='empirical' else 'MethodsX journal scope and title method cue; JATS article type '+typ),title_words=len(W.findall(out['title'])),abstract_words=len(W.findall(text(root.find('.//abstract')))),caption_words=sum(len(W.findall(text(c))) for c in body.findall('.//caption')),main_words=len(words),paragraphs=len(pars),sentences=len(sent),word_characters=sum(len(w) for w in words),figures=len(body.findall('.//fig')),tables=len(body.findall('.//table-wrap')),references=len(root.findall('.//ref-list//ref')),top_sections=len(sections),section_detail=json.dumps(sections,ensure_ascii=False),paragraph_word_counts=json.dumps([len(W.findall(z)) for z in pars]),sentence_word_counts=json.dumps([len(W.findall(z)) for z in sent]),license=text(root.find('.//permissions/license/license-p'))[:500])
 except Exception as e:out.update(status='unavailable',reason=type(e).__name__+': '+str(e)[:150])
 return out

def main():
 items=[];searchinfo={}
 for kind,q in QUERIES.items():
  j=get_candidates(kind,q);xs=j['resultList']['result'];searchinfo[kind]={'query':q,'hit_count':j['hitCount'],'returned':len(xs),'provider':'Europe PMC REST search','snapshot_utc':datetime.fromtimestamp((C/(kind+'-search.json')).stat().st_mtime,timezone.utc).isoformat(),'note':'citation counts returned at metadata request, cache retained'};items.extend((kind,x) for x in xs[:500])
 rows=[]; counts={'empirical':0,'methods':0}
 with cf.ThreadPoolExecutor(max_workers=int(os.environ.get('CORPUS_WORKERS','3'))) as pool:
  # ordered batches preserve source ranking and stop after 200 measured per pool
  for kind in QUERIES:
   poolitems=[i for i in items if i[0]==kind]
   for start in range(0,len(poolitems),25):
    if counts[kind]>=200:break
    for row in pool.map(work,poolitems[start:start+25]):
     if row['status']=='measured':
      if counts[kind]>=200:row['status']='excluded';row['reason']='sample quota reached'
      else:counts[kind]+=1
     rows.append(row)
    fields=sorted(set().union(*(r.keys() for r in rows)))
    with (D/'manifest.csv').open('w',newline='') as f:
     w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
    (D/'search.json').write_text(json.dumps(searchinfo,indent=2))
    print(kind,start+25,counts[kind],flush=True)
 fields=['form','pmcid','title','year','journal','doi','source_url','cited_by_count','source_type','jats_type','jats_category','citation_snapshot_utc','xml_sha256','xml_retrieved_utc','status','reason','title_words','abstract_words','caption_words','main_words','paragraphs','sentences','word_characters','figures','tables','references','top_sections','section_detail','paragraph_word_counts','sentence_word_counts','license']
 with (D/'manifest.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
 (D/'search.json').write_text(json.dumps(searchinfo,indent=2))
 for kind in QUERIES:
  a=[r for r in rows if r['form']==kind and r['status']=='measured'];print(kind,len(a));
  if a:
   for k in ['main_words','paragraphs','sentences','figures','tables','references']:
    v=sorted(r[k] for r in a); print(k,min(v),statistics.median(v),max(v))
if __name__=='__main__':main()
