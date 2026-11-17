#!/usr/bin/env python3
"""Read-only collection; stores derived metrics, metadata and hashes, not page text."""
import concurrent.futures, collections, datetime, hashlib, html.parser, json, re, statistics, time, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
import requests
OUT=Path(__file__).resolve().parent
UA={'User-Agent':'WritingCorpusResearch/1.0 (descriptive analysis; respectful access)'}
WORD=re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")
def words(s): return WORD.findall(s)
def sentences(s): return [x for x in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9“\"\(])',s.strip()) if x.strip()]
def stats(x):
 x=sorted(x)
 if not x:return {'n':0}
 def pct(q):return round(x[round((len(x)-1)*q)],2)
 return {'n':len(x),'min':x[0],'p25':pct(.25),'median':statistics.median(x),'p75':pct(.75),'max':x[-1],'mean':round(statistics.mean(x),2)}
class Page(html.parser.HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True); self.stack=[];self.active=False;self.found=False;self.blocks=[];self.capture=None;self.buf=[];self.title='';self.canonical='';self.date='';self.skip=0
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='link' and a.get('rel')=='canonical':self.canonical=a.get('href','')
  if t=='time' and not self.date:self.date=a.get('datetime','')
  if t=='main': self.active=True; self.found=True
  if not self.active:return
  if t in ('script','style','nav','aside','footer'):self.skip+=1;return
  if self.skip:return
  if self.capture is None and (t in ('p','pre','li','table','figure') or re.fullmatch(r'h[1-6]',t)):
   self.capture=t;self.buf=[]
  elif self.capture and t=='br':self.buf.append(' ')
 def handle_endtag(self,t):
  if not self.active:return
  if t in ('script','style','nav','aside','footer') and self.skip:self.skip-=1;return
  if self.skip:return
  if self.capture==t:
   s=' '.join(''.join(self.buf).split());
   if s:self.blocks.append((t,s))
   self.capture=None;self.buf=[]
  if t=='main':self.active=False
 def handle_data(self,d):
  if self.active and not self.skip and self.capture:self.buf.append(d)
def sitemap(u):
 r=requests.get(u,headers=UA,timeout=60);r.raise_for_status();root=ET.fromstring(r.content)
 return [(next((c.text for c in x if c.tag.endswith('loc')),None),next((c.text for c in x if c.tag.endswith('lastmod')),None)) for x in root if x.tag.endswith('url')]
def interleave(urls, key):
 buckets=collections.defaultdict(list)
 for u in sorted(urls):buckets[key(u)].append(u)
 result=[]
 while buckets:
  for k in sorted(list(buckets)):
   result.append(buckets[k].pop(0))
   if not buckets[k]:del buckets[k]
 return result

def metric(item):
 genre,u,declared,lastmod=item
 try:
  r=requests.get(u,headers=UA,timeout=30);r.raise_for_status();p=Page();p.feed(r.text)
  blocks=p.blocks; title=next((s for t,s in blocks if t=='h1'),'')
  prose=[s for t,s in blocks if t=='p']; lists=[s for t,s in blocks if t=='li']; codes=[s for t,s in blocks if t=='pre'];heads=[(t,s) for t,s in blocks if re.fullmatch(r'h[2-6]',t)]
  paragraphs=[len(words(s)) for s in prose];sent=[len(words(q)) for s in prose for q in sentences(s)];pw=sum(paragraphs);lw=sum(len(words(s)) for s in lists);cw=sum(len(words(s)) for s in codes)
  sections=[]; current={'heading_level':None,'words':0}
  for t,s in blocks:
   if t in ('h2','h3','h4','h5','h6'):
    if current['words'] or current['heading_level']:sections.append(current)
    current={'heading_level':int(t[1]),'words':0}
   elif t in ('p','li'):current['words']+=len(words(s))
  if current['words'] or current['heading_level']:sections.append(current)
  mdn='developer.mozilla.org' in u
  accepted=bool(title and p.found and pw>=80 and cw <= 3*(pw+lw) and len(blocks)>=5 and p.canonical.rstrip('/')==r.url.rstrip('/'))
  reason='accepted mechanically; genre screening pending' if accepted else 'failed title/body/prose/canonical/code-volume filter'
  return {'genre':genre,'original_type':declared,'classification_confidence':'provisional path-based; task/lookup purpose requires human review', 'canonical_url':p.canonical,'requested_url':u,'final_url':r.url,'title':title,'project':'MDN Web Docs' if mdn else 'Django Software Foundation','author':'MDN contributors' if mdn else 'Django documentation contributors','date_last_modified':p.date or lastmod,'date_basis':'page time' if p.date else ('sitemap lastmod' if lastmod else 'not stated in extracted metadata'),'version':'live' if mdn else '6.1', 'license':'CC BY-SA 2.5' if mdn else 'BSD-3-Clause documentation license', 'license_url':'https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license' if mdn else 'https://github.com/django/django/blob/main/LICENSE', 'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(r.content).hexdigest(),'body_scope':'HTML main; p, li, pre, table, figure, h1-h6; suppress navigation, scripts, style, aside and footer; capture outer block once','accepted':accepted,'filter_result':reason,'metrics':{'prose_words':pw,'list_words':lw,'code_words':cw,'paragraph_word_distribution':stats(paragraphs),'sentence_word_distribution':stats(sent),'word_character_distribution':stats([len(w) for s in prose for w in words(s)]),'heading_count':len(heads),'heading_depth_counts':dict(collections.Counter(t for t,s in heads)),'section_prose_list_word_distribution':stats([x['words'] for x in sections]),'section_word_counts':sections,'paragraph_count':len(prose),'list_item_count':len(lists),'code_block_count':len(codes),'table_count':sum(t=='table' for t,s in blocks),'figure_count':sum(t=='figure' for t,s in blocks),'example_heading_count':sum(bool(re.search(r'\bexamples?\b',s,re.I)) for t,s in heads)}}
 except Exception as e:return {'genre':genre,'requested_url':u,'original_type':declared,'accepted':False,'error':str(e)}
def main():
 md=sitemap('https://developer.mozilla.org/sitemaps/en-us/sitemap.xml.gz');dj=sitemap('https://docs.djangoproject.com/sitemap-en.xml'); items=[]
 for genre in ['procedure','reference']:
  candidates=[]
  for u,d in dj:
   if not u or '/en/6.1/' not in u:continue
   if genre=='procedure' and '/howto/' in u and not u.endswith('/howto/'):candidates.append((u,'Django how-to',d))
   if genre=='reference' and '/ref/' in u and not u.endswith('/ref/'):candidates.append((u,'Django reference',d))
  for u,d in md:
   if not u:continue
   if genre=='procedure' and ('/How_to/' in u or ('/Guides/' in u and re.search(r'/(?:Using|Creating|Building|Setting|Configuring|Implementing|Adding|How_to|Working_with|Managing|Writing|Making|Applying|Installing|Deploying|Testing|Getting_started)',u,re.I))):candidates.append((u,'MDN how-to' if '/How_to/' in u else 'MDN guide with task-oriented title',d))
   if genre=='reference' and '/Reference/' in u and len(u.split('/'))>=10:candidates.append((u,'MDN reference',d))
  key=lambda x: urllib.parse.urlparse(x[0]).netloc+'/'+('/'.join(urllib.parse.urlparse(x[0]).path.split('/')[3:6]))
  ranked=interleave(candidates,key)
  print(genre,'candidates',len(ranked),flush=True)
  for u,typ,d in ranked:items.append((genre,u,typ,d))
  (OUT/(genre+'-candidates.json')).write_text(json.dumps([{'url':u,'original_type':t,'sitemap_lastmod':d} for u,t,d in ranked],indent=2)+'\n')
  # Extra records allow for mechanical rejection. Limits are candidate budgets, not claims of suitability.
  items=items[:]
  if genre=='procedure': proc=items[:700];items=[]
  else: ref=items[:600]
 for genre,selection in [('procedure',proc),('reference',ref)]:
  records=[];accepted=0
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
   for record in ex.map(metric,selection):
    records.append(record);accepted+=bool(record.get('accepted'))
    if len(records)%50==0:print(genre,'attempted',len(records),'mechanically eligible',accepted,flush=True)
    if accepted>=200:break
  with (OUT/(genre+'-records.jsonl')).open('w') as f:
   for r in records:f.write(json.dumps(r,ensure_ascii=False)+'\n')
  print(genre,'finished',len(records),accepted,flush=True)
if __name__=='__main__':main()
