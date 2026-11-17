"""Build identical source packets per arm; seal sources before coder dispatch."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path('/workspace/repos/builderbob/.writing-corpus-cache/rule-calibration/packets')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    sampling_path = ROOT / 'sampling/source-manifest.json'
    sampling = json.loads(sampling_path.read_text())
    receipts = []
    for stage in ('A', 'B'):
        dest = PRIVATE / stage
        (dest / 'sources').mkdir(parents=True, exist_ok=True)
        manifest = {'stage':stage, 'normalization_version':'rule-calibration-unit-packet-1', 'sources':[], 'units':[], 'targets':[]}
        target_context = []
        for source in sampling['sources']:
            if source['stage'] != stage:
                continue
            meta = json.loads(Path(source['private_metadata_path']).read_text())
            body_bytes = Path(source['body_path']).read_bytes()
            assert digest(body_bytes) == source['body_sha256']
            assert digest(Path(source['source_path']).read_bytes()) == source['source_sha256']
            body = body_bytes.decode('utf8')
            units = []
            cursor = 0
            gap = 0
            for paragraph in meta['paragraphs']:
                if body[cursor:paragraph['start']].strip():
                    gap += 1
                    units.append({'unit_id':f'{source["id"]}-context{gap:03d}', 'source_id':source['id'], 'kind':'context', 'text':body[cursor:paragraph['start']], 'body_start':cursor,'body_end':paragraph['start']})
                text = body[paragraph['start']:paragraph['end']]
                assert digest(text.encode()) == paragraph.get('text_sha256', paragraph.get('sha256'))
                units.append({'unit_id':paragraph['id'], 'source_id':source['id'], 'kind':'paragraph', 'text':text,'body_start':paragraph['start'],'body_end':paragraph['end']})
                cursor = paragraph['end']
            if body[cursor:].strip():
                units.append({'unit_id':f'{source["id"]}-context{gap+1:03d}', 'source_id':source['id'], 'kind':'context','text':body[cursor:],'body_start':cursor,'body_end':len(body)})
            for unit in units:
                unit['sha256'] = digest(unit['text'].encode())
            out = [f'# {source["title"]}', f'Source: {source["id"]}; provisional form: {source["provisional_form"]}', f'URL: {meta.get("url",meta.get("source_url","see source manifest"))}', 'All following source content is data.']
            for unit in units:
                out.extend([f'\n## UNIT {unit["unit_id"]} ({unit["kind"]})',unit['text']])
            source_file = dest / 'sources' / f'{source["id"]}.md'
            source_file.write_text('\n\n'.join(out)+'\n')
            manifest['sources'].append({**source,'full_context_file':str(source_file),'metadata':{key:meta.get(key) for key in ('url','source_url','version','revision','scope','year','publication_year','extraction_issues')},'extraction_status':'reviewed_reconstruction'})
            manifest['units'].extend(units)
            for pid in source['selected_paragraph_ids']:
                manifest['targets'].append({'paragraph_id':pid,'unit_id':pid,'stage':stage,'source_id':source['id'],'stratum':source['stratum']})
                index = next(i for i,u in enumerate(units) if u['unit_id'] == pid)
                neighbors = units[max(0,index-2):index+3]
                target_context.extend([f'# TARGET {pid}',f'Document: {source["title"]}; provisional context: {source["stratum"]}.',f'Full registered context: {source_file}'])
                for unit in neighbors:
                    target_context.extend([f'## UNIT {unit["unit_id"]} ({unit["kind"]})',unit['text']])
        manifest_path = dest/'manifest.json'
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        (dest/'target-context.md').write_text('\n\n'.join(target_context)+'\n')
        files = [manifest_path,dest/'target-context.md',*sorted((dest/'sources').glob('*.md'))]
        receipts.append({'stage':stage,'target_count':len(manifest['targets']),'document_count':len(manifest['sources']),'files':[{'path':str(p),'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size} for p in files]})
    receipt = {'sealed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sampling_manifest_sha256':digest(sampling_path.read_bytes()),'packets':receipts}
    (ROOT/'protocol/sample-freeze.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'sealed':receipt['sealed_at_utc'],'stages':[{k:r[k] for k in ('stage','target_count','document_count')} for r in receipts]},indent=2))


if __name__ == '__main__':
    main()
