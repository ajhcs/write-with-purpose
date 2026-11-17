#!/usr/bin/env python3
"""Bounded Europe PMC sample; cache source XML and save metadata/derived counts."""
import concurrent.futures, datetime, hashlib, json, re, statistics, time, xml.etree.ElementTree as ET
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/narrative-scoping'); CACHE.mkdir(parents=True,exist_ok=True)
BASE='https://www.ebi.ac.uk/europepmc/webservices/rest'
SPECS={'narrative': 'TITLE:"narrative review" AND OPEN_ACCESS:Y', 'scoping': 'TITLE:"scoping review" AND OPEN_ACCESS:Y'}
WORD=re.compile(r"\b[^\W_]+(?:['’\-][^\W_]+)*\b", re.UNICODE)
SENT=re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9“\"(])')
BAD=re.compile(r'\b(protocol|systematic review|meta.analysis|scoping review|umbrella review|bibliometric|guideline|reporting standard|scale for the quality|review of reviews|methodolog(?:y|ical)|how to (?:conduct|write))\b',re.I)
BADSC=re.compile(r'\b(protocol|systematic review|meta.analysis|umbrella review|bibliometric|reporting guideline|methodolog(?:y|ical)|how to (?:conduct|write))\b',re.I)
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def txt(e): return ' '.join(' '.join(e.itertext()).split()) if e is not None else ''
def words(s): return WORD.findall(s)
def role(s):
 for label,pat in [('introduction',r'introduction|background'),('methods',r'method|search strateg|eligib|selection|data extraction'),('results',r'results|findings'),('discussion',r'discussion'),('conclusion',r'conclu')]:
  if re.search(pat,s,re.I): return label
 return 'other_or_unheaded'
def download(pmc):
 path=CACHE/(pmc+'.xml')
 if path.exists(): return path,'cached'
 for attempt in range(3):
  try:
   r=requests.get(f'{BASE}/{pmc}/fullTextXML',timeout=45)
   if r.status_code==200 and r.content.lstrip().startswith(b'<'): path.write_bytes(r.content); return path,'downloaded'
   if r.status_code in (404,403): return None,'http_'+str(r.status_code)
  except requests.RequestException: pass
  time.sleep(1+attempt)
 return None,'unavailable'
def analyze(row):
 pmc=row.get('pmcid','')
 if not pmc: return None,'no_pmcid'
 path,status=download(pmc)
 if path is None: return None,status
 try: root=ET.parse(path).getroot(); orig=ET.parse(path).getroot()
 except ET.ParseError: return None,'invalid_xml'
 body=root.find('./body'); ob=orig.find('./body')
 if body is None: return None,'no_body'
 groups=[txt(x) for x in root.findall('./front/article-meta/article-categories/subj-group/subject')]
 admin_titles={'acknowledgements','acknowledgments','author contributions','authors contributions','funding','funding information','financial support','data availability','availability of data and materials','declarations','declaration','ethics approval and consent to participate','ethics approval','consent for publication','competing interests','conflict of interest','conflicts of interest','footnotes','associated data'}
 for parent in body.iter():
  for child in list(parent):
   if child.tag=='sec' and txt(child.find('./title')).strip(' .:').lower() in admin_titles: parent.remove(child)
 for tag in ('fig','fig-group','table-wrap','table-wrap-group','supplementary-material','ref-list','disp-formula','boxed-text','code','preformat','list'):
  for parent in body.iter():
   for child in list(parent):
    if child.tag==tag: parent.remove(child)
 paragraphs=[txt(p) for p in body.iter('p') if txt(p)]
 if not paragraphs: return None,'no_body_paragraphs'
 ps=[len(words(p)) for p in paragraphs]; ss=[len(words(s)) for p in paragraphs for s in SENT.split(p) if words(s)]; toks=[w for p in paragraphs for w in words(p)]
 sections=[]
 for s in body.findall('./sec'):
  sections.append({'role':role(txt(s.find('./title'))),'words':sum(len(words(txt(x))) for x in s.iter('p'))})
 for section in sections: section['body_percent']=round(100*section['words']/len(toks),2) if toks else 0
 def depth(e):
  children=e.findall('./sec'); return 1+max((depth(c) for c in children),default=0)
 max_section_depth=max((depth(s) for s in body.findall('./sec')),default=0)
 counts={k:len(list(ob.iter(tag))) for k,tag in [('figures','fig'),('tables','table-wrap'),('lists','list'),('code','code'),('preformat','preformat'),('citation_xrefs','xref')]}
 counts['bibliographic_xrefs']=sum(1 for x in ob.iter('xref') if x.attrib.get('ref-type')=='bibr')
 return {'publisher_article_type':root.attrib.get('article-type',''),'publisher_subject_labels':groups,'body_words':len(toks),'paragraphs':len(ps),'paragraph_words':ps,'sentence_words':ss,'word_characters':[len(w) for w in toks], 'top_level_sections':len(sections),'max_section_depth':max_section_depth,'section_roles_words':sections,'abstract_words':len(words(txt(orig.find('./front/article-meta/abstract')))),'reference_entries':sum(len(x.findall('./ref')) for x in orig.iter('ref-list')),**counts},status
def quant(vals):
 if not vals:return None
 vals=sorted(vals)
 def p(q):
  i=(len(vals)-1)*q; lo=int(i); hi=min(lo+1,len(vals)-1); return round(vals[lo]+(vals[hi]-vals[lo])*(i-lo),2)
 return {'n':len(vals),'min':vals[0],'p25':p(.25),'median':p(.5),'p75':p(.75),'max':vals[-1]}
def main():
 receipt={'started_utc':now(),'endpoint':BASE+'/search','sort_requested':'CITED desc','citation_provider':'Europe PMC citedByCount, snapshot at search time','target_per_form':200,'source':'Europe PMC open access fullTextXML','queries':{}}
 for form,query in SPECS.items():
  params={'query':query,'format':'json','pageSize':1000,'resultType':'core','sort':'CITED desc'}
  r=requests.get(BASE+'/search',params=params,timeout=90);r.raise_for_status(); j=r.json(); records=j['resultList']['result']
  receipt['queries'][form]={'url':r.url,'request_echo':j.get('request'),'hit_count':j['hitCount'],'returned':len(records),'search_utc':now()}
  screen=[]; candidates=[]
  for rank,x in enumerate(records,1):
   match=(BAD if form=='narrative' else BADSC).search(x.get('title',''))
   screen.append({'search_rank':rank,'pmcid':x.get('pmcid',''),'pmid':x.get('pmid',''),'doi':x.get('doi',''),'title':x.get('title',''),'year':x.get('pubYear',''),'cited_by_count':x.get('citedByCount',0),'screen_exclusion_match':match.group(0) if match else ''})
   if not match: candidates.append((rank,x))
  (ROOT/(form+'-search-screen.json')).write_text(json.dumps(screen,indent=2,ensure_ascii=False)+'\n')
  selected=candidates[:275]
  with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool: results=list(pool.map(lambda pair:analyze(pair[1]), selected))
  metadata=[]; measurements=[]
  for (rank,x),(m,status) in zip(selected,results):
   row={'form':form,'search_rank':rank,'pmcid':x.get('pmcid',''),'pmid':x.get('pmid',''),'doi':x.get('doi',''),'title':x.get('title',''),'year':x.get('pubYear',''),'journal':x.get('journalTitle') or x.get('journalInfo',{}).get('journal',{}).get('title',''),'publication_types':x.get('pubTypeList',{}).get('pubType',[]),'cited_by_count':x.get('citedByCount',0),'classification_basis':'explicit form phrase in title; automated exclusion of named other forms and methods papers; semantic fit provisional','xml_status':status,'measured':False}
   if m:
    row['publisher_article_type']=m['publisher_article_type'];row['publisher_subject_labels']=m['publisher_subject_labels']; row['xml_sha256']=hashlib.sha256((CACHE/(row['pmcid']+'.xml')).read_bytes()).hexdigest();row['xml_cached_mtime_utc']=datetime.datetime.fromtimestamp((CACHE/(row['pmcid']+'.xml')).stat().st_mtime,datetime.timezone.utc).isoformat();row['citation_snapshot_utc']=receipt['queries'][form]['search_utc'];row['year_basis']='Europe PMC pubYear'
    incompatible=(form=='narrative' and m['publisher_article_type']=='systematic-review') or (m['publisher_article_type'] in ('editorial','letter','commentary','book-review') and not any('review' in s.lower() for s in m['publisher_subject_labels']))
    if incompatible: row['classification_basis']+='; publisher article type requires manual review; excluded';row['xml_status']='excluded_incompatible_publisher_type'
    elif len(measurements)<200: row['measured']=True; measurements.append({'pmcid':row['pmcid'],**m})
    else: row['xml_status']='available_beyond_selected_limit'
   metadata.append(row)
  (ROOT/(form+'-candidates.json')).write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
  (ROOT/(form+'-metrics.json')).write_text(json.dumps(measurements,ensure_ascii=False)+'\n')
  stats={k:quant([m[k] for m in measurements]) for k in ('body_words','paragraphs','top_level_sections','max_section_depth','abstract_words','reference_entries','figures','tables','lists','code','bibliographic_xrefs')}
  stats.update({k+'_document_medians':quant([statistics.median(m[k]) for m in measurements if m[k]]) for k in ('paragraph_words','sentence_words','word_characters')})
  (ROOT/(form+'-aggregate.json')).write_text(json.dumps(stats,indent=2)+'\n')
  receipt['queries'][form].update({'title_screen_survivors_in_returned':len(candidates),'xml_attempted':len(selected),'measured':len(measurements)})
  print(form,receipt['queries'][form],flush=True)
 receipt['finished_utc']=now();(ROOT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__': main()
