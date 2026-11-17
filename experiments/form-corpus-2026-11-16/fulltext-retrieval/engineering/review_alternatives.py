#!/usr/bin/env python3
"""Revisit distinct OA copies and substantive HTML; never bypass restrictions."""
import hashlib,html.parser,json,re
from pathlib import Path
import retrieve as m
P=m.ROOT;CACHE=m.CACHE;state=json.loads((P/'run-state.json').read_text());m.blocked.update(state['blocked_hosts'])
rows=[json.loads(x) for x in m.SRC.read_text().splitlines()];prev={r['id']:r for r in map(json.loads,(P/'checkpoint.jsonl').read_text().splitlines())};meta={}
for f in (CACHE/'metadata').glob('*.json'):
 for x in json.loads(f.read_text())['payload']['results']:meta[x['id']]=x
class Article(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.depth=0;self.capture=None;self.buf=[];self.paras=[];self.heads=[]
 def handle_starttag(self,t,a):
  if t=='article':self.depth+=1
  if self.depth and self.capture is None and (t=='p' or t in ('h1','h2','h3')):self.capture=t;self.buf=[]
 def handle_endtag(self,t):
  if self.capture==t:
   s=' '.join(''.join(self.buf).split());(self.paras if t=='p' else self.heads).append(s);self.capture=None
  if t=='article' and self.depth:self.depth-=1
 def handle_data(self,d):
  if self.capture:self.buf.append(d)
results=[]
for row in rows:
 rid=row['openalex_id'].rsplit('/',1)[-1];original=prev[rid];data=meta.get(row['openalex_id']) or {};locs=[l for l in data.get('locations',[]) if l.get('is_oa')]
 if original.get('result')=='pdf_retrieved' and original.get('source_identity',{}).get('status')!='consistent' and len(locs)>1:
  r=m.assess(row,data);r['review_reason']='multiple advertised OA locations after unresolved PDF';results.append(r)
 urls=[(a.get('url'),a.get('version'),a.get('license')) for a in original['attempts'] if a.get('outcome','').startswith('HTML')]
 for url,version,license in urls:
  b,trace,error=m.fetch(url);obj={'id':rid,'review_reason':'OA HTML landing page inspected for full article body','url':url,'trace':trace,'error':error,'result':'not_fulltext'}
  if b:
   text=b.decode('utf-8','replace');parser=Article()
   try:parser.feed(text)
   except Exception:pass
   joined=' '.join(parser.paras);heading=' '.join(parser.heads);doi=row['doi_url'].removeprefix('https://doi.org/').lower();title_ok=m.skill.normalize_title(row['title']) in m.skill.normalize_title(heading);doi_ok=doi in text.lower();body_words=len(re.findall(r'\b\w+\b',joined));section_count=sum(bool(re.search(r'\b(?:introduction|methods?|results?|discussion|conclusions?)\b',h,re.I)) for h in parser.heads)
   obj.update({'article_paragraphs':len(parser.paras),'article_words':body_words,'article_section_signals':section_count,'title_heading_match':title_ok,'doi_in_html':doi_ok})
   paywall=re.search(r'\b(?:purchase this article|subscribe to (?:read|access)|access through your institution)\b',text,re.I)
   if title_ok and doi_ok and body_words>=1000 and len(parser.paras)>=8 and section_count>=2 and not paywall:
    (CACHE/'html').mkdir(exist_ok=True);sha=hashlib.sha256(b).hexdigest();file=CACHE/'html'/f'{rid}-{sha[:12]}.html';file.write_bytes(b);obj.update({'result':'html_retrieved','file':str(file),'bytes':len(b),'file_sha256':sha,'version':version,'license':license,'source_identity':{'status':'html_title_and_doi_consistent','reason':'article heading and page markup match; body heuristics only'}})
  results.append(obj)
 with (P/'alternative-checkpoint.jsonl').open('w') as f:
  for x in results:f.write(json.dumps(x,ensure_ascii=False)+'\n')
print('alternative and HTML assessments',len(results))
