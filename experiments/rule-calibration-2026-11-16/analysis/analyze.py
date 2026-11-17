"""Matched exploratory comparison; source truth and semantic accuracy unscored."""
from collections import Counter, defaultdict
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

from contract import normalize, validate, FUNCTION_FIELDS, RELATIONS

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = Path('/workspace/repos/builderbob/.writing-corpus-cache/rule-calibration/packets')
metric_path = ROOT.parent / 'corpus-analysis-2026-11-16/analysis/metrics.py'
spec = importlib.util.spec_from_file_location('common_metrics', metric_path)
metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metrics)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair_stats(pairs, field='clear_labels'):
    counts = Counter(n=len(pairs))
    jaccards = []
    for a,b in pairs:
        x,y = set(a[field]), set(b[field])
        counts['exact'] += x == y
        counts['strict_subset'] += x < y or y < x
        counts['two_sided'] += bool(x-y) and bool(y-x)
        counts['both_empty'] += not (x|y)
        jaccards.append(len(x&y)/len(x|y) if x|y else 1.)
    return {**{k:counts[k] for k in ('n','exact','strict_subset','two_sided','both_empty')},
            'exact_rate':counts['exact']/counts['n'] if counts['n'] else None,
            'mean_jaccard':sum(jaccards)/len(jaccards) if jaccards else None}


def intervals(anchors):
    groups = defaultdict(list)
    for a in anchors:
        groups[a['unit_id']].append((a['start'],a['end']))
    result = {}
    for uid, spans in groups.items():
        merged = []
        for start,end in sorted(spans):
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0],max(end,merged[-1][1]))
            else:
                merged.append((start,end))
        result[uid] = merged
    return result


def length(spans):
    return sum(end-start for ranges in spans.values() for start,end in ranges)


def span_iou(a,b):
    shared = sum(max(0,min(ae,be)-max(ast,bst)) for uid in a.keys()&b.keys()
                 for ast,ae in a[uid] for bst,be in b[uid])
    union = length(a)+length(b)-shared
    return shared/union if union else None


def check_freeze():
    checks = []
    for name in ('freeze.json','interface-freeze.json'):
        receipt = json.loads((ROOT/'protocol'/name).read_text())
        for rec in receipt['files']:
            p = ROOT/'protocol'/rec['file'] if 'file' in rec else ROOT.parents[1]/rec['path']
            # Interface receipt paths are repository-relative.
            if not p.exists() and 'path' in rec:
                p = Path(rec['path'])
            checks.append({'path':str(p),'expected':rec['sha256'],'actual':sha(p)})
    sample = json.loads((ROOT/'protocol/sample-freeze.json').read_text())
    checks.append({'path':'sampling/source-manifest.json','expected':sample['sampling_manifest_sha256'],'actual':sha(ROOT/'sampling/source-manifest.json')})
    for stage in sample['packets']:
        for rec in stage['files']:
            checks.append({'path':rec['path'],'expected':rec['sha256'],'actual':sha(Path(rec['path']))})
    assert all(x['expected']==x['actual'] for x in checks), 'frozen input changed'
    return checks


def main():
    freeze = check_freeze()
    packets, manifests, validation = {}, {}, []
    for stage in ('A','B'):
        manifest = manifests[stage] = json.loads((PRIVATE/stage/'manifest.json').read_text())
        for arm in ('original','revised'):
            for coder in (1,2):
                cid = f'{stage}-{arm}-{coder}'
                directory = ROOT/'coding'/cid
                files = sorted(directory.glob('raw*.json'),key=lambda p:1 if p.stem=='raw' else int(p.stem.removeprefix('raw-v')))
                if not files:
                    raise RuntimeError(f'missing {cid}')
                for p in files:
                    raw = json.loads(p.read_text())
                    errors = validate(raw,manifest)
                    validation.append({'coder_id':cid,'file':str(p.relative_to(ROOT)),'sha256':sha(p),'errors':errors,'selected':p==files[-1]})
                raw = json.loads(files[-1].read_text())
                assert raw['coder_id']==cid and raw['arm']==arm and raw['stage']==stage and raw['model']=='gpt-6.1-terra'
                packet = normalize(raw,manifest)
                packet['submission'] = {'path':str(files[-1].relative_to(ROOT)), 'sha256':sha(files[-1]),'bytes':files[-1].stat().st_size,'compact_characters':len(json.dumps(raw,ensure_ascii=False,separators=(',',':'))),'submission_count':len(files)}
                packets[cid] = packet
                (directory/'normalized.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
    results = {'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'input_integrity':freeze,'validation':validation,'by_stage':{},'by_context':{},'by_document':{},'paired_differences':[], 'coder_effort':[], 'target_proxy':[], 'lengths':{},'per_label':{}}
    allpairs = defaultdict(list)
    annotations = {cid:{a['paragraph_id']:a for a in p['annotations']} for cid,p in packets.items()}
    for stage,manifest in manifests.items():
        results['by_stage'][stage] = {}
        for arm in ('original','revised'):
            pairs = [(annotations[f'{stage}-{arm}-1'][t['paragraph_id']],annotations[f'{stage}-{arm}-2'][t['paragraph_id']]) for t in manifest['targets']]
            allpairs[arm].extend(pairs)
            results['by_stage'][stage][arm] = {field:pair_stats(pairs,field) for field in ('clear_labels','candidate_union')}
            for source in manifest['sources']:
                selected=[t for t in manifest['targets'] if t['source_id']==source['id']]
                spairs=[(annotations[f'{stage}-{arm}-1'][t['paragraph_id']],annotations[f'{stage}-{arm}-2'][t['paragraph_id']]) for t in selected]
                row = results['by_document'].setdefault(source['id'],{'title':source['title'],'stage':stage,'stratum':source['stratum']})
                row[arm]={field:pair_stats(spairs,field) for field in ('clear_labels','candidate_union')}
        for target in manifest['targets']:
            pid=target['paragraph_id']
            row={**target}
            for arm in ('original','revised'):
                x,y=[annotations[f'{stage}-{arm}-{i}'][pid] for i in (1,2)]
                row[arm]={field:[x[field],y[field]] for field in ('clear_labels','unresolved_labels','candidate_union')}
            results['paired_differences'].append(row)
            x,y=[annotations[f'{stage}-revised-{i}'][pid] for i in (1,2)]
            for fid in sorted(RELATIONS & set(x['clear_labels']) & set(y['clear_labels'])):
                anchors=[]
                for ann in (x,y):
                    anchors.append([a for role in ann['roles'] if role['function_id']==fid and role['decision']=='present' for tg in role['targets'] for a in tg['anchors']])
                spans=[intervals(a) for a in anchors]
                results['target_proxy'].append({'paragraph_id':pid,'function_id':fid,'unit_sets':list(map(lambda x:sorted(x),spans)),'exact_unit_set':set(spans[0])==set(spans[1]),'character_span_iou':span_iou(*spans)})
    results['pooled']={arm:{field:pair_stats(allpairs[arm],field) for field in ('clear_labels','candidate_union')} for arm in ('original','revised')}
    for arm in ('original','revised'):
        results['per_label'][arm]={}
        for fid in FUNCTION_FIELDS:
            c=Counter()
            for a,b in allpairs[arm]:
                x,y=fid in a['clear_labels'],fid in b['clear_labels']
                c['both_positive' if x and y else 'coder1_only' if x else 'coder2_only' if y else 'both_negative']+=1
            den=2*c['both_positive']+c['coder1_only']+c['coder2_only']
            results['per_label'][arm][fid]={**dict(c),'positive_agreement':2*c['both_positive']/den if den else None}
    strata={t['stratum'] for m in manifests.values() for t in m['targets']}
    for stratum in sorted(strata):
        results['by_context'][stratum]={}
        for arm in ('original','revised'):
            pairs=[]
            for stage,m in manifests.items():
                pairs.extend((annotations[f'{stage}-{arm}-1'][t['paragraph_id']],annotations[f'{stage}-{arm}-2'][t['paragraph_id']]) for t in m['targets'] if t['stratum']==stratum)
            results['by_context'][stratum][arm]={field:pair_stats(pairs,field) for field in ('clear_labels','candidate_union')}
    bylayer={'local_move':{'define','report','assert','explain','compare','interpret','instruct'},'temporal_presentation':{'narrate'},'relation':RELATIONS}
    results['revised_layers']={}
    for layer,fids in bylayer.items():
        pairs=[({'clear_labels':list(set(a['clear_labels'])&fids)},{'clear_labels':list(set(b['clear_labels'])&fids)})for a,b in allpairs['revised']]
        results['revised_layers'][layer]=pair_stats(pairs)
    for cid,packet in packets.items():
        aa=packet['annotations']
        roles=[role for a in aa for role in a['roles']]
        elapsed=(datetime.datetime.fromisoformat(packet['finished_at_utc'].replace('Z','+00:00'))-datetime.datetime.fromisoformat(packet['started_at_utc'].replace('Z','+00:00'))).total_seconds()
        results['coder_effort'].append({'coder_id':cid,**packet['submission'],'elapsed_seconds':elapsed,'paragraphs':len(aa),'roles':len(roles),'clear_label_assignments':sum(len(a['clear_labels'])for a in aa),'candidate_label_assignments':sum(len(a['candidate_union'])for a in aa),'unresolved_paragraphs':sum(bool(a['unresolved_labels'])for a in aa),'unresolved_roles':sum(r['decision']=='unresolved'for r in roles),'empty_clear_paragraphs':sum(not a['clear_labels']for a in aa),'reviewed_units_unique':len({uid for a in aa for uid in a['context']['reviewed_units']})})
    whole=defaultdict(list)
    for m in manifests.values():
        units={u['unit_id']:u for u in m['units']}
        for t in m['targets']:
            whole[t['stratum']].append(len(metrics.word_tokens(units[t['unit_id']]['text'])))
    results['lengths']['whole_paragraph_by_context']={k:metrics.summarize(v)for k,v in whole.items()}
    results['lengths']['role_span_by_coder']={}
    for cid,p in packets.items():
        units={u['unit_id']:u for u in manifests[p['stage']]['units']}
        spans=defaultdict(list)
        for a in p['annotations']:
            for role in a['roles']:
                if role['decision']=='present':
                    union=intervals(role['anchors'])
                    # Count only this paragraph's anchor union, retaining context scope separately in records.
                    text=' '.join(units[a['paragraph_id']]['text'][s:e]for s,e in union.get(a['paragraph_id'],[]))
                    spans[role['function_id']].append(len(metrics.word_tokens(text)))
        results['lengths']['role_span_by_coder'][cid]={fid:metrics.summarize(v)for fid,v in spans.items()}
    results['lengths']['provenance']={'tokenizer_path':str(metric_path),'tokenizer_sha256':sha(metric_path),'scope':'36 unique whole target paragraphs; role spans are within-target union per clear role per coder, nonadditive across roles; context anchors excluded from role-length count','working_targets':None,'minimum_limits':None,'maximum_limits':None}
    (ROOT/'results/comparison.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'by_stage':results['by_stage'],'pooled':results['pooled']},indent=2))


if __name__=='__main__':
    main()
