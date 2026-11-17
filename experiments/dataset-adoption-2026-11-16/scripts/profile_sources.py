"""Count original units and labels without assigning paragraph functions."""
import ast
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parents[1]
CACHE=Path('/workspace/repos/builderbob/.writing-corpus-cache/dataset-adoption-2026-11-16')

def root(name):
    paths=list((CACHE/name/'unpacked').iterdir())
    assert len(paths)==1, (name,paths)
    return paths[0]

def main():
    profiles=[]
    def emit(dataset,**values):
        profiles.append(dict(dataset=dataset,**values));print(dataset,flush=True)
    # GUM: one authoritative graph directory, not duplicate _build and conversion layers.
    fs=sorted((root('gum')/'rst/rstweb').glob('*.rs4'))
    labels=Counter();primary=Counter();secondary=Counter();declared=set();errors=[]
    for p in fs:
        tree=ET.parse(p)
        declared.update(x.attrib['name'] for x in tree.findall('.//rel') if 'name' in x.attrib)
        labels.update(x.attrib['relname'] for x in tree.iter() if 'relname' in x.attrib)
        primary.update(x.attrib['relname'] for x in tree.iter() if x.tag in {'segment','group'} and 'relname' in x.attrib)
        secondary.update(x.attrib['relname'] for x in tree.iter() if x.tag=='secedge' and 'relname' in x.attrib)
    emit('GUM/eRST',files=len(fs),unit='RS4 graph file; primary segment/group parent attachments and secondary edges counted separately; not paragraph/function counts',
         directory=str(fs[0].parent),declared_labels=sorted(declared),all_relation_attribute_counts=dict(labels),primary_attachment_label_counts=dict(primary),secondary_edge_label_counts=dict(secondary),
         structural_labels=['span'],semantic_labels=sorted(set(labels)-{'span'}),
         limitation='Includes GENTLE challenge documents and source-specific rights; duplicate _build views and GDTB conversions excluded.')
    p=root('readme')/'input/dataset_combined.csv'
    with p.open(newline='') as source:rows=list(csv.DictReader(source))
    active=[r for r in rows if r['Codes with >= 2 votes']!='-']
    labels=Counter(code for r in active for code in r['Codes with >= 2 votes'])
    emit('READMEClassifier',file=str(p),unit='CSV section row; multi-code occurrences counted separately',
         raw_rows=len(rows),excluded_rows=len(rows)-len(active),coded_rows=len(active),
         active_file_ids=len({r['file-id'] for r in active}),numeric_code_counts=dict(labels),
         serialized_codes={str(i+1):n for i,n in enumerate(['What','Why','How','When','Who','References','Contribution','Other'])},
         bundled_markdown_files=len(list((root('readme')/'input/dev_and_eval_readmes').glob('*.md'))),
         limitation='CSV plus 441 bundled Markdown copies and a section-text SQLite database. Exact section-to-document correspondence and original per-project rights still require verification.')
    fs=list((root('india50')/'data/text').glob('*.txt'));labels=Counter();bad=0
    for p in fs:
        for line in p.read_text().splitlines():
            if not line.strip():continue
            if '\t' not in line:bad+=1;continue
            labels[line.rsplit('\t',1)[1]]+=1
    emit('Indian-50',files=len(fs),unit='source sentence line',label_counts=dict(labels),malformed_lines=bad,
         limitation='Serialized full names differ from paper label abbreviations; source legal roles are not paragraph functions.')
    fs=list((root('microtexts')/'corpus/en').glob('*.xml'));nodes=Counter();edges=Counter();roles=Counter()
    for p in fs:
        tree=ET.parse(p)
        for x in tree.iter():
            nodes[x.tag]+=1
            if x.tag=='edge':edges[x.attrib.get('type')]+=1
            if x.tag=='adu':roles[x.attrib.get('type')]+=1
    emit('Argumentative microtexts English',files=len(fs),unit='English translated text graph; node and edge occurrences',
         node_counts=dict(nodes),edge_counts=dict(edges),adu_role_counts=dict(roles),
         limitation='English/German versions overlap; two languages are not independent texts; graph edges may target other edges.')
    fs=sorted((root('scidtb')/'dataset').rglob('*.dep'));labels=Counter();ids=set();malformed=[]
    bysplit=Counter()
    for p in fs:
        try:items=json.loads(p.read_text(encoding='utf-8-sig'))['root']
        except Exception as e:malformed.append({'file':str(p),'error':str(e)});continue
        bysplit[str(p.relative_to(root('scidtb')/'dataset').parent)]+=1
        ids.add(re.sub(r'_anno\d+$','',p.name.replace('.edu.txt.dep','')))
        labels.update(x.get('relation','MISSING') for x in items)
    emit('SciDTB',files=len(fs),unique_base_ids=len(ids),unit='dependency tree and original EDU relation occurrence',
         files_by_split_path=dict(bysplit),relation_counts=dict(labels),parse_errors=malformed,
         limitation='Repeated annotations and split/organization copies require explicit matching; ROOT/null are structural, not functions.')
    fs=sorted(root('wlp').rglob('*.ann'));entities=Counter();event_roles=Counter();unpaired=[]
    for p in fs:
        if not p.with_suffix('.txt').exists():unpaired.append(str(p))
        for line in p.read_text().splitlines():
            if line.startswith('T'):
                parts=line.split('\t')
                if len(parts)>1:entities[parts[1].split()[0]]+=1
            if line.startswith('E') and '\t' in line:
                for pair in line.split('\t',1)[1].split()[1:]:event_roles[pair.split(':')[0]]+=1
    emit('WLP 2018',annotation_files=len(fs),unit='BRAT annotation file, text-bound entity and event argument occurrence',
         entity_label_counts=dict(entities),event_argument_counts=dict(event_roles),unpaired_annotations=unpaired,
         limitation='Action/entity spans are not whole instructions; numbered role variants preserved; overlaps later WLP versions.')
    # ECHR processed arrays are parsed as literal data, never evaluated as Python code.
    r=root('echr-main');folders=[p for p in (r/'data').iterdir() if p.is_dir()]
    layers={}
    for folder in folders:
        fs=list(folder.glob('*.csv'));labels=Counter();rows_count=0;bad=0
        for p in fs:
            with p.open(newline='') as source:
                for row in csv.DictReader(source,delimiter='\t'):
                    try:
                        tokens=ast.literal_eval(row['tokens']);codes=ast.literal_eval(row['labels'])
                        bad+=int(len(tokens)!=len(codes));labels.update(codes);rows_count+=1
                    except (KeyError,ValueError,SyntaxError):bad+=1
        if fs:layers[folder.name]={'files':len(fs),'rows':rows_count,'token_label_counts':dict(labels),'malformed_or_length_mismatch':bad}
    emit('LAM:ECHR',layers=layers,unit='processed paragraph row and token BIO label; actor/type layers overlap source texts',
         limitation='Processed The Law onward arrays are not independent corpora by layer and lack explicit argument-target edges.')
    # Only retain aggregate role/ID counts from PERSUADE, excluding all demographic fields.
    for split,path in [('train',CACHE/'persuade-train/persuade-training.csv'),('test',CACHE/'persuade-test/unpacked/persuade_corpus_2.0_test.csv')]:
        if not path.exists():continue
        csv.field_size_limit(10000000)
        with path.open(newline='',encoding='utf-8-sig') as source:
            reader=csv.DictReader(source);columns=reader.fieldnames
            labels=Counter();essay_ids=set();count=0;bad_offsets=0;checked=0
            for row in reader:
                count+=1
                essay_ids.add(row.get('essay_id',row.get('id','MISSING')))
                labels[row.get('discourse_type','MISSING')]+=1
                if {'discourse_start','discourse_end','full_text'}<=set(row):
                    try:
                        start,end=int(row['discourse_start']),int(row['discourse_end'])
                        bad_offsets+=int(not (0<=start<=end<=len(row['full_text'])))
                        checked+=1
                    except (ValueError,TypeError):bad_offsets+=1
        emit('PERSUADE 2.0 '+split,unit='CSV discourse-element row; unique essay IDs per split',
             csv_path=str(path),rows=count,unique_essay_ids=len(essay_ids),discourse_type_counts=dict(labels),
             offset_bounds_checked=checked,out_of_bounds_or_invalid_offsets=bad_offsets,
             limitation='School assignment writing; row totals are not essays; demographic fields are not included in derived outputs. Offset bounds do not establish semantic validity or exact text agreement.')
    # CORE is form/register metadata, not fine-grained paragraph-function annotation.
    split_counts={};labels=Counter();ids=set();duplicates=0
    for p in root('core').glob('*.tsv.gz'):
        count=0
        with gzip.open(p,'rt',encoding='utf-8') as source:
            for line in source:
                parts=line.rstrip('\n').split('\t',2)
                if len(parts)!=3:continue
                count+=1;labels[parts[0]]+=1
                duplicates+=int(parts[1] in ids);ids.add(parts[1])
        split_counts[p.name]=count
    emit('CORE',unit='web document row and original register-label combination',split_counts=split_counts,
         unique_ids=len(ids),repeated_ids=duplicates,register_combinations=dict(labels),
         limitation='Coarse register labels assist form selection; uncurated web documents do not establish professional quality or paragraph-function labels.')
    # BAWE has multiple encodings and derived views of the same assignments.
    br=root('bawe-data')
    fs=sorted((br/'CORPUS_ASCII').glob('*.xml'));families=Counter();parse_errors=[];missing_family=0
    for p in fs:
        try:
            tree=ET.parse(p)
            values=[(x.text or '').strip() for x in tree.iter('p') if x.attrib.get('n')=='genre family']
            if not values:missing_family+=1
            families.update(values)
        except ET.ParseError as error:parse_errors.append({'file':str(p),'error':str(error)})
    emit('BAWE',unit='assignment source file; one chosen XML representation only',
         plain_text_files=len(list((br/'CORPUS_TXT').glob('*.txt'))),
         selected_xml_files=len(fs),genre_family_header_counts=dict(families),
         missing_family_headers=missing_family,parse_errors=parse_errors,
         limitation='University student assignments; component texts differ from assignments. Multiple encodings and derived views are not extra documents. Source record declares CC BY-NC-SA 3.0.')
    result={'purpose':'Observed original units/labels only. No source-label count is a paragraph-function count or validated crosswalk coverage.','profiles':profiles}
    (BASE/'source-profiles.json').write_text(json.dumps(result,indent=2)+'\n')
    print('profiles',len(profiles),flush=True)

if __name__=='__main__':main()
