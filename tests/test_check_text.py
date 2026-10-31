"""Focused behavioral tests for the read-only advisory text checker.

Run from any directory:
    python -m unittest discover -s tests -v
Only temporary test files are created; the checker is invoked as a real CLI.
"""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = (Path(__file__).resolve().parents[1] / "skills" /
           "write-with-purpose" / "scripts" / "check_text.py")


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="write-purpose-checker-")
        self.directory = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def write(self, name, text):
        path = self.directory / name
        path.write_bytes(text.encode("utf-8"))
        return path

    def invoke(self, artifact=None, source=None, contract=None, extra=()):
        command = [sys.executable, str(CHECKER)]
        if artifact is not None:
            command.append(str(artifact))
        if source is not None:
            command += ["--source", str(source)]
        if contract is not None:
            command += ["--contract", str(contract)]
        command += list(extra)
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding="utf-8", check=False)
        self.assertEqual(result.stderr, "", result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["assessment"]["conformance"]["status"], "LIMITED")
        self.assertEqual(report["assessment"]["correctness"]["status"], "NOT_ASSESSED")
        self.assertEqual(report["assessment"]["usefulness"]["status"], "NOT_ASSESSED")
        self.assertEqual(report["checker_version"], "0.2.0")
        return result.returncode, report

    def findings(self, report, check):
        return [item for item in report["findings"] if item["check"] == check]

    def test_exact_duplicate_is_located_but_repeated_technical_word_is_not(self):
        artifact = self.write("draft.md", "API access is required.\n\n"
                              "The API returns a receipt.\n\n"
                              "Record the decision.\n\nRecord the decision.\n")
        before = artifact.read_bytes()
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        findings = self.findings(report, "duplicate_paragraphs")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["text"], "Record the decision.")
        self.assertEqual([item["line"] for item in findings[0]["locations"]], [5, 7])
        self.assertEqual(findings[0]["category"], "exact_observation")
        self.assertEqual(artifact.read_bytes(), before)

    def test_different_inline_code_does_not_create_false_duplicate(self):
        artifact = self.write("draft.md", "Use `alpha` here.\n\nUse `bravo` here.\n")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        self.assertEqual(self.findings(report, "duplicate_paragraphs"), [])

    def test_fenced_blocks_are_excluded_and_real_marker_line_is_preserved(self):
        artifact = self.write("draft.md", "# Draft\r\n\r\n```text\r\n"
                              "[[TODO]] 999\r\n\r\nCopied sentence.\r\n\r\n"
                              "Copied sentence.\r\n[bad](#missing)\r\n```\r\n"
                              "\r\nA real [[TBD]] remains.\r\n")
        source = self.write("source.md", "# Draft\n\nA real [[TBD]] remains.\n")
        code, report = self.invoke(artifact, source=source)
        self.assertEqual(code, 0)
        markers = self.findings(report, "unresolved_markers")
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0]["location"]["line"], 12)
        self.assertEqual(markers[0]["location"]["column"], 8)
        self.assertEqual(self.findings(report, "duplicate_paragraphs"), [])
        self.assertEqual(self.findings(report, "internal_markdown_anchors"), [])
        self.assertEqual(self.findings(report, "numeric_token_changes"), [])

    def test_tilde_and_unclosed_fences_are_excluded(self):
        artifact = self.write("draft.md", "~~~text\n[TODO]\n~~~\n\n"
                              "```\n[[TBD]]\n[bad](#no)\n")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        self.assertEqual(report["findings"], [])

    def test_utf8_bom_does_not_expose_first_fenced_block(self):
        artifact = self.write("draft.md", "\ufeff```text\n[TODO] 999\n```\n\nDone.\n")
        source = self.write("source.md", "Done.\n")
        code, report = self.invoke(artifact, source=source)
        self.assertEqual(code, 0)
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["input"]["sha256"], hashlib.sha256(artifact.read_bytes()).hexdigest())

    def test_markers_exclude_words_quoted_literals_and_inline_code(self):
        artifact = self.write("draft.md", "TODO and 'TBD' are ordinary words.\n"
                              "Use \"[TODO]\" or '\u005b\u005bTBD\u005d\u005d' as examples.\n"
                              "Also \u201c[TODO]\u201d and \u2018[[TBD]]\u2019.\n"
                              "Code `[TODO]` and ``[[TBD]]`` are examples.\n"
                              "Actual [TODO] and [[TBD]] remain.\n")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        markers = self.findings(report, "unresolved_markers")
        self.assertEqual([item["marker"] for item in markers], ["[TODO]", "[[TBD]]"])
        self.assertTrue(all(item["location"]["line"] == 5 for item in markers))
        self.assertEqual(report["checks"]["unresolved_markers"]["quoted_literal_exclusions"], 4)

    def test_real_internal_anchors_pass_and_fail_under_ascii_convention(self):
        artifact = self.write("draft.md", "# Project Scope\n\n"
                              "[good](#project-scope) [missing](#missing)\n"
                              "[remote](https://example.test/#missing)\n"
                              "[other](other.md#missing)\n"
                              "`[example](#missing)`\n\n"
                              "## Phase 2: Scope ##\n\n[phase](#phase-2-scope)\n")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        anchors = self.findings(report, "internal_markdown_anchors")
        self.assertEqual(len(anchors), 1)
        self.assertEqual(anchors[0]["destination"], "#missing")
        self.assertEqual(anchors[0]["location"]["line"], 3)
        self.assertEqual(anchors[0]["category"], "exact_observation")
        self.assertEqual(report["checks"]["internal_markdown_anchors"]["status"], "evaluated")

    def test_duplicate_heading_suffixes_and_top_fragment(self):
        artifact = self.write("draft.md", "# Scope\n\n# Scope\n\n"
                              "[first](#scope) [second](#scope-1) [top](#)\n")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        self.assertEqual(self.findings(report, "internal_markdown_anchors"), [])
        slugs = report["checks"]["internal_markdown_anchors"]["heading_slugs"]
        self.assertEqual([item["slug"] for item in slugs], ["scope", "scope-1"])

    def test_unsupported_heading_is_unavailable_and_not_a_false_pass(self):
        artifact = self.write("draft.md", "# R\u00e9sum\u00e9\n\n[link](#resume)\n")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        self.assertEqual(report["checks"]["internal_markdown_anchors"]["status"], "unavailable")
        self.assertEqual(self.findings(report, "internal_markdown_anchors"), [])

    def test_numeric_difference_is_only_a_review_observation_and_hashes_match(self):
        artifact = self.write("draft.md", "Target is 12; count is 2.\n")
        source = self.write("source.md", "Target is 10; count is 2.\n")
        code, report = self.invoke(artifact, source=source)
        self.assertEqual(code, 0)
        findings = self.findings(report, "numeric_token_changes")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["category"], "review")
        self.assertEqual([item["token"] for item in findings[0]["added"]], ["12"])
        self.assertEqual([item["token"] for item in findings[0]["removed"]], ["10"])
        self.assertEqual(report["checks"]["numeric_token_changes"]["semantic_assessment"], "NOT_ASSESSED")
        self.assertEqual(report["input"]["sha256"], hashlib.sha256(artifact.read_bytes()).hexdigest())
        self.assertEqual(report["source"]["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())

    def test_numeric_multiset_counts_and_formatting_are_lexical(self):
        artifact = self.write("draft.md", "Values: 1,000 and 7 and 7.\n")
        source = self.write("source.md", "Values: 1000 and 7.\n")
        code, report = self.invoke(artifact, source=source)
        self.assertEqual(code, 0)
        change = self.findings(report, "numeric_token_changes")[0]
        self.assertEqual({item["token"]: item["count"] for item in change["added"]},
                         {"1,000": 1, "7": 1})
        self.assertEqual({item["token"]: item["count"] for item in change["removed"]}, {"1000": 1})
        self.assertEqual(change["category"], "review")

    def test_equal_number_multiset_does_not_claim_semantic_preservation(self):
        artifact = self.write("draft.md", "9 patients and 123 doctors.\n")
        source = self.write("source.md", "123 patients and 9 doctors.\n")
        code, report = self.invoke(artifact, source=source)
        self.assertEqual(code, 0)
        self.assertEqual(self.findings(report, "numeric_token_changes"), [])
        self.assertEqual(report["checks"]["numeric_token_changes"]["status"], "evaluated")
        self.assertEqual(report["assessment"]["correctness"]["status"], "NOT_ASSESSED")

    def test_protected_literal_absent_is_exact_observation(self):
        artifact = self.write("draft.md", "Keep the project name.\n")
        contract = self.write("contract.json", json.dumps({"protected_literals": [
            {"text": "Project Cedar"}, {"text": "Keep", "min_count": 2}]}))
        code, report = self.invoke(artifact, contract=contract)
        self.assertEqual(code, 0)
        findings = self.findings(report, "protected_literals")
        self.assertEqual([item["actual_count"] for item in findings], [0, 1])
        self.assertTrue(all(item["category"] == "exact_observation" for item in findings))
        self.assertEqual(report["contract"]["sha256"], hashlib.sha256(contract.read_bytes()).hexdigest())

    def test_protected_literals_use_entire_raw_artifact(self):
        artifact = self.write("draft.md", "```\nProject Cedar\n```\n\n\"Project Cedar\"\n")
        contract = self.write("contract.json", json.dumps({"protected_literals": [
            {"text": "Project Cedar", "min_count": 2}]}))
        before = {path: path.read_bytes() for path in [artifact, contract]}
        code, report = self.invoke(artifact, contract=contract)
        self.assertEqual(code, 0)
        self.assertEqual(self.findings(report, "protected_literals"), [])
        self.assertEqual(report["checks"]["protected_literals"]["literals"][0]["actual_count"], 2)
        for path, original in before.items():
            self.assertEqual(path.read_bytes(), original)

    def test_malformed_contract_is_unavailable_with_exit_two(self):
        artifact = self.write("draft.md", "A paragraph.\n")
        for value in ["{bad json", '{"protected_literlas": []}',
                      '{"protected_literals": [{"text": "x", "min_count": true}]}',
                      '{"protected_literals": [{"text": "x", "min_count": 0}]}',
                      '{"protected_literals": [{"text": "x", "text": "y"}]}']:
            with self.subTest(value=value):
                contract = self.write("contract.json", value)
                code, report = self.invoke(artifact, contract=contract)
                self.assertEqual(code, 2)
                self.assertEqual(report["result"], "input_failure")
                self.assertEqual(report["checks"]["protected_literals"]["status"], "unavailable")
                self.assertEqual(report["contract"]["status"], "invalid")
                self.assertTrue(report["contract"]["sha256"])
                self.assertEqual(report["checks"]["duplicate_paragraphs"]["status"], "evaluated")

    def test_unreadable_source_is_unavailable_with_exit_two(self):
        artifact = self.write("draft.md", "A paragraph with 4.\n")
        code, report = self.invoke(artifact, source=self.directory / "missing-source.md")
        self.assertEqual(code, 2)
        self.assertEqual(report["checks"]["numeric_token_changes"]["status"], "unavailable")
        self.assertEqual(report["source"]["status"], "unavailable")
        self.assertIsNone(report["source"]["sha256"])
        self.assertEqual(report["checks"]["duplicate_paragraphs"]["status"], "evaluated")

    def test_missing_artifact_and_missing_cli_argument_return_structured_json(self):
        for artifact in [None, self.directory / "missing.md"]:
            with self.subTest(artifact=artifact):
                code, report = self.invoke(artifact)
                self.assertEqual(code, 2)
                self.assertEqual(report["result"], "input_failure")
                self.assertEqual(report["checks"]["duplicate_paragraphs"]["status"], "unavailable")

    def test_unrequested_optional_checks_are_not_requested(self):
        artifact = self.write("draft.md", "A paragraph.\n")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 0)
        for name in ["numeric_token_changes", "protected_literals"]:
            self.assertEqual(report["checks"][name]["status"], "not_requested")

    def test_empty_explicit_path_is_a_structured_input_failure(self):
        code, report = self.invoke("")
        self.assertEqual(code, 2)
        self.assertEqual(report["result"], "input_failure")
        self.assertEqual(report["checks"]["duplicate_paragraphs"]["status"], "unavailable")

    def test_invalid_utf8_retains_raw_hash_and_is_unavailable(self):
        artifact = self.directory / "draft.md"
        artifact.write_bytes(b"\xff")
        code, report = self.invoke(artifact)
        self.assertEqual(code, 2)
        self.assertEqual(report["input"]["sha256"], hashlib.sha256(b"\xff").hexdigest())
        self.assertEqual(report["checks"]["duplicate_paragraphs"]["status"], "unavailable")


    def test_word_ceiling_equality_and_failure_are_explicit(self):
        artifact = self.write("draft.md", "one two three")
        for maximum, enforce, expected_code in [(3, True, 0), (2, True, 1), (2, False, 0)]:
            with self.subTest(maximum=maximum, enforce=enforce):
                contract = self.write("contract.json", json.dumps({"max_words": maximum}))
                code, report = self.invoke(artifact, contract=contract,
                                          extra=("--enforce-contract",) if enforce else ())
                self.assertEqual(code, expected_code)
                self.assertEqual(report["checks"]["word_limits"]["artifact_words"], 3)
                self.assertEqual(report["checks"]["word_limits"]["finding_count"], int(maximum < 3))
                self.assertEqual(report["advisory"], not enforce)
                self.assertEqual(report["contract_enforcement"]["status"],
                                 ("passed" if maximum == 3 else "failed") if enforce else "not_requested")

    def test_no_growth_checks_the_source_and_allows_shorter_text(self):
        source = self.write("source.md", "one two three")
        contract = self.write("contract.json", '{"max_growth_words": 0}')
        for content, expected in [("one two", 0), ("one two three", 0), ("one two three four", 1)]:
            with self.subTest(content=content):
                artifact = self.write("draft.md", content)
                code, report = self.invoke(artifact, source, contract, ("--enforce-contract",))
                self.assertEqual(code, expected)
                self.assertEqual(report["checks"]["word_limits"]["source_words"], 3)
                self.assertEqual(report["checks"]["word_limits"]["constraints"][0]["actual"],
                                 len(content.split()) - 3)

    def test_both_word_limits_are_enforced(self):
        source = self.write("source.md", "one two")
        artifact = self.write("draft.md", "one two three four")
        contract = self.write("contract.json", '{"max_words": 3, "max_growth_words": 1}')
        code, report = self.invoke(artifact, source, contract, ("--enforce-contract",))
        self.assertEqual(code, 1)
        self.assertEqual(len(self.findings(report, "word_limits")), 2)

    def test_enforcement_without_contract_is_input_failure(self):
        artifact = self.write("draft.md", "Text.")
        code, report = self.invoke(artifact, extra=("--enforce-contract",))
        self.assertEqual(code, 2)
        self.assertEqual(report["contract_enforcement"]["status"], "unavailable")

    def test_missing_growth_source_cannot_pass(self):
        artifact = self.write("draft.md", "Text.")
        contract = self.write("contract.json", '{"max_growth_words": 0}')
        for source in [None, self.directory / "missing.md"]:
            with self.subTest(source=source):
                code, report = self.invoke(artifact, source, contract, ("--enforce-contract",))
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"]["word_limits"]["status"], "unavailable")
                self.assertEqual(report["contract_enforcement"]["status"], "unavailable")

    def test_invalid_word_limit_contracts_fail_closed(self):
        artifact = self.write("draft.md", "Text.")
        for value in [{}, {"max_word": 5}, {"max_words": True}, {"max_words": -1},
                      {"max_words": 1.5}, {"max_words": "5"}, {"max_growth_words": False},
                      {"max_growth_words": -1}, {"max_words": float("nan")}]:
            with self.subTest(value=value):
                contract = self.write("contract.json", json.dumps(value))
                code, report = self.invoke(artifact, contract=contract, extra=("--enforce-contract",))
                self.assertEqual(code, 2)
                self.assertEqual(report["contract"]["status"], "invalid")
                self.assertEqual(report["contract_enforcement"]["status"], "unavailable")
        contract = self.write("contract.json", '{"max_words": 1, "max_words": 100}')
        code, _ = self.invoke(artifact, contract=contract, extra=("--enforce-contract",))
        self.assertEqual(code, 2)

    def test_enforced_missing_literal_fails_even_within_word_limit(self):
        artifact = self.write("draft.md", "A short text.")
        contract = self.write("contract.json", json.dumps({"max_words": 10,
                              "protected_literals": [{"text": "Project Cedar"}]}))
        code, report = self.invoke(artifact, contract=contract, extra=("--enforce-contract",))
        self.assertEqual(code, 1)
        self.assertEqual(report["contract_enforcement"]["violated_checks"], ["protected_literals"])

    def test_noncontract_findings_remain_advisory_when_enforcing(self):
        artifact = self.write("draft.md", "The result is 8. [TODO]")
        source = self.write("source.md", "The result is 4.")
        contract = self.write("contract.json", '{"max_words": 20}')
        code, report = self.invoke(artifact, source, contract, ("--enforce-contract",))
        self.assertEqual(code, 0)
        self.assertTrue(self.findings(report, "numeric_token_changes"))
        self.assertTrue(self.findings(report, "unresolved_markers"))
        self.assertEqual(report["contract_enforcement"]["status"], "passed")

    def test_word_count_includes_markup_code_and_unicode_but_not_initial_bom(self):
        artifact = self.write("draft.md", "\ufeff# Title\n\n```text\né β\n```\n")
        contract = self.write("contract.json", '{"max_words": 6}')
        code, report = self.invoke(artifact, contract=contract, extra=("--enforce-contract",))
        self.assertEqual(code, 0)
        self.assertEqual(report["checks"]["word_limits"]["artifact_words"], 6)
        artifact = self.write("empty.md", "\ufeff  \n")
        contract = self.write("contract.json", '{"max_words": 0}')
        code, report = self.invoke(artifact, contract=contract, extra=("--enforce-contract",))
        self.assertEqual(code, 0)
        self.assertEqual(report["checks"]["word_limits"]["artifact_words"], 0)

    def test_contract_failure_preserves_all_input_bytes(self):
        artifact = self.write("draft.md", "one two three\r\n")
        source = self.write("source.md", "one two\r\n")
        contract = self.write("contract.json", '{"max_growth_words": 0}')
        before = {path: path.read_bytes() for path in self.directory.iterdir()}
        code, report = self.invoke(artifact, source, contract, ("--enforce-contract",))
        self.assertEqual(code, 1)
        self.assertEqual(report["result"], "contract_failed")
        self.assertEqual({path: path.read_bytes() for path in self.directory.iterdir()}, before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
