#!/usr/bin/env python3
"""Persist limited title-screen decisions without changing extraction acceptance."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
REJECT={
 'procedure':{'CSS layout cookbook','Contribute a recipe','Cookbook template','Introduction to writing mode systems','How-to guides¶','Tasks','Accessing Clusters','Access Services Running on Clusters'},
 'reference':{'ARIA states and properties (attributes)','WebDriver BiDi modules','Axes','XSLT elements reference','Class-based generic views - flattened index¶','Deploying GeoDjango¶','Reference¶','Reference','Using ABAC Authorization','Authenticating Kubernetes','Authorization','Using Node Authorization','Mapping PodSecurityPolicies to Pod Security Standards','Using RBAC Authorization','Managing Service Accounts'},
}
for genre in ('procedure','reference'):
 for suffix in ('-records.jsonl','-supplement-records.jsonl'):
  path=P/(genre+suffix);rows=[json.loads(line) for line in path.read_text().splitlines()]
  for r in rows:
   if not r.get('accepted'):
    r['title_screen_status']='not_screened_mechanical_failure';r['included_in_analysis']=False;r['exclusion_reason']='Failed mechanical extraction or eligibility check; see filter_result or error.'
   elif r.get('title') in REJECT[genre]:
    r['title_screen_status']='excluded_by_title_screen';r['included_in_analysis']=False;r['exclusion_reason']='Limited title screen identified an apparent index, template, introduction, or mismatched reader purpose.'
   else:
    r['title_screen_status']='passed_limited_title_screen';r['included_in_analysis']=True;r['exclusion_reason']=None
  path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
path=P/'procedure-historical-records.jsonl';rows=[json.loads(line) for line in path.read_text().splitlines()]
for r in rows:
 r['title_screen_status']='not_screened_separate_historical_pilot';r['included_in_analysis']=False;r['exclusion_reason']='Separate historical pilot; excluded from main aggregate regardless of mechanical acceptance.'
path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
