"""Regression checks for source-block extraction; no network or source execution."""
import json
from pathlib import Path
import unittest
from analyze_docs import source_to_blocks


class DocsParserTests(unittest.TestCase):
    def test_wrapping_inline_code_and_shortcodes(self):
        source = b'''---\ntitle: Test\n---\nA wrapped\nsentence uses `cgroup` today.\n\n{{< feature-state state="stable" >}}\n\nLinux uses {{< glossary_tooltip text="control groups" term_id="cgroup" >}} here.\n'''
        blocks, _, flags = source_to_blocks(source, 'markdown')
        paragraphs = [b['text'] for b in blocks if b['kind'] == 'paragraph']
        self.assertEqual(paragraphs, ['A wrapped sentence uses cgroup today.', 'Linux uses control groups here.'])
        self.assertIn('possible_unexpanded_template_or_transclusion', flags)

    def test_retained_cgroups_source(self):
        records = Path(__file__).parent / 'docs-records.jsonl'
        first = json.loads(records.read_text().splitlines()[0])
        self.assertEqual(first['id'], 'b24ef0e9823783e8')
        blocks, _, _ = source_to_blocks(Path(first['source_cache_path']).read_bytes(), 'markdown')
        prose = ' '.join(b['text'] for b in blocks if b['kind'] == 'paragraph')
        for joined in ('theunderlying', 'enforceresource', 'isthe'):
            self.assertNotIn(joined, prose)
        self.assertNotIn('feature-state', prose)
        self.assertIn('control groups', prose)


if __name__ == '__main__': unittest.main()
