"""Regression checks for speaker-line presentation in the reader and cards.

The collapsed whole-verse card (.m-whole-verse) renders a speaker as
`<span class="spk">` followed by sibling `<span class="spk-iast" lang="sa-Latn">`.
Historically `.m-whole-verse .spk` lacked `display:block` and painted
`border-bottom:1px dashed var(--line); padding-bottom:8px;`, which dropped a
dashed line onto the first line of the verse below, while `.m-whole-verse .spk
.iast` never matched the sibling `.spk-iast`.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rule_body(css: str, selector: str) -> str:
    match = re.search(rf"{re.escape(selector)}\s*\{{([^}}]*)\}}", css)
    if not match:
        raise AssertionError(f"CSS rule not found: {selector}")
    return match.group(1)


class SpeakerPresentationTests(unittest.TestCase):
    def test_whole_verse_speaker_is_unlined_block_with_sibling_iast(self):
        for rel in ("source/css/50-reader-shell.css", "index.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            spk = rule_body(text, ".m-whole-verse .spk")
            self.assertIn("display:block", spk, rel)
            self.assertIn("text-align:left", spk, rel)
            self.assertNotIn("border-bottom", spk, rel)
            self.assertNotIn("padding-bottom", spk, rel)
            self.assertNotIn("underline", spk, rel)

            spk_iast = rule_body(text, ".m-whole-verse .spk-iast")
            self.assertIn("display:block", spk_iast, rel)
            self.assertIn("text-align:left", spk_iast, rel)
            self.assertNotIn(".m-whole-verse .spk .iast", text, rel)

            mid = rule_body(text, ".m-whole-verse .spk:not(:first-child)")
            self.assertIn("margin-top:", mid, rel)

            self.assertRegex(
                text,
                r'html\[lang="ne"\]\s+\.m-whole-verse\s+\.spk,\s*'
                r'html\[lang="hi"\]\s+\.m-whole-verse\s+\.spk\s*\{[^}]*margin-bottom:',
                rel,
            )

    def test_expanded_speaker_has_no_underline(self):
        for rel in ("source/css/50-reader-shell.css", "index.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn(".m-verse .spk-main{", text, rel)

    def test_favorites_card_styles_speaker_and_iast(self):
        for rel in ("source/css/20-learn.css", "index.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn(".res-deva .spk{", text, rel)
            self.assertIn(".res-deva .spk-iast{", text, rel)

    def test_expanded_hint_precedes_top_speaker_and_grid(self):
        for rel in ("source/js/50-reader.js", "index.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            start = text.index("const padaGridHtml =")
            end = text.index("verseViewState =", start)
            block = text[start:end]
            hint = block.index('class="pada-meanings-hint"')
            spk = block.index("${spkHtml(topS)}")
            grid = block.index('class="pada-grid"')
            self.assertLess(hint, spk, rel)
            self.assertLess(spk, grid, rel)

    def test_mobile_stacked_pada_rows_stretch_full_width(self):
        for rel in ("source/css/60-responsive.css", "index.html"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertRegex(
                text,
                r"\.m-verse\s+\.pada-row\s*\{\s*flex-direction:column;\s*align-items:stretch;",
                rel,
            )


if __name__ == "__main__":
    unittest.main()
