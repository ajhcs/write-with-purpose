#!/usr/bin/env python3
"""Audit the final manifest and generate a human-readable retrieval report."""
import collections,csv,hashlib,json,pathlib,datetime
P=pathlib.Path(__file__).resolve().parent
CACHE=pathlib.Path('/workspace/repos/builderbob/.writing-corpus-cache/fulltext/business')
rows=[json.loads(x) for x in (P/'retrieval_manifest.jsonl').read_text().splitlines() if x]
statuses=collections.Counter(x['status'] for x in rows)
files=[x for x in rows if x.get('file')]
ids=collections.Counter(x.get('source_identity',{}).get('status','unavailable') for x in files)
network=sum(any('http_status' in t for t in x.get('attempted_urls',[])) for x in rows)
deferred=sum(any(t.get('status')=='deferred_closed_record_canonical_host_blocked' for t in x.get('attempted_urls',[])) for x in rows)
miss=[];mismatch=[];referenced=set()
for r in rows:
 for f in ([r] if r.get('file') else [])+r.get('alternates',[]):
  if not f.get('file'):continue
  path=pathlib.Path(f['file']);referenced.add(str(path))
  if not path.is_file():miss.append(str(path));continue
  if hashlib.sha256(path.read_bytes()).hexdigest()!=f.get('sha256'):mismatch.append(str(path))
cache_files=[x for folder in ['pdf','html'] for x in (CACHE/folder).glob('*') if x.is_file() and not x.name.endswith('.part')]
orphans=[str(p) for p in cache_files if str(p) not in referenced]
with (P/'manual_needed.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['source_id','venue','title','doi','manual_action','status','identity_status','file','first_indexed_landing']);w.writeheader()
 for r in rows:
  identity=r.get('source_identity',{}).get('status','unavailable')
  action='retrieve through lawful library access' if not r.get('file') else 'inspect identity and completeness' if identity!='consistent' else 'inspect completeness and version'
  w.writerow({'source_id':r['source_id'],'venue':r['venue'],'title':r['title'],'doi':r['doi'],'manual_action':action,'status':r['status'],'identity_status':identity,'file':r.get('file'),'first_indexed_landing':next((t['url'] for t in r.get('attempted_urls',[]) if t.get('kind')=='indexed_landing'),'')})
counts={'records_in_manifest':len(rows),'metadata_found':sum(bool(x.get('metadata_found')) for x in rows),'records_with_http_response':network,'primary_status':dict(statuses),'files_with_primary_identity':dict(ids),'files_missing':len(miss),'files_hash_mismatch':len(mismatch),'files_unreferenced_in_cache':len(orphans),'closed_canonical_publisher_blocked_deferrals':deferred,'completeness_verified':sum(x.get('completeness')=='verified' for x in rows)}
(P/'counts.json').write_text(json.dumps({'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':counts,'missing_files':miss,'mismatched_files':mismatch,'unreferenced_cache_files':orphans},indent=2))
byvenue=collections.defaultdict(collections.Counter)
for r in rows:byvenue[r['venue']][r['status']]+=1
lines=['# Business full-text retrieval',f"\nRecords in this report: **{len(rows)}** of 1,200. OpenAlex metadata matched **{counts['metadata_found']}**; **{network}** records received at least one HTTP response from a checked document or landing URL. The remainder still have metadata and attempted/deferred URL traces. This is a retrieval attempt, not a count of works available to a licensed library.",f"\nPrimary retained results: **{statuses.get('pdf_retrieved',0)} PDFs** and **{statuses.get('html_body_retrieved',0)} substantial public HTML bodies**. Across retained results, **{ids.get('consistent',0)}** have matching source-identity evidence, **{ids.get('unresolved',0)}** are unresolved, **{ids.get('conflict',0)}** conflict, and **{ids.get('unavailable',0)}** lack usable identity evidence. Completeness was verified for **{counts['completeness_verified']}**: page count and an extracted title are not evidence of a complete publication.",f"\nAll retained files are outside Git under `{CACHE}`. The full per-record trace and alternate paths are in `retrieval_manifest.jsonl`; `manual_needed.csv` distinguishes library access, identity/completeness review, and completeness/version review. Hash audit: {len(miss)} missing files, {len(mismatch)} hash mismatches; {len(orphans)} other cache files not referenced by the current manifest are preserved and listed in `counts.json`.",f"\nThe first pass matched all location metadata and applied a 0.75-second per-host minimum. It did **not** enforce robots-declared longer crawl delays or request rates, and treated robots redirects conservatively as unavailable. The initial follow-up followed robots redirects automatically without separately pacing redirect hops, although it enforced crawl-delay and request-rate for document requests. The last follow-up corrected this by manually pacing robots redirect hops and paces document requests by the greater of 0.75 seconds, declared crawl-delay, and request-rate interval. These earlier limitations are retained rather than retroactively claiming compliance. Follow-up preserves 403, 429, and access-challenge host deferrals. For {deferred} closed records, it recorded a deferral instead of following a DOI to an already-blocked canonical publisher. Rate blocks and challenge detection may be over-conservative; a generic CAPTCHA marker can also appear in a normal page. HBR disallows automated `/search` in its robots file, so indexed public locations were used.","\nOpenAlex OA flags are leads, not proof of access; metadata batches are cached outside Git. Public landing pages count only when a substantial article element has at least three prose paragraphs and approximately 500 words, matching title evidence, and no detected explicit paywall markers. HTML DOI metadata is required for an identity-consistent HTML result. These checks can miss paywalls, truncated bodies, and article layouts; HTML is never claimed complete automatically. Only PDFs at least 10 KiB with a `%PDF-` header are retained. PDF identity uses the fulltext-retrieval skill's bounded first-page text, not a title appearing in the body or references. Unresolved or conflicting alternatives remain in the manifest and cache. No restricted content or site challenge was bypassed.","\nThe set is a citation-ranked business discovery queue, not a verified classification of writing forms; no rhetorical or genre claims have been made from downloads. Source titles, author strings, identifiers, versions, licenses, dates, URL traces, byte sizes and SHA-256 digests are recorded where known, not inferred when missing.","\n| Venue | Primary result status counts |","| --- | --- |"]
for k,v in byvenue.items():lines.append('| '+k+' | '+', '.join(f'{s}: {n}' for s,n in v.items())+' |')
(P/'report.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(counts,indent=2))
