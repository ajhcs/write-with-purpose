"""Resumable public full-text retrieval with source/identity receipts.

No credentials, paywall workarounds or fabricated contact email. Unpaywall is
used only if MEDSCI_CONTACT_EMAIL is already configured. Run with medsci-python.
Downloaded candidates and source identity are distinct results.
"""
import argparse
import concurrent.futures
import csv
import datetime
import hashlib
import html
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/library-retrieval-2026-11-16')
SKILL=Path('/home/builderbob/.agents/skills/fulltext-retrieval/fetch_oa.py')
spec=importlib.util.spec_from_file_location('fulltext_skill',SKILL)
skill=importlib.util.module_from_spec(spec);spec.loader.exec_module(skill)
CONTACT=os.getenv('MEDSCI_CONTACT_EMAIL','')
LOCK=threading.Lock(); HOST_LOCKS={}; HOST_LAST={}; BLOCKS={}; DISABLED=set()
UA='WritingCorpusRetrieval/1.0'+(' (mailto:'+CONTACT+')' if CONTACT else '')


def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(data):return hashlib.sha256(data).hexdigest()
def key(row):return hashlib.sha256((row.get('doi')or row['candidate_key']).encode()).hexdigest()[:16]
def norm(text):return skill.normalize_title(text)
def write_json(path,data):
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temp.replace(path)


def request(url,rec,purpose):
    url=html.unescape(url).replace(' ','%20')
    if not url.startswith(('https://','http://')):return None,None,None
    host=urllib.parse.urlparse(url).netloc.lower()
    with LOCK:lock=HOST_LOCKS.setdefault(host,threading.Lock())
    with lock:
        if host in DISABLED:
            rec['attempts'].append({'url':url,'purpose':purpose,'outcome':'host_rate_or_access_blocked_after_prior_failures'});return None,None,None
        pause=.45-(time.monotonic()-HOST_LAST.get(host,0))
        if pause>0:time.sleep(pause)
        entry={'url':url,'purpose':purpose,'at_utc':now()}
        try:
            req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/pdf,application/xml,text/html,application/json,*/*'})
            with urllib.request.urlopen(req,timeout=12)as response:
                chunks=[];size=0;transfer_started=time.monotonic()
                while True:
                    if time.monotonic()-transfer_started>35:raise TimeoutError('35 second total response-transfer ceiling')
                    piece=response.read1(65536)
                    if not piece:break
                    size+=len(piece)
                    if size>60*1024*1024:raise ValueError('response exceeds 60MiB ceiling')
                    chunks.append(piece)
                data=b''.join(chunks)
                final=response.geturl();ct=response.headers.get('content-type','')
                entry.update(status=response.status,final_url=final,content_type=ct,bytes=len(data),sha256=digest(data))
                rec['attempts'].append(entry)
                return data,final,ct
        except Exception as error:
            code=getattr(error,'code',None)
            entry.update(outcome='error',error=str(error),status=code)
            rec['attempts'].append(entry)
            if code in (403,429):
                with LOCK:
                    BLOCKS[host]=BLOCKS.get(host,0)+1
                    if code==429 or BLOCKS[host]>=3:DISABLED.add(host)
            return None,None,None
        finally:HOST_LAST[host]=time.monotonic()


def api(url,rec,name,directory):
    data,final,ct=request(url,rec,name)
    if data is None:return None
    (directory/(name+'.json')).write_bytes(data)
    try:return json.loads(data)
    except (ValueError,UnicodeDecodeError):return None


def identity(row,path):
    text=skill.extract_pdf_text(path,max_pages=2)
    result=skill.assess_source_identity({'doi':row.get('doi',''),'title':row['title'],'first_author':json.loads(row['authors'])[0] if row['authors'] else ''},text)
    pagecount=skill.pdf_page_count(path)
    front=skill.first_page_front_matter(text)
    expected=norm(row['title'])
    # Independent advisory evidence, never relabel the skill's unresolved status.
    title_present=bool(expected and expected in norm(front))
    author=json.loads(row['authors'])[0] if row['authors']else ''
    surname=norm(author).split()[-1:] if author else []
    author_present=bool(surname and surname[0]in norm(front).split())
    return {'source_identity':result,'page_count':pagecount,'title_match':skill.classify_title_match(row['title'],text),'advisory_complete_title_in_front':title_present,'advisory_first_author_surname_in_front':author_present,'first_pages_text_path':str(path.with_suffix('.front.txt'))},text


def register_pdf(data,url,row,rec,directory,origin):
    if not skill.is_valid_pdf(data):return False
    sha=digest(data)
    if any(f.get('sha256')==sha for f in rec['files']):return False
    path=directory/('candidate-'+str(len(rec['files'])+1)+'.pdf');path.write_bytes(data)
    assessed,text=identity(row,path)
    path.with_suffix('.front.txt').write_text(text or '')
    item={'path':str(path),'format':'pdf','sha256':sha,'bytes':len(data),'source_url':url,'origin':origin,**assessed}
    rec['files'].append(item)
    return assessed['source_identity']['status']=='consistent' or (assessed['advisory_complete_title_in_front'] and assessed['advisory_first_author_surname_in_front'])


def pdf_links(text,base):
    primary=[];other=[]
    for tag in re.findall(r'<meta\b[^>]*>',text,re.I):
        attrs=dict((k.lower(),html.unescape(v))for k,q,v in re.findall(r'([\w:-]+)\s*=\s*([\"\'])(.*?)\2',tag,re.S))
        if attrs.get('name','').lower()in ('citation_pdf_url','dc.identifier')and attrs.get('content'):
            if attrs.get('name')=='citation_pdf_url' or '.pdf'in attrs['content'].lower():primary.append(urllib.parse.urljoin(base,attrs['content']))
    for link in re.findall(r'href\s*=\s*[\"\']([^\"\']+)[\"\']',text,re.I):
        if '.pdf'in link.lower()or '/download/'in link.lower()or '/bitstreams/'in link.lower():other.append(urllib.parse.urljoin(base,html.unescape(link)))
    return list(dict.fromkeys(primary+other))


def landing(url,row,rec,directory,purpose,deadline,seen):
    if time.monotonic()>deadline or url in seen:return False
    seen.add(url)
    data,final,ct=request(url,rec,purpose)
    if data is None:return False
    if data.startswith(b'%PDF-'):return register_pdf(data,final,row,rec,directory,purpose)
    if 'html'in (ct or '')or data.lstrip().startswith((b'<!DOCTYPE',b'<html')):
        text=data.decode('utf8','replace')
        lp=directory/('landing-'+str(sum(1 for p in directory.glob('landing-*.html'))+1)+'.html');lp.write_bytes(data)
        rec.setdefault('landing_files',[]).append({'path':str(lp),'url':final,'sha256':digest(data),'bytes':len(data)})
        for link in pdf_links(text,final)[:5]:
            if time.monotonic()>deadline:break
            if link in seen:continue
            seen.add(link)
            content,resolved,ct=request(link,rec,'linked_pdf')
            if content and register_pdf(content,resolved,row,rec,directory,'linked_pdf'):return True
    return False


EXISTING=[]


def retrieve(row,force=False):
    ident=key(row);directory=CACHE/'records'/ident;directory.mkdir(parents=True,exist_ok=True)
    resultpath=directory/'result.json'
    if resultpath.exists()and not force:return json.loads(resultpath.read_text())
    rec={'candidate_key':row['candidate_key'],'doi':row['doi'],'title':row['title'],'field':row['field'],'form':row['form_name'],'started_at_utc':now(),'files':[],'attempts':[],'status':'not_retrieved','unpaywall':'enabled'if CONTACT else 'not_used_no_configured_contact_email'}
    deadline=time.monotonic()+150
    try:
        # Previously retained copies: exact DOI or complete normalized title near front.
        for item in EXISTING:
            front=norm(skill.first_page_front_matter(item['first_pages']))
            doi=(row['doi']or'').lower()
            identifiers=[v.lower()for v in skill.front_matter_identifiers(item['first_pages'][:6000])]
            if (doi and doi in identifiers)or (len(norm(row['title']).split())>=4 and norm(row['title'])in front):
                p=Path(item['path'])
                if register_pdf(p.read_bytes(),str(p),row,rec,directory,'existing_local_copy'):
                    rec['status']='downloaded_pdf';return rec
        doi=row['doi'];seen=set();candidates=[]
        if doi:
            if CONTACT:
                up=api('https://api.unpaywall.org/v2/'+urllib.parse.quote(doi,safe='/')+'?email='+urllib.parse.quote(CONTACT),rec,'unpaywall',directory)
                if up:
                    for loc in [up.get('best_oa_location'),*up.get('oa_locations',[])]:
                        if loc:candidates.extend(v for v in [loc.get('url_for_pdf'),loc.get('url')]if v)
            ep=api('https://www.ebi.ac.uk/europepmc/webservices/rest/search?query='+urllib.parse.quote('DOI:'+doi)+'&format=json&resultType=core',rec,'europepmc',directory)
            for hit in (ep or{}).get('resultList',{}).get('result',[]):
                pmcid=hit.get('pmcid');rec['pmcid']=pmcid
                if pmcid:
                    candidates.insert(0,'https://europepmc.org/backend/ptpmcrender.fcgi?accid='+pmcid+'&blobtype=pdf')
                    data,final,ct=request('https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmcid+'/fullTextXML',rec,'europepmc_fulltext_xml')
                    if data:
                        try:
                            tree=ET.fromstring(data);body=tree.find('.//body');title=' '.join(tree.find('.//article-title').itertext())
                            if body is not None and len(' '.join(body.itertext()))>500 and norm(row['title'])in norm(title):
                                xp=directory/'fulltext.xml';xp.write_bytes(data)
                                rec['files'].append({'path':str(xp),'format':'xml','sha256':digest(data),'bytes':len(data),'source_url':final,'origin':'europepmc','identity':'exact_article_title_and_doi_lookup','body_text_characters':len(' '.join(body.itertext()))})
                        except (ET.ParseError,AttributeError):pass
            oa=api('https://api.openalex.org/works/https://doi.org/'+urllib.parse.quote(doi,safe='/'),rec,'openalex',directory)
            if oa:
                rec['resolved_openalex_doi']=oa.get('doi');rec['resolved_openalex_title']=oa.get('title')
                locs=[oa.get('best_oa_location'),oa.get('primary_location'),*oa.get('locations',[])]
                candidates.extend(loc.get('pdf_url')for loc in locs if loc and loc.get('pdf_url'))
                candidates.extend(loc.get('landing_page_url')for loc in locs if loc and loc.get('is_oa')and loc.get('landing_page_url'))
                for loc in locs:
                    if loc:
                        arxiv=re.search(r'arxiv\.org/(?:abs|pdf)/([^?#]+)',str(loc.get('landing_page_url','')))
                        if arxiv:candidates.append('https://arxiv.org/pdf/'+arxiv.group(1).removesuffix('.pdf'))
            # Good OA locations first; defer Crossref until needed.
            for url in list(dict.fromkeys(candidates))[:9]:
                if landing(url,row,rec,directory,'oa_candidate',deadline,seen):rec['status']='downloaded_pdf';return rec
            cr=api('https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='/'),rec,'crossref',directory)
            if cr:
                msg=cr.get('message',{});rec['resolved_crossref_doi']=msg.get('DOI');rec['resolved_crossref_title']=msg.get('title')
                candidates=[l['URL']for l in msg.get('link',[])if l.get('URL')]
                primary=msg.get('resource',{}).get('primary',{}).get('URL')
                if primary:candidates.append(primary)
                for url in list(dict.fromkeys(candidates))[:4]:
                    if landing(url,row,rec,directory,'crossref_candidate',deadline,seen):rec['status']='downloaded_pdf';return rec
        url=row['stable_url']
        # Official pinned source downloads for software documents.
        if 'github.com/'in url and '/blob/'in url:
            raw=url.replace('github.com/','raw.githubusercontent.com/').replace('/blob/','/').split('#')[0]
            data,final,ct=request(raw,rec,'pinned_source_download')
            if data:
                p=directory/'source.rst';p.write_bytes(data);rec['files'].append({'path':str(p),'format':'rst','sha256':digest(data),'bytes':len(data),'source_url':final,'origin':'official_pinned_source','identity':'registered_source_file_container_scope_requires_section_selection'})
                rec['status']='downloaded_source';return rec
        arxiv=re.search(r'arxiv\.org/abs/([^?#]+)',url)
        if arxiv:
            if landing('https://arxiv.org/pdf/'+arxiv.group(1),row,rec,directory,'arxiv',deadline,seen):rec['status']='downloaded_pdf';return rec
        if landing(url,row,rec,directory,'registered_landing',deadline,seen):rec['status']='downloaded_pdf';return rec
        if any(f['format']=='xml'for f in rec['files']):rec['status']='downloaded_xml'
        elif rec['files']:rec['status']='candidate_needs_identity_review'
        elif rec.get('landing_files'):rec['status']='landing_only_fulltext_unconfirmed'
    except Exception as error:rec['error']=str(error)
    finally:
        rec['finished_at_utc']=now();rec['exhaustion_scope']='Bounded public routes, metadata candidates and linked PDFs; not proof no copy exists anywhere.'
        write_json(resultpath,rec)
    return rec


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=6);parser.add_argument('--force',action='store_true');parser.add_argument('--only',nargs='*');args=parser.parse_args()
    global EXISTING
    EXISTING=json.loads((CACHE/'existing-pdf-index.json').read_text())
    rows=list(csv.DictReader((REPO/'experiments/library-expansion-2026-11-16/library-pull-list.csv').open()))
    if args.only:rows=[r for r in rows if r['candidate_key']in args.only or r['doi']in args.only]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers)as pool:
        futures={pool.submit(retrieve,row,args.force):row for row in rows}
        counts={}
        for i,f in enumerate(concurrent.futures.as_completed(futures),1):
            result=f.result();counts[result['status']]=counts.get(result['status'],0)+1
            print(json.dumps({'done':i,'total':len(rows),'counts':counts,'last':result['candidate_key']},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
