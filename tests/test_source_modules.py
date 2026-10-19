"""Contracts for the feature-sized app source files.

The browser still receives one inline style and one inline script. These tests
protect the authoring boundary: every module must be explicitly ordered by the
builder, and an unlisted file must not silently disappear from the build.
"""
from __future__ import annotations

import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
BUILDER = SOURCE / "build_gita.py"


def builder_tuple(name: str) -> tuple[str, ...]:
    tree = ast.parse(BUILDER.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                value = ast.literal_eval(node.value)
                if not isinstance(value, tuple):
                    raise AssertionError(f"{name} must be an explicit tuple")
                return value
    raise AssertionError(f"{name} is not declared in source/build_gita.py")


class SourceModuleContractTests(unittest.TestCase):
    def check_family(self, folder: str, manifest: str, suffix: str, max_lines: int) -> str:
        names = builder_tuple(manifest)
        self.assertTrue(names)
        self.assertEqual(list(names), sorted(names), f"{manifest} must remain visibly ordered")
        actual = sorted(path.name for path in (SOURCE / folder).glob(f"*{suffix}"))
        self.assertEqual(list(names), actual, "every source module must be listed exactly once")
        chunks = []
        for name in names:
            text = (SOURCE / folder / name).read_text(encoding="utf-8")
            self.assertTrue(text, name)
            self.assertLessEqual(len(text.splitlines()), max_lines, f"{name} is becoming a new monolith")
            chunks.append(text)
        return "".join(chunks)

    def test_javascript_manifest_covers_feature_sources(self):
        js = self.check_family("js", "APP_JS_FILES", ".js", 700)
        self.assertEqual(js.count("__UI__"), 1)
        self.assertEqual(js.count("__LR_LEGACY_JSON__"), 1)
        self.assertEqual(js.count("__DATALOADER__"), 1)
        self.assertNotIn("\nimport ", js)
        self.assertNotIn("\nexport ", js)

    def test_css_manifest_covers_feature_sources(self):
        css = self.check_family("css", "APP_CSS_FILES", ".css", 450)
        self.assertEqual(css.count("__FONTS__"), 1)

    def test_feature_interfaces_are_explicit(self):
        js = self.check_family("js", "APP_JS_FILES", ".js", 700)
        for feature in ("library", "learn", "play", "drills", "views", "reader"):
            self.assertIn(f"App.{feature} = Object.freeze({{", js)

    def test_mutable_feature_state_has_one_owner(self):
        files = {path.name: path.read_text(encoding="utf-8")
                 for path in (SOURCE / "js").glob("*.js")}
        owners = {
            "10-library.js": ("VERSES", "FAV", "FAV_LIST", "SRCH_HITS"),
            "20-learn.js": ("LV", "FP", "lrTest", "lrOpen"),
            "30-play.js": ("PL",),
            "35-drills.js": ("LQ", "LQi", "LQmiss", "LQpick"),
        }
        import re
        for owner, names in owners.items():
            allowed = {owner}
            if owner == "20-learn.js":
                allowed.add("25-learn-session.js")
            for name in names:
                for filename, text in files.items():
                    if filename not in allowed:
                        self.assertIsNone(re.search(rf"\b{re.escape(name)}\b", text),
                                          f"{name} leaked from {owner} into {filename}")

    def test_retired_monoliths_stay_retired(self):
        self.assertFalse((SOURCE / "app.js").exists())
        self.assertFalse((SOURCE / "app.css").exists())


if __name__ == "__main__":
    unittest.main()
