#!/usr/bin/env python3
"""Enrich collector checkpoints with provenance and write descriptive summary."""
import csv, hashlib, json, pathlib, statistics, re, xml.etree.ElementTree as ET
from datetime import datetime, timezone
import collect
D=pathlib.Path(__file__).resolve().parent
C=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/empirical-methods')
def readcsv(p):
 with p.open(newline='') as f:return list(csv.DictReader(f))
def iso(p):return datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat()
paths=[D/'manifest.csv',C/'methods-run'/'manifest.csv' if (C/'methods-run'/'manifest.csv').exists() else D/'manifest.csv'];rows=[]
for kind,path in zip(['empirical','methods'],paths):
 if path.exists():rows += [r for r in readcsv(path) if r['form']==kind]
tail=C/'methods-tail.csv'
if tail.exists():rows += [r for r in readcsv(tail) if r['form']=='methods']
meta={}
for kind in ['empirical','methods']:
 p=C/(kind+'-search.json')
 if p.exists():
  j=json.loads(p.read_text());meta[kind]={'query':j['request']['queryString'],'hit_count':j['hitCount'],'returned':len(j['resultList']['result']),'provider':'Europe PMC REST search','snapshot_utc':iso(p)}
  for rank,x in enumerate(j['resultList']['result'],1):
   x['_source_rank']=rank
   if x.get('pmcid'):meta[(kind,x['pmcid'])]=x
   else:meta[(kind,'title:'+x.get('title',''))]=x
for r in rows:
 kind=r['form']; pmc=r.get('pmcid');x=meta.get((kind,pmc),{}) or meta.get((kind,'title:'+r.get('title','')),{});f=C/(str(pmc)+'.xml')
 r['journal']=x.get('journalTitle') or x.get('journalInfo',{}).get('journal',{}).get('title','')
 r['citation_snapshot_utc']=meta[kind]['snapshot_utc'];r['source_rank']=x.get('_source_rank','')
 if f.is_file():
  r['xml_sha256']=hashlib.sha256(f.read_bytes()).hexdigest();r['xml_retrieved_utc']=iso(f)
  try:
   root=ET.parse(f).getroot(); W=re.compile(r"\b[^\W_]+(?:['’\-][^\W_]+)*\b",re.UNICODE)
   def words(node):return len(W.findall(' '.join(node.itertext()))) if node is not None else 0
   r['title_words']=len(W.findall(r.get('title','')));r['abstract_words']=words(root.find('.//abstract'));body=root.find('./body');r['caption_words']=sum(words(n) for n in body.findall('.//caption')) if body is not None else 0
   def refs(n):
    total=0
    for child in n:
     if child.tag in {'fig','table-wrap','caption','list','disp-formula','supplementary-material','boxed-text','ref-list','fn-group'}:continue
     if child.tag=='sec' and is_admin(child):continue
     if child.tag=='xref' and child.get('ref-type')=='bibr':total+=1
     else:total+=refs(child)
    return total
   # Recompute from cached XML so administrative declarations are separate.
   admin=re.compile(r"^(acknowledg(e)?ments?|competing interests?|conflicts? of interest|declaration of (competing )?interests?|authors?['’]?( contributions?| information)|author contributions?|funding( information| statement)?|financial support|ethical approval|ethics (approval|statement)|consent for publication|data availability( statement)?|availability of data( and materials)?|pre.?publication history|supplementary (material|information)|abbreviations)$",re.I)
   def is_admin(sec):return bool(admin.match(' '.join(sec.find('title').itertext()).strip().rstrip(':') if sec.find('title') is not None else ''))
   def keep_paras(node,omit_admin=True):
    for ch in node:
     if ch.tag in {'fig','table-wrap','caption','list','disp-formula','supplementary-material','boxed-text','ref-list','fn-group'}:continue
     if ch.tag=='sec' and omit_admin and is_admin(ch):continue
     if ch.tag=='p':yield ch
     else:yield from keep_paras(ch,omit_admin)
   if body is not None and r.get('status')=='measured':
    pp=[collect.clean_para(p) for p in keep_paras(body)];pp=[p for p in pp if p]
    def admin_paras(node):
     for ch in node:
      if ch.tag=='sec' and is_admin(ch):yield from keep_paras(ch,False)
      else:yield from admin_paras(ch)
    excluded=[collect.clean_para(p) for p in admin_paras(body)]
    ww=[w for p in pp for w in collect.W.findall(p)];ss=[t for p in pp for t in collect.S.split(p) if t.strip()]
    r['main_words']=len(ww);r['paragraphs']=len(pp);r['sentences']=len(ss);r['word_characters']=sum(len(w) for w in ww)
    r['paragraph_word_counts']=json.dumps([len(collect.W.findall(p)) for p in pp]);r['sentence_word_counts']=json.dumps([len(collect.W.findall(t)) for t in ss]);r['excluded_admin_words']=sum(len(collect.W.findall(p)) for p in excluded)
    sections=[]
    for sec in body.findall('./sec'):
     if is_admin(sec):continue
     ps=[collect.clean_para(p) for p in keep_paras(sec)]
     sections.append({'heading':' '.join(sec.find('title').itertext()) if sec.find('title') is not None else '', 'words':sum(len(collect.W.findall(p)) for p in ps),'paragraphs':sum(bool(p) for p in ps)})
    r['top_sections']=len(sections);r['section_detail']=json.dumps(sections,ensure_ascii=False)
   r['citation_xrefs']=refs(body) if body is not None else 0
   r['section_citation_xrefs']=json.dumps([{'heading':' '.join(sec.find('title').itertext()) if sec.find('title') is not None else '', 'citation_xrefs':refs(sec)} for sec in body.findall('./sec') if not is_admin(sec)]) if body is not None else '[]'
  except ET.ParseError:pass
rows.sort(key=lambda r:(r['form'],int(r['source_rank']) if str(r['source_rank']).isdigit() else 100000))
for kind in ['empirical','methods']:
 seen=0
 for r in rows:
  if r['form']==kind and r['status']=='measured':
   seen+=1
   if seen>200:r['status']='excluded';r['reason']='sample quota reached after ranked merge'
keys=['form','pmcid','title','year','journal','doi','source_url','cited_by_count','source_rank','source_type','jats_type','jats_category','citation_snapshot_utc','xml_sha256','xml_retrieved_utc','status','reason','title_words','abstract_words','caption_words','main_words','excluded_admin_words','paragraphs','sentences','word_characters','figures','tables','references','citation_xrefs','section_citation_xrefs','top_sections','section_detail','paragraph_word_counts','sentence_word_counts','license']
with (D/'manifest.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
(D/'search.json').write_text(json.dumps({k:v for k,v in meta.items() if isinstance(k,str)},indent=2))
def dist(v):
 v=sorted(v)
 if not v:return 'n/a'
 def q(p):
  x=(len(v)-1)*p;i=int(x);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(x-i)
 return f'{v[0]:,.0f} / {q(.25):,.1f} / {q(.5):,.1f} / {q(.75):,.1f} / {v[-1]:,.0f}'
lines=['# Empirical reports and methods papers: exploratory corpus', '', 'These are citation-ranked open-access samples, not global rankings or prescribed writing limits. Measured results reflect the sources and automated screens below; no independent full-text editorial suitability review was performed. Treat all results as provisional observed distributions. Counts can change as Europe PMC updates its index.', '', '## Discovery and classification', '', '- **Empirical:** pre-2015, Europe PMC randomized controlled trial publication-type metadata; JATS research-article, visible design/method and results headings, and at least 300 extracted prose words. This is a medical-trial subset, not all empirical research. Publication metadata and headings are screening evidence, not a manual assessment of every study.', '- **Methods:** MethodsX journal, OA, title matching a method-contribution cue; excluded review/protocol title cues and non-research JATS types. This is a single-journal subset, mostly later than 2014, and title cues are a conservative imperfect proxy for article type. Elsevier describes MethodsX as publishing methodological advances as well as protocols and reviews: https://www.elsevier.com/researcher/author/tools-and-resources/research-elements-journals. Individual titles and source records remain available for review.', '- Both pools use `SORT_CITED:y` from Europe PMC and retain the source citation count and query snapshot. Download failures, exclusions, and quota overflow appear in the manifest; not measured means not included in distributions. Candidate ranks record the order returned by Europe PMC; screening is bounded and may stop before every candidate is examined. High citation is a discovery signal, not evidence of writing quality.', '', '## Extraction policy', '', 'Europe PMC OA full-text JATS XML, cached outside this repository on the verified Samsung workspace. A manifest row has URL, title, date, journal, DOI, source publication type, JATS type/category, selection reason, SHA-256 and retrieval timestamp where XML was retrieved. The repository contains derived measurements, not the copyrighted source texts. Licenses should be checked per source.', '', 'Main text comprises paragraph elements in body prose, including nested sections and direct body paragraphs. Excludes abstract, references, headings, citations/xrefs, figures, tables, captions, formulas, lists, boxed text, and supplementary material. Administrative sections with exact headings such as acknowledgments, competing interests, author contributions, funding, ethics, data availability, abbreviations and pre-publication history are excluded and their prose-word count retained separately; heading variants may escape this screen. Nested administrative headings are excluded from section totals. Top-level section totals include nested section paragraphs; unsectioned direct-body paragraphs are in total but not section totals. Counts of abstract, title and captions are separate. Citation cross-references count JATS bibr xref elements, including grouped references as one marker, with top-level section locations recorded separately. Reference, figure and table counts are element counts, not guarantees of unique conceptual objects. Unicode letter/digit word tokens include internal hyphens/apostrophes; characters include token punctuation. Sentence splitting is a punctuation/capital heuristic and can err on abbreviations, formulas, and unusual typography. Paragraph and sentence count arrays and section counts are in the manifest. The summary does not measure communicative functions, meaning, prose/list proportions, or semantic evidence placement.', '', '## Reproduction', '', 'The scripts require Python 3 and the existing `requests` package. The first collector pass screens ranks 1–500; the separate continuation screens ranks 501–1000. The final merger applies a 200-work quota in source rank order and recomputes all measurements from cached XML, including the administrative exclusions. Queries and citation counts can change on a fresh run; the cache and snapshots are stored under `/workspace/repos/builderbob/.writing-corpus-cache/empirical-methods`.', '', '```sh', 'CORPUS_FORM=empirical python3 collect.py', 'CORPUS_FORM=methods CORPUS_OUTPUT=/workspace/repos/builderbob/.writing-corpus-cache/empirical-methods/methods-run python3 collect.py', 'python3 continue_methods.py', 'python3 summarize.py', '```', '', 'Run these commands from this directory. The recorded collection used six workers for the empirical pass and three for each methods pass; the default is three.', '', '## Results', '', 'Values below are minimum / first quartile / median / third quartile / maximum, with quartiles linearly interpolated across works. Paragraphs and sentences are totals per work; the manifest contains per-paragraph and per-sentence counts. These are observed ranges, not hard limits.', '']
for kind in ['empirical','methods']:
 rr=[r for r in rows if r['form']==kind];a=[r for r in rr if r['status']=='measured'];lines += [f'### {kind.title()}','',f"Measured **{len(a)}** of {len(rr)} screened candidates; target 200, shortfall {max(0,200-len(a))}. Status counts: "+', '.join(f'{s} {sum(r["status"]==s for r in rr)}' for s in sorted(set(r['status'] for r in rr)))+'.','', '| Measure | Observed range and quartiles |','| --- | --- |']
 for k,label in [('main_words','Main-text words'),('paragraphs','Paragraphs'),('sentences','Sentences'),('top_sections','Top-level sections'),('figures','Figures'),('tables','Tables'),('references','References'),('citation_xrefs','Citation markers')]:
  v=[int(r[k]) for r in a if r.get(k) not in ('',None)];lines.append(f'| {label} | {dist(v)} |')
 lines += ['']
 lines += ['| Publication year | Measured | Main-text words: min / Q1 / median / Q3 / max |','| --- | ---: | --- |']
 for label,lo,hi in [('Through 2014',0,2014),('2015–2019',2015,2019),('2020 onward',2020,9999)]:
  subset=[r for r in a if r.get('year','')[:4].isdigit() and lo<=int(r['year'][:4])<=hi]
  vals=[int(r['main_words']) for r in subset if r.get('main_words')]
  lines.append(f'| {label} | {len(subset)} | {dist(vals)} |')
 lines += ['']
(D/'summary.md').write_text('\n'.join(lines)+'\n')
print('summarized',len(rows))
