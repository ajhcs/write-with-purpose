#!/usr/bin/env python3
"""Extract specified source bodies, with no paragraph function decisions."""
import json, pathlib, hashlib, re, math, xml.etree.ElementTree as ET
from html.parser import HTMLParser
ROOT=pathlib.Path('/workspace/repos/builderbob/write-with-purpose')
PRIVATE=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/rule-calibration')
OUT=ROOT/'experiments/rule-calibration-2026-11-16/sampling'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s): return re.sub(r'\s+',' ',s).strip()
class Raw(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.parts=[]
 def handle_data(self,s): self.parts.append(s)
htmlrecords={x['id']:x for x in map(json.loads,open(ROOT/'experiments/corpus-analysis-2026-11-16/analysis/html-records.jsonl'))}
xmlrecords={x['pmcid']:x for x in map(json.loads,open(ROOT/'experiments/corpus-analysis-2026-11-16/analysis/xml-records.jsonl'))}
# Block boundaries manually identified from literal bylines, article starts, ends and adjacent furniture.
htmlspec=[('LF-d23d38c43ea7','A','argument/perspective',1,29),('LF-80bd6f30b443','A','argument/perspective',2,37),('LF-536f04360ed3','B','argument/perspective',2,43),('LF-fca9142fd337','A','personal reflection',6,39),('LF-2cb0e10879f3','A','personal reflection',4,18),('LF-03f718ef8cc6','B','personal reflection',1,24)]
xmlspec=[('PMC2867979','A'),('PMC4053896','A'),('PMC4566873','B')]
manifest=[]
def emit(id,stage,stratum,metadata,blocks,rawcheck):
 out=[]; paragraphs=[]; pos=0
 for block in blocks:
  text=norm(block['text'])
  if not text: continue
  if out: pos+=2
  start=pos; out.append(text); pos+=len(text)
  if block['kind']=='paragraph': paragraphs.append({'id':f'{id}-p{len(paragraphs)+1:03}', 'start':start,'end':pos,'text_sha256':hashlib.sha256(text.encode()).hexdigest()})
  block['start']=start; block['end']=pos; block['text']=text
 body='\n\n'.join(out); assert len(paragraphs)>=6
 chosen=[math.floor((i+.5)*len(paragraphs)/3) for i in range(3)]
 assert len(set(chosen))==3
 path=PRIVATE/(id+'.body.txt'); path.write_text(body,encoding='utf-8')
 for p in paragraphs: assert hashlib.sha256(body[p['start']:p['end']].encode()).hexdigest()==p['text_sha256']
 obj={'id':id,'stage':stage,'stratum':stratum,'provisional_form':stratum,'sampling_date':'2026-11-16',**metadata,'body_path':str(path),'body_sha256':sha(path),'offset_unit':'zero-based Unicode code points, end exclusive','paragraph_count':len(paragraphs),'paragraphs':paragraphs,'selected_paragraph_ids':[paragraphs[i]['id'] for i in chosen],'selected_zero_based_positions':chosen,'blocks':blocks,'raw_boundary_check':rawcheck}
 (PRIVATE/(id+'.json')).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
 manifest.append({k:obj[k] for k in ['id','stage','stratum','provisional_form','sampling_date','title','authors','source_path','source_sha256','body_path','body_sha256','paragraph_count','selected_paragraph_ids','selected_zero_based_positions']})
for id,stage,stratum,first,last in htmlspec:
 x=htmlrecords[id]; assert x['analysis_status']=='measured' and not x.get('hold_reason')
 raw=pathlib.Path(x['source_path']); assert sha(raw)==x['source_sha256']
 blocks=json.loads(pathlib.Path(x['blocks_path']).read_text())[first:last+1]
 # Identifiable page controls are excluded before the sampling frame is counted.
 blocks=[b for b in blocks if not re.fullmatch(r'\[adblock-[^]]+\]',b['text'].strip(),re.I)]
 assert blocks[0]['kind']=='paragraph' and blocks[-1]['kind']=='paragraph'
 # Check text exists in the actual HTML, ignoring inline tags and whitespace.
 parser=Raw(); parser.feed(raw.read_text(encoding='utf-8',errors='replace')); rawtext=norm(' '.join(parser.parts)); clean=lambda s: re.sub(r'[^\w]+','',s).casefold()
 rawcompact=clean(rawtext)
 checks=[]
 for b in blocks:
  if b['kind']!='paragraph': continue
  needle=clean(b['text']); checks.append(needle in rawcompact)
 assert all(checks), (id,[i for i,v in enumerate(checks) if not v])
 emit(id,stage,stratum,{'title':x['title'],'authors':x['authors'],'url':x['url'],'source_path':str(raw),'source_sha256':sha(raw),'normalized_source_blocks':x['blocks_path'],'scope':f'body block indices {first} through {last} inclusive'},blocks,{'all_paragraphs_found_in_orderless_raw_visible_text':True,'first_last_manually_reviewed':True,'note':'Article-body endpoints manually inspected; boilerplate outside slice excluded. Raw markup text compared after whitespace/punctuation folding.'})
for id,stage in xmlspec:
 x=xmlrecords[id]; raw=pathlib.Path(x['source_path']); assert sha(raw)==x['source_sha256']; root=ET.parse(raw).getroot(); body=root.find('.//body'); assert body is not None
 blocks=[]
 def walk(el):
  tag=el.tag.split('}')[-1]
  if tag in ('fig','table-wrap','supplementary-material','ref-list','ack','fn-group'): return
  if tag == 'sec' and (el.get('sec-type') in {'supplementary-material','ack','glossary','fn-group','ref-list','associated-data','contrib-info'} or el.get('id','').startswith(('notes','funding-statement')) or norm(' '.join(el.find('title').itertext()) if el.find('title') is not None else '').casefold() in {'supplementary information','supplementary material','data availability','references','competing interests',"authors' contributions",'acknowledgements','contributor information'}): return
  if tag in ('title','p','list-item','preformat','disp-quote'):
   text=norm(' '.join(el.itertext()))
   if text:
    kind={'title':'heading','p':'paragraph','list-item':'list_item','preformat':'code','disp-quote':'quotation'}[tag]
    if tag=='p' and re.search(r'\bOR\b.*\bAND\b', text) and text.startswith('('): kind='search_query'
    blocks.append({'kind':kind,'text':text})
   return
  for child in el: walk(child)
 walk(body)
 assert blocks[0]['kind'] in ('heading','paragraph') and blocks[-1]['kind'] in ('heading','paragraph')
 emit(id,stage,'research/synthesis',{'title':x['title'],'authors':x['authors'],'outlet':x['journal'],'url':'https://pmc.ncbi.nlm.nih.gov/articles/'+id+'/','source_path':str(raw),'source_sha256':sha(raw),'scope':'JATS body, excluding figures, tables, supplements, acknowledgements and references'},blocks,{'source':'JATS body direct element boundaries','first':blocks[0]['text'][:180],'last':blocks[-1]['text'][-180:]})
(OUT/'source-manifest.partial.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('\n'.join(f"{x['id']} {x['stage']} {x['stratum']} {x['paragraph_count']} {x['selected_zero_based_positions']}" for x in manifest))
