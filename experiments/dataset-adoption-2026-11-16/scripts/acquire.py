"""Download declared public research artifacts, preserving hashes and failures.

No upstream code or serialized Python objects are executed. Archives are unpacked
as regular files under the workspace cache; links and traversal paths are refused.
"""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import time
import urllib.error
import urllib.request
import zipfile

BASE = Path(__file__).resolve().parents[1]
CACHE = Path('/workspace/repos/builderbob/.writing-corpus-cache/dataset-adoption-2026-11-16')
UA = 'Writing-harness-dataset-reuse-research/1.0'
LIMIT = 1024 * 1024 * 1024


def fetch(url, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + '.part')
    for attempt in range(2):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(request, timeout=90) as response, partial.open('wb') as output:
                total = 0
                sha = hashlib.sha256()
                while block := response.read(1024 * 1024):
                    total += len(block)
                    if total > LIMIT:
                        raise ValueError('Artifact exceeded declared 1 GiB per-file transfer bound')
                    output.write(block)
                    sha.update(block)
                meta = {'requested_url': url, 'effective_url': response.url,
                        'content_type': response.headers.get('Content-Type'),
                        'bytes': total, 'sha256': sha.hexdigest(), 'http_status': response.status}
            partial.replace(path)
            return meta
        except Exception:
            partial.unlink(missing_ok=True)
            if attempt:
                raise
            time.sleep(0.5)


def unpack(path, destination):
    destination.mkdir(parents=True, exist_ok=True)
    count, total = 0, 0
    def target(name):
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or '\\' in name:
            raise ValueError('Unsafe archive path')
        return destination.joinpath(*p.parts)
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if member.is_dir() or (member.external_attr >> 16) & 0o170000 == 0o120000:
                    continue
                dst = target(member.filename)
                total += member.file_size
                if total > 4 * LIMIT:
                    raise ValueError('Expanded archive exceeds declared 4 GiB bound')
                dst.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as source, dst.open('wb') as output:
                    shutil.copyfileobj(source, output)
                count += 1
    else:
        with tarfile.open(path, 'r:*') as archive:
            for member in archive:
                if not member.isfile():
                    continue
                dst = target(member.name)
                total += member.size
                if total > 4 * LIMIT:
                    raise ValueError('Expanded archive exceeds declared 4 GiB bound')
                dst.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source, dst.open('wb') as output:
                    shutil.copyfileobj(source, output)
                count += 1
    return {'regular_files': count, 'expanded_bytes': total, 'extracted_path': str(destination)}


def acquire(item):
    record = dict(item)
    try:
        folder = CACHE / item['id']
        folder.mkdir(parents=True, exist_ok=True)
        if item['type'] == 'github_archive':
            revision = item.get('commit')
            if not revision:
                url = f"https://api.github.com/repos/{item['repo']}/commits/{item['branch']}"
                response = fetch(url, folder / 'commit.json')
                revision = json.loads((folder / 'commit.json').read_text())['sha']
                record['revision_metadata'] = response
            record['commit'] = revision
            url = f"https://codeload.github.com/{item['repo']}/tar.gz/{revision}"
            path = folder / 'source.tar.gz'
        elif item['type'] == 'existing_archive':
            path = Path(item['existing_path'])
            record['download'] = {'requested_url': item['url'], 'local_reuse': True,
                                  'bytes': path.stat().st_size,
                                  'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        else:
            url = item['url']
            path = folder / item['filename']
        if item['type'] != 'existing_archive':
            record['download'] = fetch(url, path)
        record['local_path'] = str(path)
        if item['type'] in {'github_archive', 'existing_archive', 'archive'}:
            record['extraction'] = unpack(path, folder / 'unpacked')
        elif path.suffix == '.pdf' and not path.read_bytes().startswith(b'%PDF-'):
            raise ValueError('Response is not a PDF; original response retained, not counted as acquired codebook')
        record['status'] = 'downloaded'
    except Exception as error:
        record['status'] = 'unavailable'
        record['error'] = type(error).__name__ + ': ' + str(error)
    return record


def main():
    plan = json.loads((BASE / 'acquisition-plan.json').read_text())
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(acquire, item) for item in plan['artifacts']]
        for future in concurrent.futures.as_completed(futures):
            record = future.result()
            records.append(record)
            payload = {'created_utc': datetime.now(timezone.utc).isoformat(),
                       'cache': str(CACHE), 'scope': plan['scope'],
                       'records': sorted(records, key=lambda r: r['id'])}
            temp = BASE / 'acquisition.json.tmp'
            temp.write_text(json.dumps(payload, indent=2) + '\n')
            temp.replace(BASE / 'acquisition.json')
            print(json.dumps({'id': record['id'], 'status': record['status'],
                              'bytes': record.get('download', {}).get('bytes'),
                              'error': record.get('error')}), flush=True)


if __name__ == '__main__':
    main()
