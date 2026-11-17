"""Save and read-verify a local research checkpoint without changing Git staging."""
import datetime
import hashlib
import io
import json
import stat
import subprocess
import tarfile
from pathlib import Path

TASK=Path(__file__).resolve().parent.parent
REPO=TASK.parent.parent
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
out=Path('/workspace/build/builderbob/write-with-purpose/checkpoints')/stamp
out.mkdir(parents=True)
roots=['README.md','docs/writing-harness','experiments/form-corpus-2026-11-16','experiments/corpus-analysis-2026-11-16','experiments/pattern-test-2026-11-16','experiments/paragraph-functions','experiments/library-expansion-2026-11-16','work']
files=[]
for name in roots:
    p=REPO/name
    files.extend([p] if p.is_file() else [x for x in p.rglob('*') if x.is_file() and not x.is_symlink() and '__pycache__' not in x.parts and x.suffix!='.pyc' and x.name!='checkpoint-final.json'])
index=[]
archive=out/'writing-harness-checkpoint.tar.gz'
with tarfile.open(archive,'w:gz',compresslevel=3) as tar:
    for p in sorted(set(files)):
        data=p.read_bytes();relative=str(p.relative_to(REPO));entry=tarfile.TarInfo(relative)
        entry.size=len(data);entry.mode=stat.S_IMODE(p.stat().st_mode)
        tar.addfile(entry,io.BytesIO(data))
        index.append(dict(path=relative,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
with tarfile.open(archive,'r:gz') as tar:
    members=tar.getmembers();assert len(members)==len(index)
    by_name={m.name:m for m in members}
    for row in index:
        data=tar.extractfile(by_name[row['path']]).read()
        assert hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
status=subprocess.check_output(['git','status','--short'],cwd=REPO,text=True)
diff=subprocess.check_output(['git','diff','--binary'],cwd=REPO,text=True)
(out/'working-tree.patch').write_text(diff)
manifest=dict(kind='local_research_checkpoint',created_utc=stamp,repository=str(REPO),head=head,
    git_status=status,git_index_modified=False,archive=str(archive),
    archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),archive_entries_read_verified=True,
    files=index,source_cache_policy='Original full article bytes and normalized source caches remain in their existing persistent /workspace locations; not embedded in this repository-work checkpoint. This is local recovery, not offsite backup.')
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
pointer={k:v for k,v in manifest.items() if k!='files'}
pointer['manifest']=str(out/'manifest.json');pointer['saved_files']=len(index)
(TASK/'checkpoint-final.json').write_text(json.dumps(pointer,indent=2)+'\n')
print(json.dumps({'checkpoint':str(out),'saved_files':len(index),'archive_bytes':archive.stat().st_size,'readback_verified':True,'git_index_modified':False}))
