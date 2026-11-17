#!/usr/bin/env medsci-pdf-python
"""Extract approximate PDF text; all inputs are data, not instructions."""
import hashlib, json, re, sys, statistics
from collections import Counter
from pathlib import Path
import fitz
from metrics import measure_document, word_tokens

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis/pdf')
CACHE.mkdir(parents=True, exist_ok=True)
OUT=ROOT/'analysis/pdf-records.jsonl'
MANIFESTS={k:REPO/'experiments/form-corpus-2026-11-16/fulltext-retrieval'/v for k,v in {'business':'business/retrieval_manifest.jsonl','engineering':'engineering/manifest.jsonl','law':'law/manifest.json','personal':'personal/manifest.jsonl'}.items()}
DOI=re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def selected(row):
 for r in (row,row.get('retrieval') or {}):
  for key in ('file','file_path'):
   val=r.get(key)
   if isinstance(val,str) and val.lower().endswith('.pdf'): return Path(val)
def rowmeta(r):
 return {k:r.get(k) for k in ('id','source_id','title','authors','author','doi','venue','outlet','date','year_display','version','source_identity','status','result','fulltext_status','body_completeness','sha256','file_sha256') if r.get(k) is not None}
def page_order(blocks,w):
 # Wide blocks divide bands; within each band, sort left column before right.
 wide=[b for b in blocks if b['bbox'][0]<w*.45 and b['bbox'][2]>w*.58]
 narrow=[b for b in blocks if b not in wide]
 left=[b for b in narrow if (b['bbox'][0]+b['bbox'][2])/2 < w*.5]
 right=[b for b in narrow if (b['bbox'][0]+b['bbox'][2])/2 >= w*.5]
 two=len(left)>=2 and len(right)>=2 and min(b['bbox'][0] for b in right)>w*.43
 if not two: return sorted(blocks,key=lambda b:(b['bbox'][1],b['bbox'][0])),False
 out=[]; pending=narrow[:]
 for b in sorted(wide,key=lambda b:b['bbox'][1]):
  top=b['bbox'][1]; before=[x for x in pending if x['bbox'][1]<top]; pending=[x for x in pending if x not in before]
  out.extend(sorted(before,key=lambda x:(0 if (x['bbox'][0]+x['bbox'][2])/2<w*.5 else 1,x['bbox'][1]))); out.append(b)
 out.extend(sorted(pending,key=lambda x:(0 if (x['bbox'][0]+x['bbox'][2])/2<w*.5 else 1,x['bbox'][1])))
 return out,True
def extract(item):
 p=item['path']; digest=sha(p); rid=item['domain']+'-'+digest[:16]; target=CACHE/(rid+'.json')
 rec={'record_id':rid,'collection_domain':item['domain'],'path':str(p),'sha256':digest,'bytes':p.stat().st_size,'source_manifest':item.get('manifest'),'source_metadata':item.get('metadata',{}),'analysis_status':'failed','extraction_tier':'pdf_approximate','semantic_form':'unresolved','profile_eligible':False,'profile_eligibility_reason':'PDF layout and semantic boundaries require individual audit; source identity and version require verification','body_completeness':'unverified'}
 try:
  doc=fitz.open(str(p)); pages=[]; candidates=[]; allblocks=[]; sizes=[]
  for i,page in enumerate(doc):
   raw=page.get_text('dict',sort=False,flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES); blocks=[]
   for b in raw.get('blocks',[]):
    if b.get('type')!=0: continue
    lines=[]; spans=[]
    for line in b.get('lines',[]):
     s=[{'text':s.get('text',''),'size':s.get('size'),'font':s.get('font'),'flags':s.get('flags'),'bbox':s.get('bbox')} for s in line.get('spans',[]) if s.get('text','').strip()]
     if s: lines.append(''.join(x['text'] for x in s)); spans.extend(s); sizes.extend(x['size'] for x in s if x['size'])
    text=' '.join(lines).strip()
    if text: blocks.append({'page':i+1,'bbox':b['bbox'],'text':text,'lines':lines,'spans':spans})
   ordered,two=page_order(blocks,page.rect.width)
   for b in ordered:
    b['edge']=b['bbox'][1]<page.rect.height*.09 or b['bbox'][3]>page.rect.height*.91
    if b['edge']: candidates.append(re.sub(r'\d+', '#',re.sub(r'\s+',' ',b['text'].lower())).strip())
   pages.append({'page':i+1,'width':page.rect.width,'height':page.rect.height,'raw_block_count':len(blocks),'text_characters':sum(len(x['text']) for x in blocks),'raw_word_tokens':sum(len(word_tokens(x['text'])) for x in blocks),'approx_two_column':two,'image_blocks':len(page.get_images())})
   allblocks.extend(ordered)
  repeated={k for k,n in Counter(candidates).items() if n>=max(2, int(len(pages)*.4))}
  body=[]; excluded=[]; refs=False; refstart=None; med=statistics.median(sizes) if sizes else 0
  for b in allblocks:
   t=b['text']; norm=re.sub(r'\d+', '#',re.sub(r'\s+',' ',t.lower())).strip(); reason=None
   if b['edge'] and norm in repeated: reason='repeated_edge_text'
   elif b['edge'] and re.fullmatch(r'\s*(?:\d+|[ivxlcdm]+)\s*',t,re.I): reason='folio'
   elif re.fullmatch(r'\s*(references|bibliography|works cited|literature cited)\s*',t,re.I): refs=True; refstart=b['page']; reason='reference_section_start'
   elif refs: reason='after_reference_section_start'
   if reason: excluded.append({'page':b['page'],'bbox':b['bbox'],'reason':reason}); b['excluded_reason']=reason; continue
   # Block classification remains heuristic: avoid treating equations/tables as certain paragraphs.
   words=word_tokens(t); mean_size=sum(s['size'] for s in b['spans'] if s.get('size'))/max(1,len(b['spans']))
   heading=(len(words)<=12 and not re.search(r'[.!?]$',t) and mean_size>med*1.13)
   kind='heading' if heading else 'caption' if re.match(r'^(figure|fig\.|table)\s*\d',t,re.I) else 'list_item' if re.match(r'^\s*(?:[•●▪]|\d+[.)])\s+',t) else 'paragraph'
   b['kind']=kind; body.append({'kind':kind,'text':t,'page':b['page'],'bbox':b['bbox']})
  measures=measure_document(body); measures.pop('heading_sequence',None)
  text1='\n'.join(b['text'] for b in allblocks if b['page']<=2); dois=sorted(set(x.rstrip('.,;)') for x in DOI.findall(text1)))[:20]
  flags=['approximate_pdf_layout','paragraph_boundaries_unvalidated','semantic_form_unresolved','identity_version_and_completeness_unverified','tables_formulas_and_captions_may_contaminate_text']
  if any(x['approx_two_column'] for x in pages): flags.append('two_column_order_heuristic')
  if any(x['text_characters']<100 for x in pages): flags.append('pages_with_little_or_no_extractable_text')
  if not allblocks: flags.append('no_extractable_text_ocr_not_attempted')
  if refstart: flags.append('reference_cutoff_heuristic')
  metadata=doc.metadata or {}; expected=item.get('metadata',{}).get('expected_sha256') or item.get('metadata',{}).get('file_sha256') or item.get('metadata',{}).get('sha256')
  if expected and expected != digest: flags.append('source_hash_mismatch')
  rec['manifest_hash_check']='match' if expected and expected == digest else 'mismatch' if expected else 'not_available'
  rec.update({'analysis_status':'extracted' if allblocks else 'no_extractable_text','page_count':len(pages),'per_page':pages,'pdf_metadata':{k:metadata.get(k) for k in ('title','author','subject','creationDate') if metadata.get(k)},'observed_first_two_pages_dois':dois,'approximate_metrics':measures,'quality_flags':flags,'reference_cutoff_page':refstart,'excluded_block_counts':dict(Counter(x['reason'] for x in excluded)),'extraction_path':str(target)})
  target.write_text(json.dumps({'source_sha256':digest,'pages':pages,'ordered_source_blocks':allblocks,'normalized_blocks':body,'excluded_block_spans':excluded},ensure_ascii=False)+'\n')
  doc.close()
 except Exception as e: rec['error']=f'{type(e).__name__}: {e}'; rec['quality_flags']=['extraction_failed']
 return rec

def main():
 items=[]
 for a in json.loads((ROOT/'inputs/attachments-manifest.json').read_text()): items.append({'path':Path(a['copy_path']),'domain':'user_attachment','manifest':str(ROOT/'inputs/attachments-manifest.json'),'metadata':{'filename':a['filename'],'expected_sha256':a['sha256']}})
 for domain,p in MANIFESTS.items():
  rows=json.loads(p.read_text()) if p.suffix=='.json' else [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
  for row in rows:
   path=selected(row)
   if path: items.append({'path':path,'domain':domain,'manifest':str(p),'metadata':rowmeta(row)})
 proposal_manifest=REPO/'experiments/form-corpus-2026-11-16/proposal-memo/proposal-discovery.json'
 proposal_dir=Path('/workspace/tmp/builderbob/writing-corpus/proposal-memo')
 for row in json.loads(proposal_manifest.read_text()):
  match=re.fullmatch(r'proposal-uw-(\d+)',row.get('id',''))
  if match:
   items.append({'path':proposal_dir/('uw-sample-'+match.group(1)+'.pdf'),'domain':'proposal','manifest':str(proposal_manifest),'metadata':rowmeta(row) | {'url':row.get('url'),'expected_sha256':row.get('sha256')}})
 records=[]; seen={}
 for item in items:
  p=item['path']
  if not p.is_file(): records.append({'path':str(p),'collection_domain':item['domain'],'source_metadata':item.get('metadata'),'analysis_status':'source_missing','profile_eligible':False}); continue
  h=sha(p)
  if h in seen:
   records.append({'path':str(p),'sha256':h,'collection_domain':item['domain'],'source_metadata':item.get('metadata'),'analysis_status':'byte_duplicate_excluded','duplicate_of':seen[h],'profile_eligible':False}); continue
  rec=extract(item); records.append(rec); seen[h]=rec['record_id']; print(rec['analysis_status'],item['domain'],p.name,flush=True)
 with OUT.open('w') as f:
  for rec in records: f.write(json.dumps(rec,ensure_ascii=False)+'\n')
 print('RECORDS',len(records),dict(Counter(r['analysis_status'] for r in records)))
if __name__=='__main__': main()
