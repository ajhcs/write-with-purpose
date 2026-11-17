#!/usr/bin/env python3
"""Europe PMC discovery and bounded source-XML inspection; no source text saved."""
import concurrent.futures as cf, subprocess, json, urllib.parse, xml.etree.ElementTree as ET, re, hashlib, statistics, datetime, pathlib, time
P=pathlib.Path(__file__).resolve().parent
BASE='https://www.ebi.ac.uk/europepmc/webservices/rest/'
DATE=datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(url, timeout=18):
 p=subprocess.run(['curl','-sS','--connect-timeout','5','--max-time',str(timeout),url],capture_output=True)
 if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[:160])
 return p.stdout
def discovery(query, pages=1):
 cursor='*'; out=[]
 for _ in range(pages):
  url=BASE+'search?'+urllib.parse.urlencode(dict(query=query+' SORT_CITED:y',format='json',pageSize=250,resultType='core',cursorMark=cursor))
  for attempt in range(3):
   try: data=json.loads(get(url,35)); break
   except Exception:
    if attempt==2: raise
    time.sleep(2)
  out+=data['resultList']['result']; cursor=data.get('nextCursorMark','')
  if not cursor: break
 return data['hitCount'],out
def txt(e): return ' '.join(''.join(e.itertext()).split()) if e is not None else ''
def parse(item):
 form,z=item; pmc=z.get('pmcid'); title=z.get('title','')
 obj={'form':form,'stage':'candidate','id':pmc or z.get('id'),'title':title,'authors':z.get('authorString',''),'date':z.get('firstPublicationDate',z.get('pubYear','')),'url':'https://europepmc.org/articles/'+pmc if pmc else '', 'doi':z.get('doi',''),'journal':z.get('journalInfo',{}).get('journal',{}).get('title',''),'source_original_type':z.get('pubTypeList',{}).get('pubType',[]),'citation_count':z.get('citedByCount'), 'citation_provider':'Europe PMC','citation_observed_at':DATE,'selection':'Europe PMC open-access query, descending citations; candidates only','fulltext_status':'not retrieved','classification_basis':'search query only'}
 if not pmc: return obj
 try:
  raw=get(BASE+pmc+'/fullTextXML',10); root=ET.fromstring(raw); obj['fulltext_status']='retrieved XML'; obj['xml_article_type']=root.get('article-type',''); obj['xml_categories']=[txt(e) for e in root.findall('./front/article-meta/article-categories//subject')]
  body=root.find('./body'); bodytext=txt(body)
  if body is None or len(bodytext)<300: obj['fulltext_status']='retrieved; body absent or under 300 characters'; return obj
  # A product identifies a reviewed item, but source tagging alone can be wrong.
  products=[txt(e) for e in root.findall('./front/article-meta//product') if txt(e)]
  obj['product_metadata_present']=bool(products)
  obj['product_metadata_excerpt']=products[0][:250] if products else ''
  if form=='critical_review':
   if root.get('article-type')=='book-review' and products:
    obj['stage']='verified_source_label'; obj['classification_basis']='JATS book-review article type plus product metadata; review target not independently verified'
   else: obj['classification_basis']='book-review discovery label insufficient without JATS book-review and product metadata'
  else:
   cats=' '.join(obj['xml_categories']);
   if re.search(r'\b(conceptual|theoretical|theory)\b',cats,re.I) and not re.search(r'\b(methods?|results?|participants?|patients?|survey|interviews?|trial|study design)\b', ' '.join(txt(e) for e in body.findall('.//sec/title')), re.I):
    obj['stage']='verified_source_label'; obj['classification_basis']='publisher XML article category explicitly conceptual/theoretical, no empirical section heading detected; manual screening required'
   else: obj['classification_basis']='title keyword alone does not establish conceptual article type or exclude empirical research'
  if obj['stage']!='verified_source_label': return obj
  # Restrict to prose paragraphs directly in body, avoid captions, tables, boxes and references.
  paras=[]
  def walk(e, skip=False):
   if e.tag in ('fig','table-wrap','boxed-text','supplementary-material','disp-formula','ref-list'): return
   if e.tag=='p':
    t=txt(e)
    if t: paras.append(t)
    return
   for child in e: walk(child)
  walk(body)
  if not paras: obj['fulltext_status']='retrieved; no eligible prose paragraphs'; return obj
  words=lambda s: re.findall(r"\b[^\W\d_]+(?:['’\-][^\W\d_]+)*\b",s,re.UNICODE)
  sentences=[s for p in paras for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9“\"(])',p) if s.strip()]
  lengths=[len(words(p)) for p in paras]; sl=[len(words(s)) for s in sentences]; ws=words(' '.join(paras))
  secs=body.findall('./sec'); seccounts=[]
  for s in secs:
   ps=[]
   def secwalk(e):
    if e.tag in ('fig','table-wrap','boxed-text','supplementary-material','ref-list'): return
    if e.tag=='p': ps.append(txt(e)); return
    for c in e: secwalk(c)
   secwalk(s); seccounts.append({'heading':txt(s.find('./title'))[:120],'words':sum(len(words(p)) for p in ps)})
  obj['measurement']={'main_prose_words':len(ws),'paragraphs':len(paras),'paragraph_words_median':statistics.median(lengths),'sentences_heuristic':len(sl),'sentence_words_median':statistics.median(sl),'word_characters_mean':round(sum(map(len,ws))/len(ws),2) if ws else None,'top_level_sections':len(secs),'sections':seccounts,'inline_citation_xrefs':len([e for e in body.findall('.//xref') if e.get('ref-type')=='bibr']),'figures':len(body.findall('.//fig')),'tables':len(body.findall('.//table-wrap')),'list_elements':len(body.findall('.//list')),'prose_sha256':hashlib.sha256('\n'.join(paras).encode()).hexdigest()}
  obj['stage']='measured_source_label'; obj['fulltext_status']='retrieved and prose measured; source text not retained'
 except Exception as e: obj['fulltext_status']='retrieval or parsing failed: '+str(e)[:160]
 return obj
if __name__=='__main__':
 cases=[('critical_review','PUB_TYPE:"Book Review" AND OPEN_ACCESS:Y'),('conceptual_paper','TITLE:"conceptual framework" AND OPEN_ACCESS:Y')]
 allrows=[]; counts={}
 for form,q in cases:
  try: n,results=discovery(q); counts[form]={'query':q,'hitCount':n,'discovered':len(results)}; allrows.extend((form,z) for z in results)
  except Exception as e: counts[form]={'query':q,'error':str(e)}
 (P/'discovery.json').write_text(json.dumps({'retrieved_at':DATE,'queries':counts},indent=2))
 print('discovered',counts,flush=True)
 out=[]
 with cf.ThreadPoolExecutor(max_workers=16) as ex:
  futures=[ex.submit(parse, item) for item in allrows]
  for i,future in enumerate(cf.as_completed(futures),1):
   row=future.result()
   out.append(row)
   if i%50==0: print('processed',i,'measured',sum(x['stage']=='measured_source_label' for x in out),flush=True)
   if i%25==0: (P/'records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out))
 (P/'records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out))
