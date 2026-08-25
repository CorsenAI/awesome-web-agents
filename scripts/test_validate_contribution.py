# ABOUTME: Tests for the contribution policy validator used by the lint workflow.
# ABOUTME: Run with `python3 -m unittest discover -s scripts -p "test_*.py"`.

from __future__ import annotations

import unittest

from validate_contribution import REQUIRED_BODY_SECTIONS, extract_body_sections, normalize_section


BODY = """## Summary

Adds an item.

## Section

Dev Tools

## Why this belongs

It controls a browser.

## Primary documented web-agent use case

https://example.com/docs

## Public reference

https://example.com

## Affiliation disclosure

I maintain the project.

## Checklist

- [x] This PR adds exactly one item.
"""


class ExtractBodySectionsTest(unittest.TestCase):
    def test_reads_every_required_section(self) -> None:
        sections = extract_body_sections(BODY)
        for heading in REQUIRED_BODY_SECTIONS:
            self.assertTrue(sections.get(heading), f'missing "{heading}"')

    def test_reads_every_required_section_with_carriage_returns(self) -> None:
        # Some clients send the pull request body with CRLF line endings.
        sections = extract_body_sections(BODY.replace("\n", "\r\n"))
        for heading in REQUIRED_BODY_SECTIONS:
            self.assertTrue(sections.get(heading), f'missing "{heading}"')

    def test_section_name_has_no_carriage_return(self) -> None:
        sections = extract_body_sections(BODY.replace("\n", "\r\n"))
        self.assertEqual(normalize_section(sections["Section"]), "Dev Tools")

    def test_absent_section_is_not_reported(self) -> None:
        sections = extract_body_sections(BODY.replace("## Public reference", "## Other"))
        self.assertIsNone(sections.get("Public reference"))

    def test_empty_section_is_not_reported(self) -> None:
        sections = extract_body_sections(BODY.replace("https://example.com\n\n## Affiliation", "\n## Affiliation"))
        self.assertFalse(sections.get("Public reference"))


if __name__ == "__main__":
    unittest.main()
