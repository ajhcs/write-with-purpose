#!/usr/bin/env python3
"""Reanalyse retained pinned documentation source bytes; no network or source execution."""
import ast
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import tokenize
from markdown_it import MarkdownIt
from metrics import measure_document

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / 'form-corpus-2026-11-16/explanation-tutorial/records.jsonl'
CACHE = Path('/workspace/tmp/builderbob/writing-corpus/explanation-tutorial')
PRIVATE = Path('/workspace/repos/builderbob/.writing-corpus-cache/analysis/docs')
MD = MarkdownIt('commonmark').enable('table')


def plain_inline(token):
    # Keep inline code as displayed prose; line breaks separate words.
    return ''.join(' ' if t.type in ('softbreak', 'hardbreak') else
                   t.content if t.type in ('text', 'code_inline') else ''
                   for t in token.children or [])


def markdown_blocks(text):
    text = re.sub(r'\A(?:\ufeff)?---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.S)
    # Hugo shortcodes are not rendered. Drop standalone directives; for inline
    # shortcodes retain an explicit text= display label when provided.
    text = re.sub(r'(?m)^[ \t]*\{\{[<%][^\n]*?[>%]\}\}[ \t]*$', '', text)
    def inline_shortcode(match):
        label = re.search(r'\btext=[\"\']([^\"\']*)[\"\']', match.group())
        return label.group(1) if label else ''
    text = re.sub(r'\{\{[<%].*?[>%]\}\}', inline_shortcode, text, flags=re.S)
    tokens = MD.parse(text)
    blocks, objects = [], Counter()
    section = 'section-0000'
    section_num = 0
    list_depth = quote_depth = 0
    for i, t in enumerate(tokens):
        if t.type in ('bullet_list_open', 'ordered_list_open'):
            list_depth += 1
            objects['list_blocks'] += 1
        elif t.type in ('bullet_list_close', 'ordered_list_close'):
            list_depth -= 1
        elif t.type == 'blockquote_open':
            quote_depth += 1
            objects['blockquotes'] += 1
        elif t.type == 'blockquote_close':
            quote_depth -= 1
        elif t.type in ('fence', 'code_block'):
            blocks.append(dict(kind='code', text=t.content, section_id=section))
            objects['code_blocks'] += 1
        elif t.type == 'table_open':
            objects['tables'] += 1
        elif t.type == 'inline':
            for c in t.children or []:
                if c.type in ('link_open', 'image'):
                    objects['links' if c.type == 'link_open' else 'images'] += 1
            prev = tokens[i-1].type if i else ''
            content = plain_inline(t).strip()
            if not content:
                continue
            if prev == 'heading_open':
                section_num += 1
                section = f'section-{section_num:04d}'
                blocks.append(dict(kind='heading', text=content, section_id=section,
                                   heading_level=int(tokens[i-1].tag[1:])))
            elif prev == 'paragraph_open':
                kind = 'list_item' if list_depth else 'quote' if quote_depth else 'paragraph'
                blocks.append(dict(kind=kind, text=content, section_id=section))
    return blocks, objects


def rst_to_markdown(source):
    lines = source.splitlines(); out = []; omissions = 0; i = 0
    while i < len(lines):
        line = lines[i]; stripped = line.strip()
        if re.match(r'^\.\.\s', stripped):
            omissions += 1; i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i][:1].isspace()):
                i += 1
            continue
        if i + 1 < len(lines) and stripped and re.fullmatch(r'[=\-~^"`:+*#]{3,}\s*', lines[i+1].strip()):
            level = {'=': 1, '-': 2, '~': 3, '^': 3}.get(lines[i+1].strip()[0], 3)
            out.extend(['#' * level + ' ' + stripped, '']); i += 2; continue
        line = re.sub(r':\w+:`([^`<>]+)\s*<[^>]+>`', r'\1', line)
        line = re.sub(r':\w+:`([^`]+)`', r'\1', line)
        out.append(line); i += 1
    return '\n'.join(out), omissions


def source_to_blocks(data, fmt):
    source = data.decode('utf-8-sig'); flags = []; extras = Counter()
    if fmt == 'notebook':
        notebook = json.loads(source)
        pieces = []
        for cell in notebook.get('cells', []):
            s = cell.get('source', '')
            s = ''.join(s) if isinstance(s, list) else s
            if cell.get('cell_type') == 'markdown': pieces.append(s)
            elif cell.get('cell_type') == 'code':
                # Fenced code retains ordering without including outputs in prose.
                pieces.append('\n```\n' + s.replace('```', '`` `') + '\n```\n')
        text = '\n\n'.join(pieces)
        flags.extend(['notebook_outputs_omitted', 'notebook_markdown_unrendered'])
    elif fmt == 'rst':
        text, omissions = rst_to_markdown(source)
        extras['unexpanded_directives_omitted'] = omissions
        flags.append('rst_heuristic_directives_omitted')
    elif fmt == 'sphinx-gallery':
        tree = ast.parse(source)
        doc = ast.get_docstring(tree) or ''
        comments = []
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.COMMENT and tok.start[1] == 0:
                val = tok.string[1:].lstrip()
                comments.append('' if re.fullmatch(r'[%#=\-]{3,}', val) else val)
        text = doc + '\n\n' + '\n'.join(comments)
        flags.append('gallery_docstring_and_top_level_comments_only')
    else:
        text = source
    if re.search(r'\{[{%<]|\{%|\.\.\s+(?:include|literalinclude)::|\{include\}|<include', source, re.I):
        flags.append('possible_unexpanded_template_or_transclusion')
    blocks, objects = markdown_blocks(text)
    objects.update(extras)
    return blocks, objects, flags


def main():
    PRIVATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    PRIVATE.chmod(0o700)
    records = [json.loads(line) for line in OLD.read_text().splitlines()]
    results = []
    for r in records:
        source_path = CACHE / hashlib.sha256(r['raw_url'].encode()).hexdigest()
        data = source_path.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if actual != r['sha256']:
            raise ValueError(f"source hash mismatch for {r['id']}")
        fmt = r.get('source_format', 'markdown')
        blocks, objects, flags = source_to_blocks(data, fmt)
        metrics = measure_document(blocks, objects)
        nav = Path(r['path']).stem.lower() in ('index', '_index', 'readme')
        if nav: flags.append('possible_navigation_index')
        flags.append('source_not_rendered_or_parser_verified')
        private_path = PRIVATE / (r['id'] + '.json')
        private_path.write_text(json.dumps({'id': r['id'], 'blocks': blocks}, ensure_ascii=False) + '\n')
        private_path.chmod(0o600)
        meta = {k: v for k, v in r.items() if k != 'metrics'}
        meta.update(domain='software_documentation', era='current_version_at_pinned_commit_year_unknown',
                    form_candidate=r['proposed_form'], form_candidate_status='unverified',
                    extraction_tier='source_partial', profile_eligible=False,
                    profile_ineligibility_reason='source extraction has not been verified against rendered page',
                    source_cache_path=str(source_path), source_sha256_actual=actual,
                    source_format=fmt, extraction_flags=flags,
                    short_under_120_prose_words=metrics['prose_words'] < 120,
                    possible_navigation_index=nav, metrics=metrics)
        results.append(meta)
    (HERE / 'docs-records.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in results))
    print('processed', len(results), 'formats', dict(Counter(x['source_format'] for x in results)),
          'short', sum(x['short_under_120_prose_words'] for x in results),
          'possible index', sum(x['possible_navigation_index'] for x in results))

if __name__ == '__main__': main()
