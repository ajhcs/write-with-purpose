"""Prepare prespecified semantic diagnostics without arm labels or outcomes."""
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path('/workspace/repos/builderbob/.writing-corpus-cache/rule-calibration')


def main():
    out = PRIVATE/'blind-review'
    out.mkdir(exist_ok=True)
    manifest = {}
    for stage in ('A','B'):
        manifest[stage]=json.loads((PRIVATE/'packets'/stage/'manifest.json').read_text())
    key=[]
    packet={'masking':'Four anonymous coding records, independently shuffled within target; wording or target detail may reveal guidance. No correctness gold labels.', 'targets':[]}
    for stage,m in manifest.items():
        selected=m['targets'] if stage=='B' else [next(t for t in m['targets'] if t['source_id']==s['id'])for s in m['sources']]
        units={u['unit_id']:u for u in m['units']}
        sources={s['id']:s for s in m['sources']}
        codings={}
        for arm in ('original','revised'):
            for coder in (1,2):
                cid=f'{stage}-{arm}-{coder}'
                p=json.loads((ROOT/'coding'/cid/'normalized.json').read_text())
                codings[cid]={a['paragraph_id']:a for a in p['annotations']}
        for target in selected:
            pid=target['paragraph_id']
            source=sources[target['source_id']]
            row={'paragraph_id':pid,'title':source['title'],'provisional_context':target['stratum'],'full_context_file':source['full_context_file'],'text':units[pid]['text'],'codings':[]}
            index=next(i for i,u in enumerate(m['units'])if u['unit_id']==pid)
            row['neighbors']=[u for u in m['units'][max(0,index-2):index+3]if u['source_id']==source['id']]
            order=list(codings)
            random.Random(int(hashlib.sha256(('blind-pilot-20261116:'+pid).encode()).hexdigest(),16)).shuffle(order)
            for n,cid in enumerate(order,1):
                anon=f'R{n}'
                ann=codings[cid][pid]
                roles=[]
                for role in ann['roles']:
                    roles.append({k:role[k]for k in ('function_id','decision','status','anchors','reason')})
                    roles[-1]['anchors']=[{k:a[k]for k in ('unit_id','quote')}for a in role['anchors']]
                    if role.get('targets'):
                        roles[-1]['related_contributions']=[{'paraphrase':t['paraphrase'],'status':t['status'],'anchors':[{k:a[k]for k in ('unit_id','quote')}for a in t['anchors']]}for t in role['targets']]
                row['codings'].append({'record_id':anon,'roles':roles})
                key.append({'paragraph_id':pid,'record_id':anon,'coder_id':cid})
            packet['targets'].append(row)
    assert len(packet['targets'])==20
    p=out/'packet.json'
    p.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'results/blind-review-key.json').write_text(json.dumps(key,indent=2)+'\n')
    print(json.dumps({'path':str(p),'targets':len(packet['targets']),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))


if __name__=='__main__':
    main()
