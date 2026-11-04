"""The 700-row worksheet in docs/title-review.md must match the canonical data.

`docs/title-review.md` is a hand-documented snapshot produced by
`python3 source/audit_titles.py --markdown`, and a snapshot silently rots: edit
a title in `source/ch*.json` and the worksheet still claims to list all 700.
These checks make the snapshot honest — every row present, in order, with the
title and the verse literal that the canonical data actually holds.

They also pin the two promises the worksheet makes to the reader:

  * it never edits anything (it is a generated document, not a change to
    `source/ch*.json`);
  * its ⚑ marks are exactly the verse-level advisories the audit reports, no
    more and no fewer, so a tick list that looks shorter than the audit is a
    bug here rather than a quiet omission.

Repair by re-running the generator, never by editing the table by hand:

    python3 source/audit_titles.py --markdown > docs/title-review.md
"""
import io
import json
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "source"))

import audit_titles  # noqa: E402

SNAPSHOT = os.path.join(ROOT, "docs", "title-review.md")

# "| ⚑ | 2.47 | ..." or "|  | 2.47 | ..." — a verse row, flagged or not.
ROW = re.compile(r"^\| (⚑)? \| (\d+\.\d+) \|")


def snapshot_text():
    return io.open(SNAPSHOT, encoding="utf-8").read()


def rows():
    out = []
    for line in snapshot_text().splitlines():
        m = ROW.match(line)
        if m:
            cells = line.split("|")
            out.append((bool(m.group(1)), m.group(2), cells[3].strip(),
                        cells[4].strip()))
    return out


class TitleWorksheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = audit_titles.load()
        cls.expected = []
        for ch in cls.chapters:
            for theme in ch["themes"]:
                for part in theme["parts"]:
                    verse = part["sutras"][0]
                    cls.expected.append((verse["n"], part["titles"]["en"],
                                         verse["lits"]["en"]))
        cls.findings = audit_titles.audit()

    def test_every_verse_has_exactly_one_row(self):
        refs = [r[1] for r in rows()]
        self.assertEqual(len(refs), 700)
        self.assertEqual(len(set(refs)), 700)
        self.assertEqual(refs, [e[0] for e in self.expected])

    def test_titles_match_the_canonical_data(self):
        for (flag, ref, title, _lit), (eref, etitle, _elit) in zip(rows(), self.expected):
            self.assertEqual(ref, eref)
            self.assertEqual(title, etitle, "title differs at %s" % ref)

    def test_verse_literals_match_the_canonical_data(self):
        # A long literal is shown truncated with " …"; it must still be a
        # prefix of the real one, or the row is showing a different verse.
        for (flag, ref, _t, shown), (eref, _et, elit) in zip(rows(), self.expected):
            ok = shown == elit or (
                shown.endswith(" …")
                and elit.startswith(shown[:-2].rstrip()))
            self.assertTrue(ok, "literal differs at %s" % ref)

    def test_flags_are_exactly_the_verse_level_advisories(self):
        want = sorted(x["ref"] for x in self.findings
                      if x["ref"].partition(".")[2].isdigit())
        got = sorted(r[1] for r in rows() if r[0])
        self.assertEqual(got, want)

    def test_still_50_advisories_and_nothing_blocking(self):
        blocking = [x for x in self.findings if x["kind"] in audit_titles.STRICT]
        self.assertEqual(blocking, [])
        self.assertEqual(len(self.findings), 50)

    def test_every_chapter_appears_once_with_a_heading(self):
        heads = re.findall(r"^### Chapter (\d+) — ", snapshot_text(), re.M)
        self.assertEqual([int(h) for h in heads], list(range(1, 19)))

    def test_rows_carry_a_tick_block_for_each_of_the_three_verdicts(self):
        for line in snapshot_text().splitlines():
            if ROW.match(line):
                self.assertTrue(line.rstrip().endswith("| ☐ | ☐ | ☐ |"), line)

    def test_snapshot_is_the_generator_output_not_a_hand_edit(self):
        # The header dates the run, so compare everything except that line —
        # otherwise this test would fail on the first day after a regeneration.
        generated = audit_titles._worksheet(self.findings, self.chapters)

        def undated(text):
            # .rstrip() absorbs the trailing blank line print() adds; the
            # worksheet's own content is compared line for line.
            return [line for line in text.rstrip("\n").splitlines()
                    if not line.startswith("Snapshot of ")]

        self.assertEqual(undated(generated), undated(snapshot_text()))


if __name__ == "__main__":
    unittest.main()
