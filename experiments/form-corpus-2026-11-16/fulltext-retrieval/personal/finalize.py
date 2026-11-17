#!/usr/bin/env python3
"""Join retrieval checkpoints, independent body checks and robots audit into an honest handoff."""
from pathlib import Path
import collections,csv,hashlib,json,urllib.parse
D=Path(__file__).resolve().parent; ROOT=D.parents[1]
def read(p):return [json.loads(s) for s in p.read_text().splitlines() if s]
src=read(ROOT/'domain-expansion/personal/records.jsonl');checks={x['id']:x for x in read(D/'manual-body-audit.jsonl')};attempts={x['id']:x for x in read(D/'checkpoint.jsonl')};
for follow in read(D/'followup-diaz.jsonl'):
 follow['prior_attempts']=[attempts[follow['id']]];attempts[follow['id']]=follow
audits={x['robots_url']:x for x in read(D/'robots-audit.jsonl') if x.get('robots_url')};rows=[]
for r in src:
 x=attempts.get(r['id'],{'id':r['id'],'status':'not_attempted','trace':[]}); m=checks.get(r['id']);p=[];auto=False
 for t in x.get('trace',[]):
  if t.get('action')!='robots':continue
  old=t['details'];url=old.get('robots_url');new=old if 'redirects' in old else audits.get(url,{})
  if old.get('final_url') and old.get('robots_url')!=old.get('final_url') and 'redirects' not in old:auto=True
  if not x.get('file'):continue
  if new.get('decision') not in ('check_rules','allowed_no_robots'):p.append('recheck_'+str(new.get('decision','missing')))
  elif old.get('sha256')!=new.get('sha256'):p.append('robots_changed_since_capture')
 if x.get('file') and not x.get('trace'):p.append('previous_cache_capture_rules_not_retained')
 if m and x.get('sha256')!=m['sha256']:raise ValueError('Manual body audit source hash mismatch '+r['id'])
 wrong=bool(m and m['assessment'] in ('no_article_body_found','wrong_destination'))
 cls=x.get('classification','');candidate=bool(x.get('file') and cls in ('html_body_extracted_unverified_completeness','pdf_retrieved_unverified_completeness') and not wrong)
 identity=x.get('source_identity',{}).get('status','unresolved')
 human=bool(m and m['assessment'] in ('publisher_pdf_title_author_consistent','publisher_html_title_author_consistent'))
 path=x.get('file');valid=bool(path and Path(path).is_file() and hashlib.sha256(Path(path).read_bytes()).hexdigest()==x.get('sha256'))
 if path and not valid:raise ValueError('Captured file failed SHA check '+r['id'])
 reason=('Inspect body boundaries, completeness, edition, form and access policy' if candidate else (m['assessment'] if wrong else x['status']))
 rows.append({**r,'retrieval':x,'manual_body_audit':m,'candidate_article_body_not_confirmed':candidate,'title_author_agreement':'manual_title_author_consistent' if human else identity,'robots_policy_audit':'unresolved: '+', '.join(sorted(set(p))) if p else ('rechecked_unchanged_and_no_ai_input_no_signal' if x.get('file') else 'not_applicable_no_file'),'prior_automatic_robots_redirect':auto,'sha256_verified_on_disk':valid,'manual_next_step':reason})
assert len(rows)==316 and len({x['id'] for x in rows})==316
(D/'manifest.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
with (D/'manual_needed.csv').open('w',newline='') as f:
 fields=['id','title','author','year_display','source_target_url','final_url','status','candidate_article_body_not_confirmed','title_author_agreement','robots_policy_audit','local_file','sha256','manual_next_step']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for x in rows:
  z=x['retrieval'];w.writerow({'id':x['id'],'title':x['title'],'author':x['author'],'year_display':x['year_display'],'source_target_url':x.get('target_url'),'final_url':z.get('final_url'),'status':z['status'],'candidate_article_body_not_confirmed':x['candidate_article_body_not_confirmed'],'title_author_agreement':x['title_author_agreement'],'robots_policy_audit':x['robots_policy_audit'],'local_file':z.get('file'),'sha256':z.get('sha256'),'manual_next_step':x['manual_next_step']})
counts=collections.Counter(x['retrieval']['status'] for x in rows); c=[x for x in rows if x['candidate_article_body_not_confirmed']];p=collections.Counter(x['robots_policy_audit'] for x in c)
summary={'records':len(rows),'statuses':dict(counts),'records_with_saved_file':sum(x['sha256_verified_on_disk'] for x in rows),'candidate_article_bodies_not_confirmed':len(c),'candidate_title_author_consistent':sum(x['title_author_agreement'] in ('title_author_consistent','manual_title_author_consistent') for x in c),'candidate_robots_policy':dict(p),'manual_false_positives_removed':sum(bool(x['manual_body_audit'] and x['manual_body_audit']['assessment'] in ('no_article_body_found','wrong_destination')) for x in rows),'prior_automatic_robots_redirect_records':sum(x['prior_automatic_robots_redirect'] for x in rows),'manual_review_needed':len(rows),'source_file_sha256':hashlib.sha256((ROOT/'domain-expansion/personal/records.jsonl').read_bytes()).hexdigest()}
(D/'counts.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
