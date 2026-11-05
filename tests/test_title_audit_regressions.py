"""Regression pins for the independent, chapter-order title audit."""
import contextlib
import io
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "source"))
from check_study_structure import TITLE_AUDIT_POINTER, main as study_structure_main


# The verdict ledger records the title at review and its proposed/applied
# replacement. Pin all three localized strings actually shipped in canonical
# JSON so later edits cannot silently undo a reviewed correction.
CORRECTED_TITLES = {
    "1.01–1.03": {
        "en": "Dhṛtarāṣṭra asks; Duryodhana surveys the Pāṇḍava ranks",
        "ne": "धृतराष्ट्रको प्रश्नपछि दुर्योधनले पाण्डव सेना नियाल्छन्",
        "hi": "धृतराष्ट्र के प्रश्न के बाद दुर्योधन पांडव सेना का निरीक्षण करते हैं",
    },
    "1.37": {
        "en": "We should not kill our own kin",
        "ne": "आफ्ना नातेदारलाई मार्नु हुँदैन",
        "hi": "अपने कुटुंबियों को नहीं मारना चाहिए",
    },
    "1.45–1.47": {
        "en": "A great sin, an unarmed death, and grief",
        "ne": "महापाप, निःशस्त्र मृत्यु र शोक",
        "hi": "महापाप, निहत्थी मृत्यु और शोक",
    },
    "2.04–2.06": {
        "en": "Arjuna cannot bring himself to fight",
        "ne": "अर्जुन युद्ध गर्न सक्नुहुन्न",
        "hi": "अर्जुन युद्ध नहीं कर पाते",
    },
    "2.22–2.25": {
        "en": "Bodies change; the Self remains untouched",
        "ne": "शरीर फेरिए पनि आत्मा अविकारी रहन्छ",
        "hi": "शरीर बदलते हैं, आत्मा अविकारी रहती है",
    },
    "2.60": {
        "en": "The mind following the senses loses its wisdom",
        "ne": "इन्द्रियको पछि लाग्ने मनले बुद्धि हराउँछ",
        "hi": "इन्द्रियों के पीछे चलने वाला मन बुद्धि हर लेता है",
    },
    "3.16": {
        "en": "Who does not follow the wheel lives in vain",
        "ne": "यो चक्र अनुसरण नगर्ने व्यर्थ बाँच्छ",
        "hi": "चक्र का अनुसरण न करने वाला व्यर्थ जीता है",
    },
    "3.32": {
        "en": "Those who find fault and do not follow are lost",
        "ne": "दोष देखेर पालन नगर्ने नष्ट हुन्छन्",
        "hi": "दोष निकालकर न मानने वाले नष्ट होते हैं",
    },
    "4.06–4.10": {
        "en": "Knowing the Lord’s divine birth and deeds brings freedom from rebirth",
        "ne": "प्रभुको दिव्य जन्म र कर्म जान्दा पुनर्जन्मबाट मुक्ति",
        "hi": "प्रभु के दिव्य जन्म और कर्म का ज्ञान पुनर्जन्म से मुक्ति देता है",
    },
    "5.17": {
        "en": "Intellect, self and refuge all in that",
        "ne": "बुद्धि, आत्मा र शरण सबै त्यसैमा",
        "hi": "बुद्धि, आत्मा और शरण सब उसी में",
    },
    "5.22": {
        "en": "Contact-born pleasures are wombs of pain",
        "ne": "संयोगजन्य भोग दुःखका योनि",
        "hi": "संयोगजन्य भोग दुःख की योनियाँ",
    },
    "6.29–6.32": {
        "en": "See one Self in all; share their joy and pain",
        "ne": "सबैमा एउटै आत्मा देख, सुख-दुःख आफ्नै मान",
        "hi": "सबमें एक आत्मा देखो, सुख-दुःख अपना जानो",
    },
    "7.01–7.03": {
        "en": "Hear knowledge and realization; few know me truly",
        "ne": "ज्ञान र विज्ञान सुन; मलाई यथार्थ जान्ने विरलै",
        "hi": "ज्ञान और विज्ञान सुनो; मुझे यथार्थ जानने वाले विरले",
    },
    "9.25": {
        "en": "Each reaches the object they worship",
        "ne": "जसलाई पुज्यो, त्यही पाउँछ",
        "hi": "जिसे पूजे, उसी को पाता है",
    },
    "9.30": {
        "en": "Even a grave sinner, if wholly devoted, is righteous",
        "ne": "एकनिष्ठ भक्त भए अति दुराचारी पनि साधु मानिन्छ",
        "hi": "अनन्य भक्त हो तो अति दुराचारी भी साधु माना जाए",
    },
    "9.32": {
        "en": "All who take refuge reach the supreme goal",
        "ne": "मेरो शरण लिने सबै परम गति पाउँछन्",
        "hi": "मेरी शरण लेने वाले सब परम गति पाते हैं",
    },
    "12.17–12.20": {
        "en": "Even-minded, faithful devotees are exceedingly dear",
        "ne": "समभावी, श्रद्धालु भक्त अत्यन्त प्रिय छन्",
        "hi": "समभावी और श्रद्धालु भक्त अत्यन्त प्रिय हैं",
    },
    "13.29–13.34": {
        "en": "Nature acts; the Self illumines all, discernment frees",
        "ne": "प्रकृतिले कर्म गर्छ; आत्मा सबैलाई प्रकाशित गर्छ, विवेकले मुक्ति दिन्छ",
        "hi": "प्रकृति कर्म करती है; आत्मा सबको प्रकाशित करता है, विवेक मुक्ति देता है",
    },
    "14.24": {
        "en": "Even in pleasure and pain; clod, stone and gold alike",
        "ne": "सुख-दुःख, माटो-ढुङ्गा-सुनमा समान",
        "hi": "सुख-दुःख, मिट्टी-पत्थर-सोने में समान",
    },
    "18.18–18.22": {
        "en": "Knowledge, action and agent under the three guṇas",
        "ne": "तीन गुणअनुसार ज्ञान, कर्म र कर्ता",
        "hi": "तीन गुणों के अनुसार ज्ञान, कर्म और कर्ता",
    },
    "18.72–18.73": {
        "en": "Arjuna has heard; doubt gone, he will act",
        "ne": "अर्जुनले सुने; संशय हट्यो, अब कर्म गर्नेछन्",
        "hi": "अर्जुन ने सुना; संशय मिटा, अब कर्म करेंगे",
    },
    "18.17": {
        "en": "Ego-free, he neither kills nor is bound",
        "ne": "अहङ्कारमुक्त, मारे पनि न मार्ने, न बाँधिने",
        "hi": "अहंकार-मुक्त, मारकर भी न मारता, न बँधता",
    },
}

ROW = re.compile(r"^\| (\d+\.\d{2})(?:–(\d+\.\d{2}))? \|")


def source_titles():
    """Map review IDs to current canonical title maps in Chapters 1–18."""
    out = {}
    for ch in range(1, 19):
        data = json.loads((ROOT / "source" / f"ch{ch}.json").read_text(encoding="utf-8"))
        for theme in data["themes"]:
            out[theme["range"]] = theme["titles"]
            for part in theme["parts"]:
                verse = part["sutras"][0]
                out[verse["n"]] = part["titles"]
    return out


class TitleAuditRegressionTests(unittest.TestCase):
    def test_corrected_canonical_titles_remain_pinned_in_all_languages(self):
        current = source_titles()
        self.assertEqual(len(CORRECTED_TITLES), 22)
        for ref, titles in CORRECTED_TITLES.items():
            with self.subTest(ref=ref):
                self.assertEqual(current.get(ref), titles)

    def test_ledger_covers_every_theme_and_verse_title_through_all_chapters(self):
        ledger = (ROOT / "docs" / "title-audit.md").read_text(encoding="utf-8")
        current_chapter = None
        section = None
        found = {"theme": {}, "verse": {}}
        for line in ledger.splitlines():
            heading = re.match(r"^## Chapter (\d+) — ", line)
            if heading:
                current_chapter = int(heading.group(1))
                section = None
                continue
            if line.startswith("### Themes —"):
                section = "theme"
                continue
            if line.startswith("### Verse titles —"):
                section = "verse"
                continue
            if current_chapter is None or current_chapter > 18 or section is None:
                continue
            match = ROW.match(line)
            if not match:
                continue
            start, end = match.groups()
            ref = f"{start}–{end}" if end else start
            found[section].setdefault(ref, []).append(line)

        expected = {"theme": {}, "verse": {}}
        for ch in range(1, 19):
            data = json.loads((ROOT / "source" / f"ch{ch}.json").read_text(encoding="utf-8"))
            for theme in data["themes"]:
                expected["theme"][theme["range"]] = theme["titles"]
                for part in theme["parts"]:
                    expected["verse"][part["sutras"][0]["n"]] = part["titles"]

        self.assertEqual(len(expected["theme"]), 169)
        self.assertEqual(len(expected["verse"]), 700)
        self.assertEqual(set(found["theme"]), set(expected["theme"]))
        self.assertEqual(set(found["verse"]), set(expected["verse"]))
        for kind in ("theme", "verse"):
            for ref, titles in expected[kind].items():
                with self.subTest(kind=kind, ref=ref):
                    rows = found[kind][ref]
                    self.assertEqual(len(rows), 1, rows)
                    for lang, title in titles.items():
                        self.assertIn(f"{lang}: {title}", rows[0])

    def test_project_records_requested_endpoint_and_scope(self):
        project = (ROOT / "PROJECT.md").read_text(encoding="utf-8")
        self.assertIn("169/169 themes and 700/700 verse titles** (869 title records)", project)
        self.assertIn("Twenty-two title records were corrected, always after the relevant verdict table: sixteen in Chapters 1–9, one each in Chapters 12–14, and three in Chapter 18", project)
        self.assertIn("The expanded independent title audit is complete", project)

    def test_study_structure_cli_prints_nonblocking_ledger_pointer(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = study_structure_main()
        self.assertEqual(status, 0)
        self.assertIn(TITLE_AUDIT_POINTER, output.getvalue())
        self.assertIn("report-only", TITLE_AUDIT_POINTER)
        self.assertIn("docs/title-audit.md", TITLE_AUDIT_POINTER)
        self.assertIn("through Chapter 18", TITLE_AUDIT_POINTER)


if __name__ == "__main__":
    unittest.main()
