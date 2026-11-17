import json,pathlib,hashlib,math,collections
R=pathlib.Path('/workspace/repos/builderbob/write-with-purpose'); D=R/'experiments/rule-calibration-2026-11-16/sampling'; C=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/rule-calibration')
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
manifest=json.load(open(D/'source-manifest.partial.json'))
html={x['id']:x for x in map(json.loads,open(R/'experiments/corpus-analysis-2026-11-16/analysis/html-records.jsonl'))}
xml={x['pmcid']:x for x in map(json.loads,open(R/'experiments/corpus-analysis-2026-11-16/analysis/xml-records.jsonl'))}
for item in manifest:
 rec=html.get(item['id'],xml.get(item['id'],{}))
 item['publication_date']=rec.get('date') or str(rec.get('first_publication_year','unknown'))
 item['publication_date_basis']='existing source inventory; provisional'
 item['url']=rec.get('url') or 'https://pmc.ncbi.nlm.nih.gov/articles/'+item['id']+'/'
 item['outlet']=rec.get('journal') or item['url'].split('/')[2]
for id,stage in [('git','A'),('python','A'),('curl','B')]:
 x=json.load(open(C/'software'/f'{id}.json')); y={'id':id,'stage':stage,'stratum':'explanation/procedure','provisional_form':'explanation/procedure','sampling_date':'2026-11-16','title':x['title'],'authors':[x['project_or_author']],'source_path':x['source_path'],'source_sha256':x['source_sha256'],'body_path':x['body_path'],'body_sha256':x['body_sha256'],'paragraph_count':x['paragraph_count'],'selected_paragraph_ids':x['selected_paragraph_ids'],'selected_zero_based_positions':x['selected_zero_based_positions'],'private_metadata_path':str(C/'software'/f'{id}.json'),'publication_date':str(x['revision_year']),'publication_date_basis':x['revision_date_basis'], 'url':x['source_url'],'outlet':x['project_or_author'],'version':x['version'],'revision':x['revision']};manifest.append(y)
for x in manifest:
 x.setdefault('private_metadata_path',str(C/(x['id']+'.json')))
 assert sha(x['source_path'])==x['source_sha256'] and sha(x['body_path'])==x['body_sha256']
 n=x['paragraph_count'];assert x['selected_zero_based_positions']==[math.floor((i+.5)*n/3) for i in range(3)]
 y=json.load(open(x['private_metadata_path']));body=pathlib.Path(x['body_path']).read_text();p=y['paragraphs'];assert len(p)==n
 for z in p:
  val=body[z['start']:z['end']]; assert hashlib.sha256(val.encode()).hexdigest()==z.get('text_sha256',z.get('sha256'))
 assert x['selected_paragraph_ids']==[p[i]['id'] for i in x['selected_zero_based_positions']]
counts=collections.Counter((x['stage'],x['stratum']) for x in manifest); assert len(manifest)==12 and all(counts['A',s]==2 and counts['B',s]==1 for s in {x['stratum'] for x in manifest})
old=json.load(open(R/'experiments/pattern-test-2026-11-16/results/documents.json'));attachments=json.load(open(R/'experiments/corpus-analysis-2026-11-16/inputs/attachments-manifest.json'))
exclude={'prior_fully_coded':[{'id':x['id'],'title':x['title'],'source_sha256':x.get('source_sha256')} for x in old], 'uploaded_works':[{'filename':x['filename'],'source_sha256':x['sha256']} for x in attachments], 'other_prior_exposures':['all three prior development examples (as specified in task)','PMC1904193','PMC10954893','PMC10008412','PMC10011205','PG4 form manual','How to Lose Time and Money','How to Do Great Work','LF-f2db6fcab11c','BAE-13fadc84b9cf','official Heller brief','queue-explainer synthetic fixture'], 'candidate_rejections':[{'id':'LF-cf40fb0405a0','reason':'Retained capture terminates within narrative; complete article body not established.'},{'id':'rust-book-page','reason':'Raw source contained unresolved include directives; render-independent body not established.'}, {'id':'Git 2.46.0','source_sha256':'1e1b47f0a378242147e928d533dd384bcb3eab8227db2e027e2fa5538d976861','reason':'2024 version replaced to favor historical corpus.'}, {'id':'Python 3.12.5','source_sha256':'b391a3d94b7dd61785cb7749ba36837735404693eed3172248f5be2101eda16b','reason':'2024 version replaced to favor historical corpus.'}, {'id':'curl e26a4814462d92c9e8c93b9270add3f577a111b1','source_sha256':'cf563362f8579fdf992b3039651b878df798b11d422372e6253eeefa4e22e503','reason':'Contemporary revision replaced to favor historical corpus.'}], 'checks':'No selected title or source hash matches prior fully coded or attachment metadata; exact IDs and explicit teaching/source exclusions also checked. Cross-format exclusions include work titles, not merely raw-byte hashes.'}
assert not set(x['source_sha256'] for x in manifest)&set(x.get('source_sha256') for x in old)
assert not set(x['source_sha256'] for x in manifest)&set(x['sha256'] for x in attachments)
assert not {x['title'].casefold() for x in manifest}&{x['title'].casefold() for x in old}
(D/'source-manifest.json').write_text(json.dumps({'sampling_date':'2026-11-16','method':'Select paragraph zero-based indices floor((i+0.5)*n/3), i=0,1,2; source suitability and whole body boundaries decided before selecting.','sources':manifest},indent=2,ensure_ascii=False)+'\n')
(D/'candidate-exclusions.json').write_text(json.dumps(exclude,indent=2,ensure_ascii=False)+'\n')
print('validated',len(manifest),'documents',sum(len(x['selected_paragraph_ids']) for x in manifest),'paragraphs',dict(counts))
