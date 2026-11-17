#!/usr/bin/env python3
"""Offline HTML corpus measurement; source text and normalized blocks remain in private cache."""
import collections, hashlib, importlib.util, json, re, sys
from pathlib import Path
from urllib.parse import urlparse
from metrics import measure_document, word_tokens
ROOT=Path(__file__).resolve().parents[2]/'form-corpus-2026-11-16'
OUT=Path(__file__).resolve().parent
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis/html')
GRAHAM=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16/paulgraham')
MEMOS=Path('/workspace/tmp/builderbob/writing-corpus/proposal-memo')

def loadmod(path,name):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(ROOT/'essays'))
memo=loadmod(ROOT/'proposal-memo/measure.py','oldmemo')
pg=loadmod(ROOT/'essays/public_essays.py','oldpg')
def lines(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def norm(s):return ' '.join((s or '').split())
def titlekey(s):return set(re.findall(r'[^\W_]+',s.casefold()))
def digest(b):return hashlib.sha256(b).hexdigest()
def plain(n):
 if isinstance(n,str):return n
 if n.tag in {'script','style','noscript','svg','nav','footer','aside','form','button'}:return ''
 return ' '.join(plain(c) for c in n.children)
def excluded(n):
 if isinstance(n,str):return False
 if n.tag in {'script','style','noscript','svg','nav','footer','aside','form','button','figure'}:return True
 a=n.a; label=' '.join([a.get('id',''),a.get('class',''),a.get('role',''),a.get('aria-label','')]).lower()
 return bool(re.search(r'(^|[\s_-])(nav|footer|sidebar|related|recommend|newsletter|subscribe|advert|author-bio|biography|social|share|comment|breadcrumb|pagination|byline)([\s_-]|$)',label))
def extract_generic(raw,title):
 tree=memo.Tree();tree.feed(raw.decode('utf-8',errors='replace')); nodes=list(memo.walk(tree.root))
 observed=[norm(plain(n)) for n in nodes if n.tag in ('title','h1')]
 observed += [n.a.get('content','') for n in nodes if n.tag=='meta' and n.a.get('property','').lower() in ('og:title','twitter:title')]
 keys=titlekey(title); match=max((len(keys & titlekey(x))/len(keys) for x in observed if keys),default=0)
 if match < .6:return [],{},dict(title_match_score=round(match,2),reason='expected title not supported by title, h1 or og:title')
 candidates=[n for n in nodes if n.tag in ('article','main') or n.a.get('role')=='main' or re.search(r'(article-body|article-content|entry-content|post-content|story-body|field--name-body)',n.a.get('class','')+' '+n.a.get('id',''),re.I)]
 def score(n):return sum(len(word_tokens(norm(plain(x)))) for x in memo.walk(n) if x.tag=='p' and not excluded(x))
 if not candidates:return [],{},dict(title_match_score=round(match,2),reason='no semantic article/main/body container')
 root=max(candidates,key=score); blocks=[];section='unsectioned';objects=collections.Counter()
 def visit(n):
  nonlocal section
  if isinstance(n,str) or excluded(n):return
  if n.tag=='a' and n.a.get('href'):objects['links']+=1
  if n.tag=='table':objects['tables']+=1
  if n.tag in ('h1','h2','h3','h4','h5','h6','p','li','pre','blockquote','figcaption'):
   text=norm(plain(n))
   if not text:return
   if n.tag[0]=='h' and len(n.tag)==2:
    if re.match(r'^(related|recommended|more from|about the author|newsletter|comments|subscribe|read more)\b',text,re.I):return
    section='section-'+str(len(blocks)+1);blocks.append(dict(kind='heading',text=text,section_id=section,heading_level=int(n.tag[1])))
   else:
    kind={'p':'paragraph','li':'list_item','pre':'code','blockquote':'quote','figcaption':'caption'}[n.tag]
    # Nested block elements are independently processed rather than counted twice.
    if any(not isinstance(c,str) and c.tag in ('p','li','pre','blockquote') for c in n.children):
     for c in n.children:visit(c)
     return
    blocks.append(dict(kind=kind,text=text,section_id=section))
   return
  for c in n.children:visit(c)
 visit(root)
 return blocks,dict(objects),dict(title_match_score=round(match,2),container=root.tag,container_id=root.a.get('id'),container_class=root.a.get('class'),candidate_containers=len(candidates))
def graham(raw):
 p=pg.Page()
 try:s=raw.decode('utf-8')
 except UnicodeDecodeError:s=raw.decode('windows-1252',errors='replace')
 p.feed(s);b=max(p.blocks,key=len,default=''); pars=[norm(x) for x in re.split(r'\n\s*\n+',b) if x.strip()]
 for i,t in enumerate(pars[:5]):
  if re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',t,re.I):pars=pars[i+1:];break
 for i,t in enumerate(pars):
  if re.match(r'^(Notes?|Acknowledg(?:e)?ments?)(?:\s|:|$)|^Thanks to\b|^Related:',t,re.I):pars=pars[:i];break
 return [dict(kind='paragraph',text=t,section_id='unsectioned') for t in pars],{},dict(container='longest Verdana font block',boundary='double breaks; date and notes removed when detected')
def memo_extract(raw,rec):
 tree=memo.Tree();tree.feed(raw.decode('utf-8',errors='replace'));title,dates,units=memo.extract(tree.root,rec['url'].rsplit('/',1)[-1]);blocks=[];section='unsectioned'
 for kind,t in units:
  if kind in ('h4','h5','heading'):
   section='section-'+str(len(blocks)+1);blocks.append(dict(kind='heading',text=t,section_id=section,heading_level=4 if kind in ('h4','heading') else 5))
  else:blocks.append(dict(kind='list_item' if kind in ('li','choice') else 'paragraph',text=t,section_id=section))
 return blocks,{},dict(container='FRUS document div',observed_title=title,date=dates,unit='transcription excludes editorial footnotes and opener')
def main():
 CACHE.mkdir(parents=True,exist_ok=True);records=[];seen={}
 def process(rec,path,mode,expected_hash=None,hold=None,exclude=None):
  rec.update(source_path=str(path) if path else None,source_sha256=None,body_sha256=None,body_completeness='unverified',source_tier='provisional',analysis_status=None,hold_reason=None,metrics=None)
  if not path or not path.exists():rec.update(analysis_status='missing',hold_reason='no saved file');records.append(rec);return
  raw=path.read_bytes();sha=digest(raw);rec['source_sha256']=sha;rec['source_bytes']=len(raw)
  if hold:rec.update(analysis_status='policy_hold',hold_reason=hold);records.append(rec);return
  if exclude:rec.update(analysis_status='excluded',hold_reason=exclude);records.append(rec);return
  if expected_hash and sha!=expected_hash:rec.update(analysis_status='hash_mismatch',hold_reason='source hash differs from manifest');records.append(rec);return
  if sha in seen:rec.update(analysis_status='duplicate_raw',duplicate_of=seen[sha],hold_reason='same source bytes already measured');records.append(rec);return
  try:
   blocks,objects,audit=graham(raw) if mode=='graham' else memo_extract(raw,rec) if mode=='memo' else extract_generic(raw,rec['title'])
   # Audited source-specific boundary corrections; no extracted prose in the repository.
   if rec['id']=='official-heller-brief':
    stop=next((i for i,b in enumerate(blocks) if b['text'].strip().casefold()=='respectfully submitted.'),len(blocks))
    blocks=blocks[:stop];audit['boundary_correction']='cut before signature and trailing footnotes'
   if rec['id']=='LF-f2db6fcab11c':
    blocks=[b for b in blocks if not (b['text'].startswith('This essay has been drawn from') or re.match(r'^\[\d+\]',b['text']) or b['text']=='✖')]
    audit['boundary_correction']='removed editorial introduction, control and numbered endnote'
   rec['extraction_audit']=audit
   if sum(len(word_tokens(b['text'])) for b in blocks if b['kind']=='paragraph')<100:
    rec.update(analysis_status='extraction_failed',hold_reason=audit.get('reason','fewer than 100 extracted prose words'));records.append(rec);return
   body=json.dumps(blocks,ensure_ascii=False,separators=(',',':')).encode();rec['body_sha256']=digest(body)
   dest=CACHE/(rec['corpus']+'-'+re.sub(r'[^A-Za-z0-9_.-]','_',str(rec['id']))+'.json');dest.write_bytes(body+b'\n');rec['blocks_path']=str(dest)
   met=measure_document(blocks,objects);met['heading_sequence']=[{'section_id':x['section_id'],'level':x['level']} for x in met['heading_sequence']]
   rec.update(analysis_status='measured',metrics=met);seen[sha]=rec['id']
  except Exception as e:rec.update(analysis_status='extraction_failed',hold_reason=type(e).__name__+': '+str(e)[:200])
  records.append(rec)
 screens={x['url']:x for x in lines(ROOT/'essays/manual-screen.jsonl')}
 for x in lines(ROOT/'essays/public_archive_measurements.jsonl'):
  url=x['source_url'];screen=screens.get(url);rec=dict(id='pg-'+str(x['archive_rank']),corpus='paul_graham_archive',title=x['title'],authors=[x['author']],date=x.get('date_label'),url=url,form=screen['form'] if screen else 'FORM_UNRESOLVED',form_evidence=screen['basis'] if screen else 'author archive only; no individual form screening',selection=x.get('selection'))
  process(rec,GRAHAM/urlparse(url).path.rsplit('/',1)[-1],'graham',x.get('sha256'))
 for x in lines(ROOT/'fulltext-retrieval/personal/manifest.jsonl'):
  r=x['retrieval'];path=Path(r['file']) if r.get('file') else None;policy=x.get('robots_policy_audit','');manual=x.get('manual_body_audit') or {};candidate=x.get('candidate_article_body_not_confirmed',False)
  rec=dict(id=x['id'],corpus='personal_retrieval',title=x['title'],authors=[x.get('author')],date=x.get('date_display'),url=r.get('final_url') or x.get('target_url'),form='FORM_UNRESOLVED',retrieval_status=r.get('status'),policy_audit=policy,source_identity=r.get('source_identity'),manual_audit=manual or None)
  hold=policy if policy.startswith('unresolved') else None
  exclude=None if candidate else 'known landing, short body, wrong destination, or no confirmed article candidate'
  if manual.get('assessment') in ('no_article_body_found','wrong_destination'):exclude=manual['assessment']
  if path and path.suffix.lower()=='.pdf':rec.update(analysis_status='other_format',source_path=str(path),hold_reason='PDF routed to PDF analysis');records.append(rec);continue
  process(rec,path,'generic',r.get('sha256'),hold,exclude)
 memo_meta={x['id']:x for x in json.loads((ROOT/'proposal-memo/metrics.json').read_text())}
 for x in json.loads((ROOT/'proposal-memo/candidates.json').read_text()):
  if x['form']!='decision memo':continue
  meta=memo_meta[x['id']];rec=dict(id=x['id'],corpus='frus_decision_memo',title=meta['title'],authors=[],date=meta['date'],url=x['url'],form='decision_memo',classification_basis=x['classification_basis'])
  process(rec,MEMOS/(x['id']+'.html'),'memo',meta['sha256'])
 # Earlier publisher-probe caches predate the retained robots policy audit. Their
 # original rules and AI-input signals were not preserved, so candidate bodies
 # are held just like the reused Vogue capture in the personal manifest.
 for x in lines(ROOT/'essays/longform_public_probes.jsonl'):
  if not x.get('sha256'):continue
  url=x['source_url'];path=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16/longform')/(digest(url.encode())+'.html')
  prior=next((r for r in records if r.get('source_sha256')==x['sha256']),None)
  rec=dict(id='probe-'+digest(url.encode())[:12],corpus='longform_publisher_probe',title=x['title'],authors=[],date=None,url=url,form='FORM_UNRESOLVED',retrieval_status=x['status'],retrieved_utc=x.get('retrieved_utc'),robots_status=x.get('robots_status'),robots_crawl_delay=x.get('robots_crawl_delay'),selection=x.get('selection'),prior_record_same_raw=prior['id'] if prior else None)
  hold='original robots rules and AI-input signals not retained for this capture' if x['status']=='extracted_unvalidated' else None
  exclude='prior probe found no article body; body not processed' if x['status']=='no_article_body' else None
  process(rec,path,'generic',x['sha256'],hold,exclude)
 for x in json.loads((ROOT/'fulltext-retrieval/law/manifest.json').read_text()):
  if x.get('id')!='official-heller-brief':continue
  rec=dict(id=x['id'],corpus='official_legal_example',title=x['title'],authors=[],date=None,url=x.get('final_url'),form='FORM_UNRESOLVED',doi=x.get('doi'),source_identity=x.get('source_identity'))
  process(rec,Path(x['file_path']) if x.get('file_path') else None,'generic',x.get('sha256'))
 (OUT/'html-records.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in records))
 print(json.dumps({k:dict(collections.Counter(x['analysis_status'] for x in records if x['corpus']==k)) for k in sorted(set(x['corpus'] for x in records))},indent=2))
if __name__=='__main__':main()
