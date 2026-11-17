#!/usr/bin/env python3
"""Collect source-typed Markdown pages; output metadata and descriptive signals, not prose."""
import concurrent.futures, csv, datetime, hashlib, json, re, statistics, time
from pathlib import Path
import requests
from markdown_it import MarkdownIt

HERE=Path(__file__).resolve().parent
CACHE=Path('/workspace/tmp/builderbob/writing-corpus/explanation-tutorial'); CACHE.mkdir(parents=True,exist_ok=True)
SPECS={
 'kubernetes/website': [('content/en/docs/concepts/','explanation'),('content/en/docs/tutorials/','tutorial')],
 'canonical/ubuntu-server-documentation':[('docs/explanation/','explanation'),('docs/tutorial/','tutorial')],
 'canonical/ubuntu-desktop-documentation':[('docs/explanation/','explanation'),('docs/tutorial/','tutorial')],
 'canonical/maas':[('docs/explanation/','explanation'),('docs/tutorials/','tutorial')],
 'canonical/lxd':[('doc/explanation/','explanation'),('doc/tutorial/','tutorial')],
 'canonical/landscape-documentation':[('docs/explanation/','explanation')],
 'canonical/pebble':[('docs/explanation/','explanation'),('docs/tutorial/','tutorial')],
 'canonical/rockcraft':[('docs/explanation/','explanation'),('docs/tutorial/','tutorial')],
 'canonical/charmcraft':[('docs/explanation/','explanation'),('docs/tutorial/','tutorial')],
 'canonical/snapcraft':[('docs/explanation/','explanation'),('docs/tutorials/','tutorial')],
}
s=requests.Session(); s.headers['User-Agent']='writing-form-corpus-research/1.0'; stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(url):
 for attempt in range(3):
  try:
   r=s.get(url,timeout=45); r.raise_for_status(); return r
  except requests.RequestException:
   if attempt==2: raise
   time.sleep(2**attempt)
def jget(url): return get(url).json()
manifest=[]; candidates=[]; failures=[]
for repo,specs in SPECS.items():
 try:
  info=jget('https://api.github.com/repos/'+repo); branch=info['default_branch']; commit=jget(f'https://api.github.com/repos/{repo}/commits/{branch}')['sha']
  tree=jget(f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1')
  license=info.get('license') or {}; manifest.append(dict(repo=repo,branch=branch,commit=commit,license_spdx=license.get('spdx_id'),license_url=license.get('url'),tree_truncated=tree.get('truncated'),retrieved_at_utc=stamp,selection_signal='official project-maintained documentation; no readership or citation ranking established'))
  for item in tree.get('tree',[]):
   p=item['path']; base=p.rsplit('/',1)[-1].lower()
   if item['type']!='blob' or not p.endswith('.md') or base in ('index.md','_index.md','readme.md') or '/reuse/' in p: continue
   for prefix,form in specs:
    if p.startswith(prefix): candidates.append((repo,commit,p,form,license.get('spdx_id'))); break
 except Exception as e: failures.append({'repo':repo,'stage':'discovery','error':str(e)})
(HERE/'sources.json').write_text(json.dumps({'retrieved_at_utc':stamp,'sources':manifest,'failures':failures},indent=2)+'\n')
md=MarkdownIt('commonmark').enable('table')
wordre=re.compile(r"[A-Za-z]+(?:['’\-][A-Za-z]+)*|\d+(?:\.\d+)?")
def words(t): return wordre.findall(t)
def textinline(tok):
 return ''.join(c.content if c.type in ('text','softbreak','hardbreak') else ' ' for c in (tok.children or []))
def measure(body):
 # Exclude source front matter. Shortcodes and templates may contain transcluded content.
 body=re.sub(r'\A\s*(---|\+\+\+)\s*\n.*?\n\1\s*\n','',body,flags=re.S)
 shortcode=len(re.findall(r'{{[<%{]',body)); body=re.sub(r'{{[<%{].*?[>%}]}}',' ',body,flags=re.S)
 toks=md.parse(body); paras=[]; heads=[]; sections=[]; current={'heading_level':0,'prose_words':0}; code=lists=figures=tables=links=quotes=0; in_list=0
 for t in toks:
  if t.type in ('bullet_list_open','ordered_list_open'): lists+=1; in_list+=1
  elif t.type in ('bullet_list_close','ordered_list_close'): in_list-=1
  elif t.type in ('fence','code_block'): code+=1
  elif t.type=='blockquote_open': quotes+=1
  elif t.type=='table_open': tables+=1
  elif t.type=='heading_open':
   sections.append(current); current={'heading_level':int(t.tag[1]),'prose_words':0}; heads.append(int(t.tag[1]))
  elif t.type=='inline':
   figures+=sum(c.type=='image' for c in (t.children or [])); links+=sum(c.type=='link_open' for c in (t.children or []))
 # paragraphs only, avoiding heading, table cells and list prose; latter counted separately.
 in_list=0; prose=[]; list_words=0
 for i,t in enumerate(toks):
  if t.type in ('bullet_list_open','ordered_list_open'): in_list+=1
  elif t.type in ('bullet_list_close','ordered_list_close'): in_list-=1
  elif t.type=='paragraph_open' and i+1<len(toks) and toks[i+1].type=='inline':
   value=textinline(toks[i+1]); n=len(words(value))
   if in_list: list_words+=n
   elif n: prose.append(value)
 # Derive sections in a separate pass.
 sections=[]; current={'heading_level':0,'prose_words':0}; in_list=0
 for i,t in enumerate(toks):
  if t.type=='heading_open': sections.append(current); current={'heading_level':int(t.tag[1]),'prose_words':0}
  elif t.type in ('bullet_list_open','ordered_list_open'): in_list+=1
  elif t.type in ('bullet_list_close','ordered_list_close'): in_list-=1
  elif t.type=='paragraph_open' and not in_list and i+1<len(toks) and toks[i+1].type=='inline': current['prose_words']+=len(words(textinline(toks[i+1])) )
 sections.append(current)
 total_section_words=sum(x['prose_words'] for x in sections)
 for x in sections: x['prose_share']=round(x['prose_words']/total_section_words,4) if total_section_words else None
 lens=[len(words(x)) for x in prose]; allwords=words(' '.join(prose)); sentences=[len(words(x)) for p in prose for x in re.split(r'(?<=[.!?])\s+',p.strip()) if words(x)]
 return dict(prose_words=len(allwords),prose_paragraphs=len(lens),paragraph_word_counts=lens,sentence_word_counts=sentences,mean_word_characters=round(sum(len(x) for x in allwords)/len(allwords),3) if allwords else None,headings=len(heads),heading_depths=heads,sections=sections,list_blocks=lists,list_words_approx=list_words,code_blocks=code,links=links,images=figures,tables=tables,blockquotes=quotes,shortcode_occurrences=shortcode)
def run(c):
 repo,sha,path,form,license=c
 url=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'
 try:
  data=get(url).content
  cache=CACHE/hashlib.sha256(url.encode()).hexdigest(); cache.write_bytes(data)
  body=data.decode('utf-8'); m=measure(body)
  title=re.search(r'^title\s*:\s*["\']?(.+?)["\']?\s*$',body,re.M) or re.search(r'^#\s+(.+)$',body,re.M)
  title=title.group(1).strip(' "\'') if title else path.rsplit('/',1)[-1][:-3].replace('-',' ').replace('_',' ')
  declared_match=re.search(r'^content_type:\s*(\S+)',body,re.M) if repo=='kubernetes/website' else None
  declared=declared_match.group(1) if declared_match else None
  expected='concept' if form=='explanation' else 'tutorial'
  status='candidate_source_typed_needs_human_review' if m['prose_words']>=120 else 'excluded_under_120_prose_words_or_fragment'
  if declared and declared != expected: status='excluded_conflicting_declared_type'
  return dict(id=hashlib.sha256(url.encode()).hexdigest()[:16],repo=repo,path=path,source_url=f'https://github.com/{repo}/blob/{sha}/{path}',raw_url=url,commit=sha,title=title,original_type=declared or ('directory: concepts' if repo=='kubernetes/website' and form=='explanation' else 'directory: '+form),proposed_form=form,classification_basis='official documentation directory; purpose and suitability require human review',attribution=f'{repo} project contributors',license_spdx=license,sha256=hashlib.sha256(data).hexdigest(),retrieved_at_utc=stamp,selection_signal='source-owner-maintained documentation; no readership/citation ranking',unit='individual documentation page',acquisition_stage='full source downloaded; extraction approximate',screening_status=status,metrics=m)
 except Exception as e: return dict(repo=repo,path=path,proposed_form=form,screening_status='acquisition_failed',error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool: records=list(pool.map(run,candidates))
with (HERE/'records.jsonl').open('w') as f:
 for r in records: f.write(json.dumps(r,ensure_ascii=False)+'\n')
columns=['id','repo','path','title','source_url','commit','license_spdx','sha256','retrieved_at_utc','original_type','proposed_form','classification_basis','screening_status','prose_words','prose_paragraphs','headings','list_words_approx','list_blocks','code_blocks','links','images','tables','blockquotes','shortcode_occurrences']
with (HERE/'measurements.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore'); w.writeheader()
 for r in records: w.writerow({**r,**r.get('metrics',{})})
print(json.dumps({'candidate_files':len(candidates),'status_counts':{x:sum(r['screening_status']==x for r in records) for x in set(r['screening_status'] for r in records)},'forms':{x:sum(r.get('proposed_form')==x and r['screening_status'].startswith('candidate') for r in records) for x in ('explanation','tutorial')},'discovery_failures':failures},indent=2))
