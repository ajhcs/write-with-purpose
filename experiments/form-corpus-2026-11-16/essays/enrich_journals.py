#!/usr/bin/env python3
"""Fill journal titles from already hashed, locally cached JATS, without network."""
import hashlib,json,xml.etree.ElementTree as E
from pathlib import Path
D=Path(__file__).resolve().parent
CACHE=Path('/workspace/repos/builderbob/.essay-corpus-cache/2026-11-16')
p=D/'measurements.jsonl'; records=[json.loads(x) for x in p.read_text().splitlines()]
for x in records:
 f=CACHE/(x['pmcid']+'.xml')
 if not f.exists():continue
 try:
  raw=f.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=x.get('sha256'):continue
  root=E.fromstring(raw); j=root.find('./front/journal-meta/journal-title-group/journal-title')
  if j is not None:x['journalTitle']=' '.join(' '.join(j.itertext()).split())
 except E.ParseError:pass
p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records))
