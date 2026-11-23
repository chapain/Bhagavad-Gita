"""The artifact-drift guard must catch the PR #98 class, and never cry wolf.

PR #98 changed `शोभादैन` → `शोभा दिँदैन` and `शत्रुतापन` → `शत्रुतापक` in
`source/ch{2,4,7,9,10,18}.json` and regenerated `chapter/*/index.html`, but
never rebuilt `data/ch*.js`. Every test was green because the build regenerated
`data/` in the runner and tested that fresh copy; nothing compared it with what
was committed. A reader got शत्रुतापक on the static chapter page and
शत्रुतापन in the app.

These tests pin the guard's two jobs rather than its implementation:

1. a committed artifact that disagrees with the committed source is reported;
2. a clean commit, an uncommitted source edit, and a non-git directory are not.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(ROOT, "source", "check_artifact_drift.py")


def git(cwd, *args):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True,
                          text=True)


def run_guard(cwd):
    """Run the guard that lives INSIDE the fixture, so it inspects the fixture.

    Using the project's own source/check_artifact_drift.py here would make the
    guard resolve ROOT to the real repository and judge that instead — a bug
    this suite itself found the first time it ran.
    """
    guard = os.path.join(cwd, "source", "check_artifact_drift.py")
    p = subprocess.run([sys.executable, guard], cwd=cwd, capture_output=True,
                       text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


class ArtifactDriftGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="drift-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _fixture(self):
        """A tiny repo shaped like the project: source/ and data/."""
        src = os.path.join(self.tmp, "source")
        data = os.path.join(self.tmp, "data")
        os.makedirs(src)
        os.makedirs(data)
        shutil.copy(GUARD, os.path.join(src, "check_artifact_drift.py"))
        # The "artifact" is derived from the "source" the way build_gita.py
        # derives data/ch*.js: one text, copied out.
        with open(os.path.join(src, "ch2.json"), "w", encoding="utf-8") as f:
            json.dump({"ne": "हे शत्रुतापक!"}, f, ensure_ascii=False)
        self._rebuild()
        git(self.tmp, "init", "-q")
        git(self.tmp, "add", "-A")
        git(self.tmp, "-c", "user.email=t@t", "-c", "user.name=t",
            "commit", "-qm", "base")

    def _rebuild(self):
        """Regenerate data/ch2.js from source/ch2.json."""
        with open(os.path.join(self.tmp, "source", "ch2.json"), encoding="utf-8") as f:
            payload = json.load(f)
        with open(os.path.join(self.tmp, "data", "ch2.js"), "w", encoding="utf-8") as f:
            f.write("GITA_CH[2] = " + json.dumps(payload, ensure_ascii=False) + ";")

    # 1. The PR #98 shape: source fixed, artifact forgotten.
    def test_stale_committed_artifact_is_reported(self):
        self._fixture()
        with open(os.path.join(self.tmp, "source", "ch2.json"), "w", encoding="utf-8") as f:
            json.dump({"ne": "हे शत्रुतापक, सच्याइयो!"}, f, ensure_ascii=False)
        # Commit the source change but deliberately leave data/ch2.js stale.
        git(self.tmp, "add", "source")
        self.assertEqual(
            git(self.tmp, "-c", "user.email=t@t", "-c", "user.name=t",
                "commit", "-qm", "fix source only").returncode, 0)
        self._rebuild()                        # what the build would do
        code, out = run_guard(self.tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("data/ch2.js", out)
        self.assertIn("BEHIND", out)

    # 2. A commit that reproduces itself is clean.
    def test_consistent_commit_passes(self):
        self._fixture()
        self._rebuild()
        code, out = run_guard(self.tmp)
        self.assertEqual(code, 0, out)

    # 3. Work in progress must not be judged.
    def test_uncommitted_source_edit_is_skipped(self):
        self._fixture()
        with open(os.path.join(self.tmp, "source", "ch2.json"), "w", encoding="utf-8") as f:
            json.dump({"ne": "हे शत्रुतापक, फेरि!"}, f, ensure_ascii=False)
        code, out = run_guard(self.tmp)
        self.assertEqual(code, 0, out)
        self.assertIn("SKIPPED", out)

    # 4. Outside git there is nothing to compare against.
    def test_non_git_directory_is_skipped(self):
        self._fixture()
        shutil.rmtree(os.path.join(self.tmp, ".git"))
        code, out = run_guard(self.tmp)
        self.assertEqual(code, 0, out)
        self.assertIn("SKIPPED", out)


if __name__ == "__main__":
    unittest.main()
