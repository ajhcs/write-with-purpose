import csv,json,hashlib,re,xml.etree.ElementTree as ET
from pathlib import Path
ids=['xml-02359','xml-02334','xml-02298','xml-02415','xml-02282','xml-02382','xml-02317','xml-02448']
rows={x['record_id']:x for x in csv.DictReader(open('experiments/corpus-analysis-2026-11-16/results/document-inventory.csv'))}
out=Path('/workspace/repos/builderbob/.writing-corpus-cache/pattern-test/systematic')
sha=lambda b:hashlib.sha256(b).hexdigest()
def tag(e):return e.tag.split('}')[-1]
def text(e):
 def rec(node):
  x=node.text or ''
  for c in node:
   if tag(c) not in {'list','table-wrap','fig','disp-formula','boxed-text','supplementary-material','fn-group','ref-list'}: x+=rec(c)
   x+=c.tail or ''
  return x
 return re.sub(r'\s+',' ',rec(e)).strip()
manifest=[]
for id in ids:
 r=rows[id]; raw=(out/f'{id}.xml').read_bytes(); assert sha(raw)==r['source_sha256']; root=ET.fromstring(raw); body=root.find('.//body'); blocks=[]; sections=[]; counts={}
 def walk(node,section=None,path='/article/body'):
  seen={}
  for c in node:
   ct=tag(c); seen[ct]=seen.get(ct,0)+1; childpath=f'{path}/{ct}[{seen[ct]}]' 
   t=tag(c); counts[t]=counts.get(t,0)+1
   if t=='sec':
    title=next((text(z) for z in c if tag(z)=='title'),None); 
    if (title or '').lower() in {'supplementary material','supplementary materials','supporting information','acknowledgments','acknowledgements','abbreviations','footnotes','references','associated data','notes','study group members','competing interests',"authors' contributions",'contributor information','role of the funding source'} or (c.get('id') or '').startswith(('ack','notes','fn-group','ref-list','_ad','_ci')): continue
    sid=c.get('id') or f'generated-{len(sections)+1}'; s={'id':sid,'heading':title,'parent':section}; sections.append(s); walk(c,sid,childpath)
   elif t=='p': blocks.append({'section_id':section,'text':text(c),'xml_path':childpath})
   elif t in {'list','table-wrap','fig','disp-formula','boxed-text','supplementary-material','fn-group','ref-list'}: pass
   elif t not in {'title','label'}: walk(c,section,childpath)
 walk(body)
 content=''; index=[]
 for n,b in enumerate(blocks,1):
  if not b['text']: continue
  start=len(content);content+=b['text'];end=len(content);content+='\n\n';index.append({'id':f'{id}-p{n:03d}','section_id':b['section_id'],'source_xml_path':b['xml_path'],'start':start,'end':end,'span_sha256':sha(b['text'].encode())})
 path=out/f'{id}.txt';path.write_text(content,encoding='utf8'); (out/f'{id}.index.json').write_text(json.dumps({'source_xml_sha256':sha(raw),'cache_sha256':sha(content.encode()),'sections':sections,'paragraphs':index,'encountered_element_counts':counts},indent=2))
 j=root.find('.//journal-title'); pubs=[]
 for x in root.findall('.//article-meta/pub-date'):pubs.append({'type':x.get('pub-type') or x.get('publication-format'),'year':x.findtext('year')})
 manifest.append({'id':id,'title':r['title'],'doi':r['doi'],'pmcid':r['pmcid'],'journal':''.join(j.itertext()) if j is not None else None,'earliest_reported_year':r['year'],'year_basis':r['year_basis'],'reported_years':r['reported_years'],'xml_publication_dates':pubs,'source_path':r['source_path'],'private_xml_copy':str(out/f'{id}.xml'),'date_disagreement':r['date_disagreement'],'source_sha256':sha(raw),'normalized_cache_path':str(path),'normalized_cache_sha256':sha(content.encode()),'paragraphs':len(index),'sections':sections,'encountered_element_counts':counts})
Path('experiments/pattern-test-2026-11-16/systematic/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
