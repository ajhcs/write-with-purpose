import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / 'analysis' / 'metrics.py'
spec = importlib.util.spec_from_file_location('metrics', PATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MetricsTests(unittest.TestCase):
    def test_clinical_abbreviations_decimals_and_citations(self):
        text = 'Dr. Lee et al. measured 3.5 mg, i.e. a dose. [12] Fig. 2 shows results. Next, A. Smith agreed.'
        self.assertEqual(m.split_sentences(text), [
            'Dr. Lee et al. measured 3.5 mg, i.e. a dose. [12]',
            'Fig. 2 shows results.', 'Next, A. Smith agreed.'
        ])
        self.assertIn('3.5', m.word_tokens(text))

    def test_reference_boundary_is_attached_and_does_not_create_sentence(self):
        self.assertEqual(m.split_sentences('The result held. [1, 2] Another finding followed. (3)'),
                         ['The result held. [1, 2]', 'Another finding followed. (3)'])

    def test_exact_separated_counts_and_sections(self):
        blocks = [
            {'kind': 'heading', 'text': 'Results', 'section_id': 'r1', 'heading_level': 1},
            {'kind': 'paragraph', 'text': 'One two. Three four five.', 'section_id': 'r1'},
            {'kind': 'list_item', 'text': 'do this now', 'section_id': 'r1'},
            {'kind': 'quote', 'text': 'quoted two', 'section_id': 'r1'},
            {'kind': 'code', 'text': 'run test', 'section_id': 'r1'},
            {'kind': 'caption', 'text': 'Figure one', 'section_id': 'r1'},
            {'kind': 'heading', 'text': 'Results', 'section_id': 'r2', 'heading_level': 2},
            {'kind': 'paragraph', 'text': 'Six seven eight.', 'section_id': 'r2'},
        ]
        result = m.measure_document(blocks, {'figures': None, 'tables': 0})
        self.assertEqual(result['prose_words'], 8)
        self.assertEqual(result['prose_paragraphs'], 2)
        self.assertEqual(result['estimated_sentences'], 3)
        self.assertEqual(result['paragraph_word_counts'], [5, 3])
        self.assertEqual(result['paragraph_sentence_counts'], [2, 1])
        self.assertEqual(result['sentence_word_counts'], [2, 3, 3])
        self.assertEqual(result['median_paragraph_words'], 4)
        self.assertEqual(result['median_sentence_words'], 3)
        self.assertEqual(result['section_words'], {'r1': 5, 'r2': 3})
        self.assertEqual(result['section_shares'], {'r1': 5/8, 'r2': 3/8})
        self.assertEqual([result[k] for k in ['list_words','quote_words','code_words','caption_words']], [3,2,2,2])
        self.assertEqual(result['headings'], 2)
        self.assertEqual(result['max_heading_depth'], 2)
        self.assertEqual(result['object_counts'], {'figures': None, 'tables': 0})

    def test_repeated_unnamed_headings_do_not_merge(self):
        blocks = [{'kind': 'heading', 'text': 'Discussion'}, {'kind': 'paragraph', 'text': 'First one.'},
                  {'kind': 'heading', 'text': 'Discussion'}, {'kind': 'paragraph', 'text': 'Second.'}]
        result = m.measure_document(blocks)
        self.assertEqual(list(result['section_words'].values()), [2, 1])
        self.assertEqual(len(result['section_words']), 2)
        self.assertAlmostEqual(sum(result['section_shares'].values()), 1.0)

    def test_empty_and_quartiles(self):
        result = m.measure_document([{'kind': 'paragraph', 'text': '  '}])
        self.assertEqual(result['prose_words'], 0)
        self.assertEqual(result['prose_paragraphs'], 0)
        self.assertIsNone(result['mean_word_characters'])
        self.assertIsNone(result['median_sentence_words'])
        self.assertEqual(result['section_shares'], {})
        self.assertEqual(m.summarize([]), {'min': None, 'q1': None, 'median': None, 'q3': None, 'max': None, 'n': 0})
        self.assertEqual(m.summarize([1, 2, 3, 4]), {'min': 1, 'q1': 1.75, 'median': 2.5, 'q3': 3.25, 'max': 4, 'n': 4})


if __name__ == '__main__':
    unittest.main()
