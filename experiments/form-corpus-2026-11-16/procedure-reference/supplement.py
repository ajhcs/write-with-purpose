#!/usr/bin/env python3
"""Add independent project page measurements, keeping original records intact."""
import collections,concurrent.futures,datetime,hashlib,json,re
from pathlib import Path
import requests
import collect
P=Path(__file__).resolve().parent
class ExtendedPage(collect.Page):
 def handle_starttag(self,t,attrs):
  if t=='article' and dict(attrs).get('role')=='main':t='main'
  super().handle_starttag(t,attrs)
 def handle_endtag(self,t):
  if t=='article' and self.active:t='main'
  super().handle_endtag(t)
def run_one(item):
 genre,u,typ,lastmod=item
 try:
  r=requests.get(u,headers=collect.UA,timeout=30);r.raise_for_status();p=ExtendedPage()
  if 'docs.python.org/3.4/' in u:r.encoding='utf-8'
  html=r.text
  if 'docs.python.org/3.4/' in u:
   start=html.index('<div class="body">'); end=html.index('<div class="sphinxsidebar"',start); html=html[:start]+'<main>'+html[start:end]+'</main>'+html[end:]
  p.feed(html); blocks=p.blocks
  title=next((s for t,s in blocks if t=='h1'),'');prose=[s for t,s in blocks if t=='p']; lists=[s for t,s in blocks if t=='li'];codes=[s for t,s in blocks if t=='pre'];heads=[(t,s) for t,s in blocks if re.fullmatch(r'h[2-6]',t)]
  words=collect.words;stats=collect.stats
  paragraphs=[len(words(s)) for s in prose];sent=[len(words(q)) for s in prose for q in collect.sentences(s)];pw=sum(paragraphs);lw=sum(len(words(s)) for s in lists);cw=sum(len(words(s)) for s in codes)
  sections=[];current={'heading_level':None,'words':0}
  for t,s in blocks:
   if t in ('h2','h3','h4','h5','h6'):
    if current['words'] or current['heading_level']:sections.append(current)
    current={'heading_level':int(t[1]),'words':0}
   elif t in ('p','li'):current['words']+=len(words(s))
  if current['words'] or current['heading_level']:sections.append(current)
  is_lxd='canonical.com' in u
  canonical=p.canonical or r.url; is_python='docs.python.org/3.4/' in u; accepted=bool(title and p.found and pw>=80 and cw<=3*(pw+lw) and len(blocks)>=5 and (is_python or canonical.rstrip('/')==r.url.rstrip('/')))
  return {'genre':genre,'original_type':typ,'classification_confidence':'provisional path-based; task/lookup purpose requires human review','canonical_url':canonical,'canonical_basis':'link rel canonical' if p.canonical else 'final URL, no canonical link found','requested_url':u,'final_url':r.url,'title':title,'project':'Python' if is_python else ('Canonical LXD' if is_lxd else 'Kubernetes'),'author':'Python documentation contributors' if is_python else ('LXD contributors' if is_lxd else 'Kubernetes contributors'),'date_last_modified':p.date or lastmod,'date_basis':'page time' if p.date else ('sitemap lastmod' if lastmod else 'not stated in extracted metadata'),'version':'3.4.10 archived documentation' if is_python else ('latest' if is_lxd else 'live'),'license':'Python documentation license' if is_python else ('AGPL-3.0 (site footer)' if is_lxd else 'CC BY 4.0'),'license_url':'https://docs.python.org/3.4/license.html' if is_python else ('https://github.com/canonical/lxd/blob/main/COPYING' if is_lxd else 'https://github.com/kubernetes/website/blob/main/LICENSE'),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(r.content).hexdigest(),'body_scope':'HTML main, article role=main, or Python 3.4 body div before sidebar; p, li, pre, table, figure, h1-h6; suppress navigation, scripts, style, aside and footer; capture outer block once','accepted':accepted,'filter_result':'accepted mechanically; genre screening pending' if accepted else 'failed title/body/prose/canonical/code-volume filter','metrics':{'prose_words':pw,'list_words':lw,'code_words':cw,'paragraph_word_distribution':stats(paragraphs),'sentence_word_distribution':stats(sent),'word_character_distribution':stats([len(w) for s in prose for w in words(s)]),'heading_count':len(heads),'heading_depth_counts':dict(collections.Counter(t for t,s in heads)),'section_prose_list_word_distribution':stats([x['words'] for x in sections]),'section_word_counts':sections,'paragraph_count':len(prose),'list_item_count':len(lists),'code_block_count':len(codes),'table_count':sum(t=='table' for t,s in blocks),'figure_count':sum(t=='figure' for t,s in blocks),'example_heading_count':sum(bool(re.search(r'\bexamples?\b',s,re.I)) for t,s in heads)}}
 except Exception as e:return {'genre':genre,'requested_url':u,'original_type':typ,'accepted':False,'error':str(e)}
def main():
 lx=collect.sitemap('https://canonical.com/lxd/docs/latest/sitemap.xml'); ku=collect.sitemap('https://kubernetes.io/en/sitemap.xml')
 for genre in ['procedure','reference']:
  c=[]
  for u,d in lx:
   if not u:continue
   if genre=='procedure' and '/howto/' in u:c.append((genre,u,'Canonical LXD how-to',d))
   if genre=='reference' and '/reference/' in u and not re.search(r'/reference/(?:manpages|api|configuration|swagger)/',u):c.append((genre,u,'Canonical LXD reference',d))
  for u,d in ku:
   if not u:continue
   if genre=='procedure' and '/docs/tasks/' in u:c.append((genre,u,'Kubernetes task',d))
   if genre=='reference' and '/docs/reference/' in u and not re.search(r'/reference/(?:kubernetes-api|generated|command-line-tools-reference)/',u):c.append((genre,u,'Kubernetes reference',d))
  c=sorted(c,key=lambda x:(x[2],x[1])); l=[x for x in c if x[2].startswith('Canonical')];k=[x for x in c if x[2].startswith('Kubernetes')];balanced=[]
  while l or k:
   if l:balanced.append(l.pop(0))
   if k:balanced.append(k.pop(0))
  (P/(genre+'-supplement-candidates.json')).write_text(json.dumps([{'url':u,'original_type':t,'sitemap_lastmod':d} for _,u,t,d in balanced],indent=2)+'\n')
  limit=190 if genre=='procedure' else 80;rows=[];accepted=0
  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
   for x in ex.map(run_one,balanced[:limit]):
    rows.append(x);accepted+=bool(x.get('accepted'))
    if len(rows)%20==0:print(genre,len(rows),accepted,flush=True)
    if accepted>=(125 if genre=='procedure' else 30):break
  with (P/(genre+'-supplement-records.jsonl')).open('w') as f:
   for x in rows:f.write(json.dumps(x,ensure_ascii=False)+'\n')
  print(genre,'done',len(rows),accepted,flush=True)
if __name__=='__main__':main()
