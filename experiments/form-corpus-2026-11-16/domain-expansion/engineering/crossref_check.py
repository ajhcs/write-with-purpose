#!/usr/bin/env python3
"""A deliberately rate-limited optional metadata spot check; stops on 429."""
import json,time,urllib.parse
from pathlib import Path
import requests
P=Path(__file__).resolve().parent
rows=[json.loads(s) for s in (P/'records.jsonl').read_text().splitlines()]
# Output only to terminal. Do not silently rewrite the preserved 2026-11-16 snapshot.
for row in rows:
 if row.get('crossref_checked_utc'):continue
 url='https://api.crossref.org/works/'+urllib.parse.quote(row['doi_url'].removeprefix('https://doi.org/'),safe='')
 try:r=requests.get(url,timeout=20,headers={'User-Agent':'EngineeringBibliographyResearch/1.0'})
 except requests.RequestException as e:print('Request failed:',str(e));break
 if r.status_code==429:print('Rate limited; stopped without retries.');break
 if r.status_code!=200:print(r.status_code,url);break
 msg=r.json()['message'];print(row['doi_url'],msg.get('issued'),msg.get('published-print'),msg.get('published-online'))
 time.sleep(2)
