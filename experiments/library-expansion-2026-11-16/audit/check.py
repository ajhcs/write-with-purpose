import json, pathlib, urllib.request, urllib.error, difflib, re, datetime, argparse
parser=argparse.ArgumentParser(description='Reconcile shortlist structure offline; optional bounded live checks.')
parser.add_argument('--live',action='store_true',help='Run a bounded sequential sample of live metadata checks.')
parser.add_argument('--limit',type=int,default=12,help='Maximum sampled live requests; default 12.')
args=parser.parse_args()
if args.limit<0:parser.error('--limit must be nonnegative')
p=pathlib.Path(__file__).resolve().parent.parent
fields=['law','medicine','personal','physical-sciences','business','engineering']
contract=json.loads((p/'selection-contract.json').read_text()); expected={x['id'] for x in contract['forms']}; out={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fields':{},'live':[]}
rows=[]
for f in fields:
 try:
  r=json.loads((p/f/'candidates.json').read_text()); c=json.loads((p/f/'coverage.json').read_text())
 except Exception as e: out['fields'][f]={'error':str(e)}; continue
 ids={x['id']:x for x in r}; issues=[]
 if len(ids)!=len(r): issues.append('duplicate candidate ids')
 if {x['form_id'] for x in c}!=expected or len(c)!=17: issues.append('coverage form IDs incomplete or duplicated')
 refs=[]
 for x in c:
  cr=x.get('candidate_ids',[]); refs+=cr
  if x['provided']!=len(cr): issues.append(f"{x['form_id']}: provided mismatch")
  if len(cr)!=len(set(cr)): issues.append(f"{x['form_id']}: duplicate references")
  for i in cr:
   if i not in ids: issues.append(f'{i}: missing row')
   elif ids[i]['form_id']!=x['form_id']: issues.append(f'{i}: form mismatch')
  if x['status']=='three_targets' and len(cr)!=3: issues.append(f"{x['form_id']}: three_targets count mismatch")
 if set(ids)-set(refs): issues.append('unreferenced rows: '+str(sorted(set(ids)-set(refs))))
 out['fields'][f]={'candidate_count':len(r),'coverage_count':len(c),'structural_issues':issues}; rows += [(f,x) for x in r]
def norm(t): return re.sub(r'[^a-z0-9]+','',t.lower())
def fetch(fr):
 f,x=fr; doi=x.get('doi'); url=('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='/') if doi else x.get('stable_url'))
 if not url: return {'field':f,'id':x['id'],'error':'no locator'}
 # Avoid fetching PDFs, even when URL has no suffix.
 ispdf=('.pdf' in url.lower() or 'get_pdf' in url.lower())
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'MetadataAudit/1.0 (scholarly metadata checking)'},method='HEAD' if not doi else 'GET')
  with urllib.request.urlopen(req,timeout=18) as v:
   result={'field':f,'id':x['id'],'url':url,'status':v.status,'final_url':v.url,'method':'HEAD' if not doi else 'GET'}
   if doi:
    data=json.load(v)['message']; titles=data.get('title',[]); t=titles[0] if titles else ''; result.update({'crossref_title':t,'crossref_type':data.get('type'),'crossref_year':str((data.get('published',{}).get('date-parts') or [[None]])[0][0]),'title_similarity':round(difflib.SequenceMatcher(None,norm(x['title']),norm(t)).ratio(),3)})
   return result
 except Exception as e: return {'field':f,'id':x['id'],'url':url,'error':str(e)}
if args.live:
 selected=[]
 for field in fields:
  candidates=[row for row in rows if row[0]==field]
  risky=[row for row in candidates if row[1]['form_id'] in ('critical_review_of_work','study_review_protocol')]
  selected.extend((risky or candidates)[:2])
 crossref_blocked=False
 for row in selected[:args.limit]:
  if row[1].get('doi') and crossref_blocked:
   out['live'].append({'field':row[0],'id':row[1]['id'],'skipped':'Crossref stopped after prior rate/access response'})
   continue
  result=fetch(row);out['live'].append(result)
  if row[1].get('doi') and any(code in result.get('error','') for code in ('429','403')):crossref_blocked=True
 out['live_scope']='Bounded sequential sample; not all references independently verified.'
 output=p/'audit'/'targeted-live-checks.json'
else:
 out['live_scope']='No network requests; earlier live attempt remains in checks.json.'
 output=p/'audit'/'structural-checks.json'
output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['fields'],indent=2)); print('LIVE failures',sum('error' in x for x in out['live']));
for x in out['live']:
 if x.get('title_similarity',1)<.8 or x.get('crossref_type') in ('book','book-review','journal-issue','journal-volume','posted-content') or ('error' in x and x['field'] in ['law','medicine','personal','physical-sciences']): print(x)
