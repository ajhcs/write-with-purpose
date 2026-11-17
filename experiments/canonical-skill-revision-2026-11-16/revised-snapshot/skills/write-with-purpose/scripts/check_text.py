#!/usr/bin/env python3
"""Read-only, standard-library advisory checks for a UTF-8 writing artifact.

Usage:
    python check_text.py ARTIFACT [--source SOURCE] [--contract CONTRACT_JSON]
                                 [--enforce-contract]

CONTRACT_JSON is a nonempty UTF-8 JSON object using any of these optional keys:
    {"protected_literals": [{"text": "literal span", "min_count": 1}],
     "max_words": 250, "max_growth_words": 0}
Word limits are nonnegative integers. Words are whitespace-separated tokens in
the entire raw artifact (including markup/code); an initial UTF-8 BOM is ignored.
max_growth_words requires --source and compares artifact words minus source words.
``min_count`` defaults to 1 and must be a positive integer. Counts are exact,
case-sensitive, non-overlapping occurrences in the entire raw decoded artifact,
including code and quoted examples. The checker never changes any file.

Prose scans exclude backtick/tilde fenced code, replacing every non-newline
character with a space to retain offsets. Duplicate paragraphs compare literal
blank-line-delimited nonheading blocks, including their whitespace and wrapping.
Markers and number/anchor scans additionally exclude matched inline backtick
code. A bracket marker immediately wrapped in matching single/double straight
or curly quotes is a quoted literal and is excluded from the marker check.
Other quoted passages and Markdown blockquotes are not inferred to be examples.

Anchors use a deliberately limited Markdown subset: simple inline [label](#id)
links and plain ASCII ATX headings (up to three leading spaces, 1-6 hashes).
Headings containing non-ASCII or possible inline markup/custom IDs make the
anchor check unavailable, rather than declaring links valid or broken. Slugs
lowercase ASCII, remove punctuation except hyphens/underscores, turn runs of
spaces/tabs into one hyphen, and suffix duplicate slugs -1, -2, etc. This is a
documented local convention, not a complete parser or renderer guarantee.
Reference links, HTML/custom anchors, Setext headings, and renderer-specific
slug rules are outside scope. Findings call out unmatched *supported* headings.

Number tokens use [0-9]+(?:[.,][0-9]+)*(?:[eE][+-]?[0-9]+)?. This is a lexical
multiset comparison, not arithmetic, equivalence, factual, or semantic analysis.
By default, exit 0 means assessment completed, including when findings exist.
With --enforce-contract, declared literal or word-limit violations exit 1; other
observations remain advisory. CLI, input, source or contract errors exit 2.
All outcomes emit structured JSON (except an explicit --help request).
Enforcement checks only declared mechanical constraints, never editorial quality.
"""

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


CHECKER_VERSION = "0.2.0"
CHECK_NAMES = (
    "duplicate_paragraphs",
    "unresolved_markers",
    "internal_markdown_anchors",
    "numeric_token_changes",
    "protected_literals",
    "word_limits",
)
NUMBER_PATTERN = r"[0-9]+(?:[.,][0-9]+)*(?:[eE][+-]?[0-9]+)?"
NUMBER_RE = re.compile(NUMBER_PATTERN)
MARKER_RE = re.compile(r"\[\[(?:TBD|TODO)\]\]|\[(?:TBD|TODO)\]")
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+(.*)|[ \t]*)$")
LINK_RE = re.compile(
    r"(?<!!)\[[^\]\r\n]*\]\([ \t]*"
    r"(?:<(?P<angle>\#[^>\s]*)>|(?P<bare>\#[^\s)]*))"
    r"[ \t]*(?:(?:\"[^\"\r\n]*\"|'[^'\r\n]*'|\([^()\r\n]*\))"
    r"[ \t]*)?\)"
)


class InputFailure(Exception):
    pass


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise InputFailure(message)


def blank_non_newlines(text):
    return re.sub(r"[^\r\n]", " ", text)


def mask_fenced_code(text):
    """Mask CommonMark-like backtick/tilde fences, retaining every offset."""
    if text.startswith("\ufeff"):
        # Keep the decoded BOM's width so a first-line heading/fence still parses.
        text = " " + text[1:]
    result = []
    fence_character = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if fence_character is not None:
            result.append(blank_non_newlines(line))
            close = re.match(r"^ {0,3}([`~]+)[ \t]*$", body)
            if (close and set(close.group(1)) == {fence_character}
                    and len(close.group(1)) >= fence_length):
                fence_character = None
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", body)
        if opening and not (opening.group(1)[0] == "`"
                            and "`" in opening.group(2)):
            fence_character = opening.group(1)[0]
            fence_length = len(opening.group(1))
            result.append(blank_non_newlines(line))
        else:
            result.append(line)
    return "".join(result)


def escaped_at(text, position):
    count = 0
    position -= 1
    while position >= 0 and text[position] == "\\":
        count += 1
        position -= 1
    return count % 2 == 1


def mask_inline_code(text):
    """Mask matched backtick runs; unmatched runs remain literal prose."""
    runs = list(re.finditer(r"`+", text))
    output = list(text)
    index = 0
    while index < len(runs):
        opening = runs[index]
        if escaped_at(text, opening.start()):
            index += 1
            continue
        closing_index = index + 1
        while closing_index < len(runs):
            closing = runs[closing_index]
            if len(closing.group()) == len(opening.group()):
                output[opening.start():closing.end()] = blank_non_newlines(
                    text[opening.start():closing.end()]
                )
                index = closing_index + 1
                break
            closing_index += 1
        else:
            index += 1
    return "".join(output)


class Locations:
    def __init__(self, path, text):
        self.path = path
        self.starts = [0] + [match.end() for match in
                             re.finditer(r"\r\n|\r|\n", text)]

    def at(self, offset):
        line_index = bisect_right(self.starts, offset) - 1
        return {"path": self.path, "line": line_index + 1,
                "column": offset - self.starts[line_index] + 1}


def observed(check, code, message, **details):
    return {"check": check, "category": "exact_observation", "code": code,
            "message": message, **details}


def review(check, code, message, **details):
    return {"check": check, "category": "review", "code": code,
            "message": message, **details}


def check_duplicates(text, locations):
    paragraphs = defaultdict(list)
    block_lines = []
    block_start = None
    offset = 0

    def flush():
        if block_lines:
            paragraph = "".join(block_lines).rstrip("\r\n")
            # Do not identify punctuation-only or entirely inline-code blocks
            # as prose. Comparison itself retains inline code and whitespace.
            if any(char.isalpha() for char in mask_inline_code(paragraph)):
                paragraphs[paragraph].append(locations.at(block_start))

    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        if not body.strip() or HEADING_RE.match(body):
            flush()
            block_lines = []
            block_start = None
        else:
            if block_start is None:
                block_start = offset
            block_lines.append(line)
        offset += len(line)
    flush()
    findings = []
    for paragraph, occurrences in paragraphs.items():
        if len(occurrences) > 1:
            findings.append(observed(
                "duplicate_paragraphs", "exact_duplicate_paragraph",
                "The same literal prose block occurs more than once; "
                "whether repetition is useful requires review.",
                text=paragraph, count=len(occurrences), locations=occurrences,
            ))
    return {"status": "evaluated", "paragraph_count": sum(
        len(items) for items in paragraphs.values()),
        "comparison": "literal text, including whitespace and line wrapping",
        "finding_count": len(findings)}, findings


def check_markers(text, locations):
    findings = []
    quoted_exclusions = 0
    quote_pairs = {'"': '"', "'": "'", "\u201c": "\u201d", "\u2018": "\u2019"}
    for match in MARKER_RE.finditer(text):
        before = text[match.start() - 1] if match.start() else ""
        after = text[match.end()] if match.end() < len(text) else ""
        if before in quote_pairs and quote_pairs[before] == after:
            quoted_exclusions += 1
            continue
        findings.append(observed(
            "unresolved_markers", "explicit_unresolved_marker",
            "An explicit bracketed unresolved marker appears outside code "
            "and is not immediately enclosed in matching literal quotes.",
            marker=match.group(), location=locations.at(match.start()),
        ))
    return {"status": "evaluated", "finding_count": len(findings),
            "quoted_literal_exclusions": quoted_exclusions}, findings


def check_anchors(fenced_text, inline_masked_text, locations):
    used_slugs = set()
    headings = []
    unsupported_headings = []
    offset = 0
    for line in fenced_text.splitlines(keepends=True):
        match = HEADING_RE.match(line.rstrip("\r\n"))
        if match:
            title = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(1) or "").strip()
            # Be conservative around inline markup and explicit/custom IDs.
            if (not title.isascii() or re.search(r"[\\`*_\[\]<>{}]", title)):
                unsupported_headings.append(locations.at(offset))
            else:
                slug = re.sub(r"[^a-z0-9_ \t-]", "", title.lower())
                slug = re.sub(r"[ \t]+", "-", slug)
                if not slug:
                    unsupported_headings.append(locations.at(offset))
                else:
                    base = slug
                    suffix = 1
                    while slug in used_slugs:
                        slug = base + "-" + str(suffix)
                        suffix += 1
                    used_slugs.add(slug)
                    headings.append({"slug": slug, "location": locations.at(offset)})
        offset += len(line)

    links = [match for match in LINK_RE.finditer(inline_masked_text)
             if not escaped_at(inline_masked_text, match.start())]
    details = {"heading_count": len(headings), "link_count": len(links),
               "heading_slugs": headings,
               "scope": "simple inline fragment links and plain ASCII ATX headings"}
    if unsupported_headings:
        return {"status": "unavailable", "finding_count": 0,
                "reason": "ATX heading syntax exceeds the documented ASCII subset; "
                          "links are not declared valid or broken.",
                "unsupported_heading_locations": unsupported_headings,
                **details}, []

    findings = []
    for match in links:
        destination = match.group("angle") or match.group("bare")
        if destination == "#":
            continue  # A bare fragment can target the top of the document.
        try:
            target = unquote(destination[1:], encoding="utf-8", errors="strict")
        except UnicodeDecodeError:
            target = None
        if target is None or not target.isascii():
            findings.append(review(
                "internal_markdown_anchors", "unsupported_internal_fragment",
                "The fragment exceeds the documented ASCII anchor subset; "
                "its destination is unverified.", destination=destination,
                location=locations.at(match.start()),
            ))
        elif target not in used_slugs:
            findings.append(observed(
                "internal_markdown_anchors", "unmatched_internal_anchor",
                "This internal fragment has no matching supported ASCII ATX "
                "heading slug. HTML/custom anchors and other Markdown syntax "
                "are outside this check's scope.", destination=destination,
                decoded_fragment=target, location=locations.at(match.start()),
            ))
    return {"status": "evaluated", "finding_count": len(findings),
            **details}, findings


def number_occurrences(text, locations):
    tokens = defaultdict(list)
    for match in NUMBER_RE.finditer(text):
        tokens[match.group()].append(locations.at(match.start()))
    return tokens


def check_numbers(text, locations, source_text, source_locations):
    current = number_occurrences(text, locations)
    previous = number_occurrences(source_text, source_locations)
    current_counts = Counter({token: len(items) for token, items in current.items()})
    previous_counts = Counter({token: len(items) for token, items in previous.items()})
    added = current_counts - previous_counts
    removed = previous_counts - current_counts
    findings = []
    if added or removed:
        def changes(counts, occurrences):
            return [{"token": token, "count": counts[token],
                     "locations": occurrences[token]} for token in sorted(counts)]

        findings.append(review(
            "numeric_token_changes", "numeric_token_multiset_changed",
            "The numeric-token multiset differs from the source. This lexical "
            "observation does not establish a factual or semantic error.",
            added=changes(added, current), removed=changes(removed, previous),
        ))
    return {"status": "evaluated", "finding_count": len(findings),
            "token_pattern": NUMBER_PATTERN,
            "input_token_count": sum(current_counts.values()),
            "source_token_count": sum(previous_counts.values()),
            "semantic_assessment": "NOT_ASSESSED"}, findings


def validate_contract(document):
    allowed = {"protected_literals", "max_words", "max_growth_words"}
    if not isinstance(document, dict) or not document or set(document) - allowed:
        raise InputFailure("Contract must be a nonempty object with only "
                           "protected_literals, max_words or max_growth_words.")
    for name in ("max_words", "max_growth_words"):
        if name in document and (type(document[name]) is not int or document[name] < 0):
            raise InputFailure("Contract %s must be a nonnegative integer." % name)
    entries = document.get("protected_literals", [])
    if not isinstance(entries, list):
        raise InputFailure("Contract 'protected_literals' must be an array.")
    for index, entry in enumerate(entries):
        if (not isinstance(entry, dict) or "text" not in entry
                or set(entry) - {"text", "min_count"}):
            raise InputFailure("Protected literal %d must contain 'text' and "
                               "optionally 'min_count' only." % index)
        if not isinstance(entry["text"], str) or not entry["text"]:
            raise InputFailure("Protected literal %d 'text' must be nonempty." % index)
        minimum = entry.get("min_count", 1)
        if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 1:
            raise InputFailure("Protected literal %d 'min_count' must be a "
                               "positive integer." % index)
    return document


def contract_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputFailure("Duplicate contract JSON key: %r." % key)
        result[key] = value
    return result


def check_literals(raw_text, entries):
    findings = []
    observations = []
    for index, entry in enumerate(entries):
        minimum = entry.get("min_count", 1)
        actual = raw_text.count(entry["text"])
        observation = {"contract_index": index, "text": entry["text"],
                       "min_count": minimum, "actual_count": actual}
        observations.append(observation)
        if actual < minimum:
            findings.append(observed(
                "protected_literals", "protected_literal_below_minimum",
                "An exact literal span occurs fewer times than the contract "
                "requires in the entire raw decoded artifact.", **observation,
            ))
    return {"status": "evaluated", "finding_count": len(findings),
            "counting": "case-sensitive, non-overlapping, entire raw decoded artifact",
            "literals": observations}, findings


def word_count(text):
    if text.startswith("\ufeff"):
        text = text[1:]
    return len(text.split())


def check_word_limits(raw_text, document, source_text):
    actual_words = word_count(raw_text)
    source_words = word_count(source_text) if source_text is not None else None
    observations, findings = [], []
    for name, actual in (("max_words", actual_words),
                         ("max_growth_words", actual_words - source_words
                          if source_words is not None else None)):
        if name not in document:
            continue
        if actual is None:
            raise InputFailure("max_growth_words requires a readable --source.")
        observation = {"constraint": name, "maximum": document[name],
                       "actual": actual, "exceeded": actual > document[name]}
        observations.append(observation)
        if observation["exceeded"]:
            findings.append(observed(
                "word_limits", "word_limit_exceeded",
                "The artifact exceeds a declared word limit.", **observation))
    return {"status": "evaluated", "finding_count": len(findings),
            "counting": "Whitespace-separated tokens in the entire raw decoded artifact; initial BOM excluded.",
            "artifact_words": actual_words, "source_words": source_words,
            "constraints": observations}, findings


def file_record(path=None, requested=False):
    return {"requested": requested, "path": str(path) if path is not None else None,
            "sha256": None, "status": "unavailable" if requested else "not_requested"}


def read_utf8(record, role, errors):
    try:
        raw = Path(record["path"]).read_bytes()
        record["sha256"] = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8")
        record["status"] = "loaded"
        return text
    except (OSError, UnicodeError, ValueError) as error:
        record["status"] = "unavailable"
        errors.append({"input": role, "type": type(error).__name__,
                       "message": str(error)})
        return None


def base_report():
    return {
        "checker": "write-with-purpose-advisory-text-checker",
        "checker_version": CHECKER_VERSION,
        "advisory": True,
        "contract_enforcement": {"requested": False, "status": "not_requested",
                                 "scope": "Declared literal and word-limit requirements only; all other findings remain advisory."},
        "result": "assessment_completed",
        "input": file_record(requested=True),
        "source": file_record(),
        "contract": file_record(),
        "checks": {name: {"status": "unavailable", "finding_count": 0}
                   for name in CHECK_NAMES},
        "findings": [],
        "errors": [],
        "assessment": {
            "conformance": {"status": "LIMITED",
                            "scope": "Only the explicit patterns, word limits and literal "
                                     "requirements listed in this report.",
                            "statement": "An evaluated check is not a pass, "
                                         "approval, or full conformance judgment."},
            "correctness": {"status": "NOT_ASSESSED"},
            "usefulness": {"status": "NOT_ASSESSED"},
        },
        "limitations": [
            "No factual, semantic, tone, style, authorship, or AI-style assessment.",
            "Prose blocks are blank-line-delimited nonheading text. Exact "
            "comparison preserves whitespace and wrapping; list/blockquote text "
            "can be included. Indented code and full Markdown grammar are not parsed.",
            "Fenced code is masked with spaces while retaining newlines and offsets. "
            "Marker, anchor-link, and numeric scans also mask matched inline backticks.",
            "Only [[TBD]], [[TODO]], [TBD], and [TODO] are markers. An immediately "
            "quote-wrapped marker is excluded; other quotation contexts are not inferred.",
            "Anchors cover simple inline fragment links and plain ASCII ATX headings. "
            "Slugs lowercase, remove punctuation except hyphen/underscore, collapse "
            "spaces/tabs to hyphens, and suffix collisions -1, -2, etc. No renderer "
            "guarantee, reference-link, Setext, HTML, or custom-anchor support.",
            "Numeric comparisons count lexical tokens, not numeric equivalence or meaning. "
            "Locations list all occurrences of changed tokens, not semantic alignments.",
            "Word limits count raw whitespace-separated tokens, including markup/code. A passing limit does not establish preserved meaning or suitable length.",
            "Contract literals use exact non-overlapping counts in the entire raw "
            "UTF-8 decoded artifact, including fenced code and quoted text.",
        ],
    }


def run(argv=None):
    report = base_report()
    parser = JsonArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("artifact", help="explicit path to a UTF-8 writing artifact")
    parser.add_argument("--source", help="optional UTF-8 source for numeric-token comparison")
    parser.add_argument("--contract", metavar="CONTRACT_JSON",
                        help="optional UTF-8 JSON contract for literals and word limits")
    parser.add_argument("--enforce-contract", action="store_true",
                        help="exit 1 when a declared literal or word limit is violated")
    try:
        args = parser.parse_args(argv)
        report["contract_enforcement"]["requested"] = args.enforce_contract
        if args.enforce_contract:
            report["advisory"] = False
            report["contract_enforcement"]["status"] = "unavailable"
            if args.contract is None:
                raise InputFailure("--enforce-contract requires --contract.")
    except InputFailure as error:
        report["result"] = "input_failure"
        report["errors"].append({"input": "cli", "type": "InputFailure",
                                 "message": str(error)})
        report["checks"]["numeric_token_changes"]["status"] = "not_requested"
        report["checks"]["protected_literals"]["status"] = "not_requested"
        return report, 2

    report["input"] = file_record(args.artifact, True)
    report["source"] = file_record(args.source, args.source is not None)
    report["contract"] = file_record(args.contract, args.contract is not None)
    raw_text = read_utf8(report["input"], "input", report["errors"])
    source_text = (read_utf8(report["source"], "source", report["errors"])
                   if args.source is not None else None)
    contract_text = (read_utf8(report["contract"], "contract", report["errors"])
                    if args.contract is not None else None)
    document = None
    if contract_text is not None:
        try:
            # JSON permits a UTF-8 BOM in many file workflows; hash remains raw.
            decoded_contract = contract_text[1:] if contract_text.startswith("\ufeff") else contract_text
            document = validate_contract(json.loads(decoded_contract,
                                                   object_pairs_hook=contract_object))
            if "max_growth_words" in document and args.source is None:
                raise InputFailure("max_growth_words requires --source.")
        except (ValueError, RecursionError, InputFailure) as error:
            document = None
            report["contract"]["status"] = "invalid"
            report["errors"].append({"input": "contract", "type": type(error).__name__,
                                     "message": str(error)})

    if args.source is None:
        report["checks"]["numeric_token_changes"] = {
            "status": "not_requested", "finding_count": 0}
    for name, keys in (("protected_literals", {"protected_literals"}),
                       ("word_limits", {"max_words", "max_growth_words"})):
        if args.contract is None or (document is not None and not keys.intersection(document)):
            report["checks"][name] = {"status": "not_requested", "finding_count": 0}

    def include(name, outcome):
        details, findings = outcome
        report["checks"][name] = details
        report["findings"].extend(findings)

    if raw_text is not None:
        locations = Locations(args.artifact, raw_text)
        fenced_text = mask_fenced_code(raw_text)
        prose_text = mask_inline_code(fenced_text)
        include("duplicate_paragraphs", check_duplicates(fenced_text, locations))
        include("unresolved_markers", check_markers(prose_text, locations))
        include("internal_markdown_anchors", check_anchors(
            fenced_text, prose_text, locations))
        if source_text is not None:
            source_prose = mask_inline_code(mask_fenced_code(source_text))
            include("numeric_token_changes", check_numbers(
                prose_text, locations, source_prose, Locations(args.source, source_text)))
        if document is not None:
            if "protected_literals" in document:
                include("protected_literals", check_literals(raw_text, document["protected_literals"]))
            if {"max_words", "max_growth_words"}.intersection(document):
                # A failed source read already contributes an input error; never claim
                # to have evaluated a relative limit without its source.
                if "max_growth_words" not in document or source_text is not None:
                    include("word_limits", check_word_limits(raw_text, document, source_text))

    if report["errors"]:
        report["result"] = "input_failure"
        return report, 2
    if args.enforce_contract:
        violated = [name for name in ("protected_literals", "word_limits")
                    if report["checks"][name]["finding_count"]]
        report["contract_enforcement"].update({
            "status": "failed" if violated else "passed", "violated_checks": violated})
        if violated:
            report["result"] = "contract_failed"
            return report, 1
    return report, 0


def main():
    report, exit_code = run()
    # ASCII escaping also makes JSON safe on legacy Windows console encodings.
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
