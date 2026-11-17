"""Deterministic descriptive measurements for normalized document blocks.

See ../method-note.md for scope, tokenization, and known limitations.
"""
from collections import Counter
import re

# Unicode letters/digits, allowing apostrophes and hyphens inside a word. A
# decimal is a single token; punctuation and standalone underscores are not.
_WORD = re.compile(r"[^\W_]+(?:[.'’\-][^\W_]+)*", re.UNICODE)
_ABBREVIATIONS = {
    'dr', 'mr', 'mrs', 'ms', 'prof', 'sr', 'jr', 'st', 'vs', 'etc',
    'fig', 'figs', 'eq', 'eqs', 'ref', 'refs', 'no', 'nos', 'vol',
    'inc', 'ltd', 'dept', 'approx', 'al', 'e.g', 'i.e', 'cf', 'p', 'pp',
}
_CITATIONS = re.compile(r"\s*(?:\[(?:\d+[\d,;\-– ]*)\]|\((?:\d+[\d,;\-– ]*)\))")


def word_tokens(text):
    """Return word-like tokens without altering case or original characters."""
    return _WORD.findall(text or '')


def split_sentences(text):
    """Split at terminal punctuation with conservative abbreviation handling."""
    text = (text or '').strip()
    if not text:
        return []
    result = []
    start = 0
    i = 0
    while i < len(text):
        if text[i] not in '.!?':
            i += 1
            continue
        if text[i] == '.':
            if i and i + 1 < len(text) and text[i-1].isdigit() and text[i+1].isdigit():
                i += 1
                continue
            # Acronyms and the internal periods of abbreviations such as i.e.
            if i + 2 < len(text) and text[i+1].isalpha() and text[i+2] == '.':
                i += 1
                continue
            match = re.search(r"([\w]+(?:\.[\w]+)*)$", text[start:i], re.UNICODE)
            last = match.group(1) if match else ''
            if last.lower() in _ABBREVIATIONS or (len(last) == 1 and last.isalpha()):
                i += 1
                continue
        end = i + 1
        while end < len(text) and text[end] in '.!?\"\'”’)]':
            end += 1
        # Numeric citation immediately after punctuation belongs with the sentence.
        while True:
            cite = _CITATIONS.match(text, end)
            if not cite:
                break
            end = cite.end()
        if end == len(text) or text[end].isspace():
            sentence = text[start:end].strip()
            if sentence:
                result.append(sentence)
            start = end
        i = end
    tail = text[start:].strip()
    if tail:
        result.append(tail)
    return result


def summarize(values):
    """Five-number summary with linearly interpolated quartiles (type 7)."""
    values = sorted(values)
    if not values:
        return dict(min=None, q1=None, median=None, q3=None, max=None, n=0)
    def quantile(p):
        position = (len(values) - 1) * p
        low = int(position)
        fraction = position - low
        return values[low] * (1 - fraction) + values[min(low + 1, len(values)-1)] * fraction
    return dict(min=values[0], q1=quantile(.25), median=quantile(.5),
                q3=quantile(.75), max=values[-1], n=len(values))


def measure_document(blocks, objects=None):
    """Measure ordered normalized blocks; parser supplies semantic boundaries."""
    paragraph_counts, paragraph_sentence_counts, sentence_counts, all_words = [], [], [], []
    section_words = {}
    heading_sequence = []
    other_counts = Counter()
    current_section = '__unsectioned__'
    max_depth = 0
    for index, block in enumerate(blocks):
        kind = block.get('kind', 'paragraph')
        content = block.get('text') or ''
        words = word_tokens(content)
        section = block.get('section_id')
        if kind == 'heading':
            current_section = str(section) if section is not None else f'heading-{index + 1}'
            level = block.get('heading_level')
            if isinstance(level, int) and not isinstance(level, bool):
                max_depth = max(max_depth, level)
            heading_sequence.append({'text': content, 'section_id': current_section, 'level': level})
        elif kind == 'paragraph':
            if not content.strip():
                continue
            key = str(section) if section is not None else current_section
            section_words[key] = section_words.get(key, 0) + len(words)
            paragraph_counts.append(len(words))
            all_words.extend(words)
            counts = [len(word_tokens(s)) for s in split_sentences(content) if word_tokens(s)]
            paragraph_sentence_counts.append(len(counts))
            sentence_counts.extend(counts)
        elif kind in ('list_item', 'code', 'quote', 'caption'):
            other_counts[kind] += len(words)
    total = len(all_words)
    return {
        'prose_words': total,
        'prose_paragraphs': len(paragraph_counts),
        'estimated_sentences': len(sentence_counts),
        'median_paragraph_words': summarize(paragraph_counts)['median'],
        'median_sentence_words': summarize(sentence_counts)['median'],
        'mean_word_characters': (sum(len(w) for w in all_words) / total if total else None),
        'headings': len(heading_sequence), 'max_heading_depth': max_depth,
        'list_words': other_counts['list_item'], 'code_words': other_counts['code'],
        'quote_words': other_counts['quote'], 'caption_words': other_counts['caption'],
        'paragraph_word_counts': paragraph_counts,
        'paragraph_sentence_counts': paragraph_sentence_counts, 'sentence_word_counts': sentence_counts,
        'section_words': section_words,
        'section_shares': {k: v / total for k, v in section_words.items()} if total else {},
        'heading_sequence': heading_sequence,
        'object_counts': dict(objects) if objects is not None else {},
    }
