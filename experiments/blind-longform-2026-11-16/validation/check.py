import hashlib,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from extract import P,walk,plain,base
root=Path(__file__).resolve().parent.parent; src=root/'sources'; data=json.loads((src/'documents.json').read_text());checks=[]
def check(name,condition):
 checks.append({'check':name,'pass':bool(condition)})
 if not condition:print('FAIL',name)
manifest=json.loads((base/'fetch-manifest.json').read_text())
for m in manifest:check('cached '+m['id']+' hash',hashlib.sha256((base/(m['id']+'.html')).read_bytes()).hexdigest()==m['sha256'])
for d in data['documents']:
 t=(src/d['source_file']).read_text();check(d['id']+' sha256',hashlib.sha256(t.encode()).hexdigest()==d['source_sha256']);p=d['passages']
 check(d['id']+' three unique spans',len(p)==3 and len({x['text'] for x in p})==3 and all(0<=x['start']<x['end']<=len(t) and t[x['start']:x['end']]==x['text'] for x in p) and all(p[i]['end']<=p[i+1]['start'] for i in range(2)))
 check(d['id']+' context',all(t[max(0,x['start']-250):x['start']]==x['context_before'] and t[x['end']:x['end']+250]==x['context_after'] for x in p))
 check(d['id']+' navigation patterns absent',not any(x in t for x in ['Skip to content','Previous topic','Next topic','Hey look at this','Read full Note','¶','Primary navigation']))
python=P((base/'python.html').read_text());body=next(n for n in walk(python.root) if n.a.get('class')=='body'); originals=[plain(n).rstrip('\n') for n in walk(body) if n.t=='pre']; actual=re.findall(r'```\n(.*?)\n```',(src/'S04.md').read_text(),re.S)
check('all Python preformatted examples exact and ordered',actual==originals and actual==data['documents'][3]['exact_code_blocks'])
check('Python licence cached copy byte identical',(src/'python-license.html').read_bytes()==(base/'python-license.html').read_bytes())
doc=P((base/'doctorow.html').read_text());content=next(n for n in walk(doc.root) if n.a.get('class')=='entry-content');rights=plain(content)
check('Doctorow source includes CC BY 4.0 rights statement', 'Creative Commons Attribution 4.0 license' in rights and 'Quotations and images are not included in this license' in rights)
check('all Cole article note sections present',all('## Notes' in (src/f'S0{i}.md').read_text() for i in (1,2)))
report={'checks':checks,'passed':sum(c['pass'] for c in checks),'total':len(checks),'rights_evidence':{'doctorow':'Cached original post colophon states Creative Commons Attribution 4.0 and excludes quotations and images; https://pluralistic.net/2023/01/21/potemkin-ai/ ; https://creativecommons.org/licenses/by/4.0/','python':'Cached Python license retained as sources/python-license.html; https://docs.python.org/3.8/license.html','cole':'User authorized use in this trial.'},'limitations':['Extraction is presentation conversion, not editorial rewriting: omitted article title, byline, dates, navigation, visual inserts and duplicated interactive note panels; kept narrative, notes, external links, and code.','Doctorow source retains a third-party quotation as part of the source; the post expressly excludes quotations and images from its CC license.','Paragraph selection uses exact Unicode offsets in the extracted Markdown; several windows are shorter than 120 words because of paragraph and section boundaries.','Checks establish extraction and index consistency, not semantic gold, independent rights clearance for third-party quotations, or writing quality.']}
(root/'validation/source-extraction.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(root/'validation/source-extraction.md').write_text('# Source extraction validation\n\n'+f"{report['passed']}/{report['total']} checks passed.\n\n"+'\n'.join('- '+c['check']+': '+('PASS' if c['pass'] else 'FAIL') for c in checks)+'\n\n## Scope and limitations\n\n'+'\n'.join('- '+x for x in report['limitations'])+'\n\n## Rights provenance\n\n'+'\n'.join('- '+k+': '+v for k,v in report['rights_evidence'].items())+'\n')
print(report['passed'], '/',report['total']);sys.exit(0 if all(c['pass'] for c in checks) else 1)
