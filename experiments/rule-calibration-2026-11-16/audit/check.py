import json,hashlib,math,pathlib,collections,datetime,xml.etree.ElementTree as ET,re
from html.parser import HTMLParser
R=pathlib.Path(__file__).resolve().parents[1]; repo=R.parents[1]; private=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/rule-calibration'); load=lambda p:json.loads(pathlib.Path(p).read_text()); sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest(); out={}; problems=[]
manifest=load(R/'sampling/source-manifest.json'); sources=manifest['sources']; freeze=load(R/'protocol/freeze.json'); interface=load(R/'protocol/interface-freeze.json'); sample=load(R/'protocol/sample-freeze.json'); checks=[]
for rec in freeze['files']:checks.append((str(R/'protocol'/rec['file']),rec['sha256']))
for rec in interface['files']:checks.append((str(repo/rec['path']),rec['sha256']))
checks.append((str(R/'sampling/source-manifest.json'),sample['sampling_manifest_sha256']))
for stage in sample['packets']:
 for rec in stage['files']:checks.append((rec['path'],rec['sha256']))
for s in sources:checks.extend([(s['source_path'],s['source_sha256']),(s['body_path'],s['body_sha256'])])
checks.extend([(str(R/v['file']),v['sha256']) for v in load(R/'results/comparison.json')['validation']])
out['hashes']={'checked':len(checks),'mismatch':[p for p,h in checks if sha(p)!=h]}
ex=load(R/'sampling/candidate-exclusions.json'); old=ex['prior_fully_coded']; uploads=ex['uploaded_works']; oldhash={e['source_sha256'] for e in old+uploads};oldtitle={e['title'].casefold() for e in old}; match=[s['id'] for s in sources if s['source_sha256'] in oldhash or s['title'].casefold() in oldtitle or s['id'] in ex['other_prior_exposures']];out['sample']={'documents':len(sources),'targets':sum(len(s['selected_paragraph_ids']) for s in sources),'strata':dict(collections.Counter(s['stage']+' '+s['stratum'] for s in sources)),'excluded_matches':match,'index_errors':[],'binding_errors':[]}
for s in sources:
 m=load(s['private_metadata_path']); body=pathlib.Path(s['body_path']).read_text(); p=m['paragraphs']; n=len(p); idx=[math.floor((i+.5)*n/3) for i in range(3)]
 if n!=s['paragraph_count'] or idx!=s['selected_zero_based_positions'] or [p[i]['id'] for i in idx]!=s['selected_paragraph_ids']:out['sample']['index_errors'].append(s['id'])
 for q in p:
  if hashlib.sha256(body[q['start']:q['end']].encode()).hexdigest()!=q.get('sha256',q.get('text_sha256')):out['sample']['binding_errors'].append(q['id'])
 for st in [s['stage']]:
  packet=load(private/'packets'/st/'manifest.json'); units={u['unit_id']:u for u in packet['units']}; t=[t['paragraph_id'] for t in packet['targets'] if t['source_id']==s['id']]
  if t!=s['selected_paragraph_ids'] or any(units[q['id']]['text']!=body[q['start']:q['end']] for q in p):out['sample']['binding_errors'].append(s['id'])
# Independent primary set counts from selected raw roles, no normalize import.
comparison=load(R/'results/comparison.json'); raws={}; counts={}
for v in comparison['validation']:
 if v['selected']: raws[v['coder_id']]=load(R/v['file'])
for stage in ('A','B'):
 m=load(private/'packets'/stage/'manifest.json')
 for arm in ('original','revised'):
  aa=[{a['paragraph_id']:a for a in raws[f'{stage}-{arm}-{i}']['annotations']} for i in (1,2)]
  for field in ('clear_labels','candidate_union'):
   c=collections.Counter();jac=[]
   for t in m['targets']:
    sets=[]
    for coder in aa:
     roles=coder[t['paragraph_id']]['roles'];sets.append({r['function_id'] for r in roles if (r['decision']=='present' and r['status']=='clear') or (field=='candidate_union' and r['decision']=='unresolved')})
    a,b=sets;c['n']+=1;c['exact']+=a==b;c['strict_subset']+=(a<b or b<a);c['two_sided']+=bool(a-b) and bool(b-a);c['both_empty']+=not(a|b);jac.append(len(a&b)/len(a|b) if a|b else 1)
   result={k:c[k] for k in ('n','exact','strict_subset','two_sided','both_empty')};result['exact_rate']=c['exact']/c['n'];result['mean_jaccard']=sum(jac)/len(jac); counts[f'{stage}-{arm}-{field}']=result
   for k,v in result.items():
    if abs(v-comparison['by_stage'][stage][arm][field][k])>1e-12:problems.append((stage,arm,field,k,v))
out['independent_primary']=counts;out['primary_mismatches']=problems
# Target IoU computed as sets of Unicode code point positions from raw quotes.
iou_errors=[]
for item in comparison['target_proxy']:
 pid=item['paragraph_id'];stage=next(st for st in ('A','B') if any(t['paragraph_id']==pid for t in load(private/'packets'/st/'manifest.json')['targets']));m=load(private/'packets'/stage/'manifest.json');units={u['unit_id']:u['text'] for u in m['units']};sets=[];uids=[]
 for i in (1,2):
  ann=next(a for a in raws[f'{stage}-revised-{i}']['annotations'] if a['paragraph_id']==pid);points=set();ids=set()
  for role in ann['roles']:
   if role['function_id']!=item['function_id'] or role['decision']!='present':continue
   for target in role['targets']:
    for a in target['anchors']:
     txt=units[a['unit_id']];pos=-1
     for _ in range(a.get('occurrence',0)+1):pos=txt.find(a['quote'],pos+1)
     assert pos>=0;ids.add(a['unit_id']);points.update((a['unit_id'],j) for j in range(pos,pos+len(a['quote'])))
  sets.append(points);uids.append(ids)
 val=len(sets[0]&sets[1])/len(sets[0]|sets[1]) if sets[0]|sets[1] else None
 if item['exact_unit_set']!=(uids[0]==uids[1]) or (val is None)!=(item['character_span_iou'] is None) or (val is not None and abs(val-item['character_span_iou'])>1e-12):iou_errors.append((pid,item['function_id']))
out['target_iou']={'n':len(comparison['target_proxy']),'mismatches':iou_errors}
expected={'orient':'relation','support':'relation','illustrate':'relation','qualify':'relation','narrate':'temporal_presentation'}; mismatches=[];missing=[];mixed=[]
for cid,raw in raws.items():
 if '-revised-' not in cid:continue
 for a in raw['annotations']:
  for role in a['roles']:
   fid=role['function_id'];wanted=expected.get(fid,'local_move')
   if 'layer' not in role:missing.append((cid,a['paragraph_id'],fid))
   elif role['layer']!=wanted:mismatches.append((cid,a['paragraph_id'],fid,role['layer']))
  ds=collections.defaultdict(set)
  for role in a['roles']:ds[role['function_id']].add(role['decision'])
  mixed.extend((cid,a['paragraph_id'],fid) for fid,v in ds.items() if len(v)>1)
out['layer_checks']={'missing':missing,'wrong':mismatches,'mixed_decisions':mixed}
x=load(R/'coding/A-revised-2/raw.json');y=load(R/'coding/A-revised-2/raw-v2.json'); diff=[]
for a,b in zip(x['annotations'],y['annotations']):
 for k in a:
  if a[k]!=b[k]:
   if k=='context':diff.extend((a['paragraph_id'],k,z) for z in a[k] if a[k][z]!=b[k].get(z))
   else:diff.append((a['paragraph_id'],k))
out['repair_diff_keys']=dict(collections.Counter('/'.join(d[1:]) for d in diff));out['results_sha256']=sha(R/'results/comparison.json');(R/'audit/checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'hash_mismatch':out['hashes']['mismatch'],'sample':out['sample'],'primary_mismatches':problems,'target_iou':out['target_iou'],'layers':out['layer_checks'],'repair':out['repair_diff_keys']},indent=2))
