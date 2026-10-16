"""Strict structural validation for the canonical chapter JSON records.

This module is deliberately side-effect free: the builder calls it before it
indexes or renders any fields, and mutation tests can exercise malformed
records without running the full site generator.
"""

import re

LANGS = ("en", "ne", "hi")
CHAPTER_KEYS = {"num", "deva", "verses", "names", "subs", "themes", "colophon"}
THEME_KEYS = {"range", "titles", "descs", "parts"}
PART_KEYS = {"range", "titles", "descs", "sutras"}
VERSE_KEYS = {"n", "d", "t", "flow", "lits", "paras"}
FLOW_PAD_KEYS = {"k", "d", "t", "n", "words"}
FLOW_SPEAKER_KEYS = {"k", "d", "t", "words"}
RANGE_RE = re.compile(r"^(\d+)\.(\d{2})–(\d+)\.(\d{2})$")


def validate_chapters(chapters):
    """Return every schema error found in ``chapters``; return ``[]`` if valid.

    The validator checks exact keys and JSON types before descending, so a
    malformed record produces a useful path-based error instead of an
    incidental ``KeyError``/``AttributeError`` later in the build.
    """
    errors = []

    def fail(where, message):
        errors.append(f"{where}: {message}")

    def exact_object(value, keys, where):
        if not isinstance(value, dict):
            fail(where, f"must be an object, got {type(value).__name__}")
            return False
        actual = set(value)
        if actual != keys:
            missing = sorted(keys - actual)
            extra = sorted((str(key) for key in actual - keys))
            bits = []
            if missing:
                bits.append(f"missing {missing}")
            if extra:
                bits.append(f"unexpected {extra}")
            fail(where, "invalid keys (" + "; ".join(bits) + ")")
        return True

    def nonempty_text(value, where):
        if not isinstance(value, str) or not value.strip():
            fail(where, "must be a non-empty string")
            return False
        return True

    def language_map(value, where):
        if not isinstance(value, dict):
            fail(where, "must be an object with en/ne/hi strings")
            return False
        actual = set(value)
        expected = set(LANGS)
        if actual != expected:
            fail(where, f"must contain exactly en/ne/hi; got {sorted(map(str, actual))}")
        for lang in LANGS:
            if lang in value:
                nonempty_text(value[lang], f"{where}.{lang}")
        return True

    def verse_number(value, expected, where):
        if not isinstance(value, str):
            fail(where, "must be a verse id string")
            return None
        match = re.fullmatch(r"(\d+)\.(\d{2})", value)
        if not match:
            fail(where, f"must use a padded chapter.verse id (got {value!r})")
            return None
        chapter_num, verse_num = map(int, match.groups())
        canonical = f"{chapter_num}.{verse_num:02d}"
        if value != canonical:
            fail(where, f"must use canonical verse id {canonical}")
            return None
        if chapter_num != expected[0] or verse_num != expected[1]:
            fail(where, f"expected {expected[0]}.{expected[1]:02d}, got {value}")
        return chapter_num, verse_num

    def range_matches(value, ids, where, chapter_num):
        if not nonempty_text(value, where):
            return
        match = RANGE_RE.fullmatch(value)
        if not match:
            fail(where, f"must be a padded range joined by an en dash (got {value!r})")
            return
        if not ids:
            fail(where, "cannot describe an empty verse range")
            return
        start_ch, start_v, end_ch, end_v = map(int, match.groups())
        canonical = f"{start_ch}.{start_v:02d}–{end_ch}.{end_v:02d}"
        if value != canonical:
            fail(where, "must use unpadded chapter numbers and two-digit verses")
            return
        if (start_ch, start_v) != ids[0] or (end_ch, end_v) != ids[-1]:
            fail(where, f"must match contained verses {ids[0][0]}.{ids[0][1]:02d}–"
                        f"{ids[-1][0]}.{ids[-1][1]:02d}")
        if start_ch != chapter_num or end_ch != chapter_num:
            fail(where, f"must stay within chapter {chapter_num}")

    if not isinstance(chapters, list):
        return [f"chapters: must be an array, got {type(chapters).__name__}"]
    if len(chapters) != 18:
        fail("chapters", f"must contain exactly 18 records, got {len(chapters)}")

    total_verses = 0
    for expected_chapter, chapter in enumerate(chapters, 1):
        where = f"chapter {expected_chapter}"
        if not exact_object(chapter, CHAPTER_KEYS, where):
            continue

        number = chapter.get("num")
        if type(number) is not int or number != expected_chapter:
            fail(f"{where}.num", f"must be integer {expected_chapter}")
        chapter_num = expected_chapter

        declared_verses = chapter.get("verses")
        if type(declared_verses) is not int or declared_verses <= 0:
            fail(f"{where}.verses", "must be a positive integer")
            declared_verses = None
        nonempty_text(chapter.get("deva"), f"{where}.deva")
        language_map(chapter.get("names"), f"{where}.names")
        language_map(chapter.get("subs"), f"{where}.subs")

        colophon = chapter.get("colophon")
        if exact_object(colophon, {"deva", "iast"}, f"{where}.colophon"):
            nonempty_text(colophon.get("deva"), f"{where}.colophon.deva")
            nonempty_text(colophon.get("iast"), f"{where}.colophon.iast")

        themes = chapter.get("themes")
        if not isinstance(themes, list) or not themes:
            fail(f"{where}.themes", "must be a non-empty array")
            continue

        expected_verse = 1
        chapter_ids = []
        for ti, theme in enumerate(themes, 1):
            tw = f"{where} theme {ti}"
            if not exact_object(theme, THEME_KEYS, tw):
                continue
            language_map(theme.get("titles"), f"{tw}.titles")
            language_map(theme.get("descs"), f"{tw}.descs")
            parts = theme.get("parts")
            if not isinstance(parts, list) or not parts:
                fail(f"{tw}.parts", "must be a non-empty array")
                continue

            theme_ids = []
            for pi, part in enumerate(parts, 1):
                pw = f"{tw} part {pi}"
                if not exact_object(part, PART_KEYS, pw):
                    continue
                language_map(part.get("titles"), f"{pw}.titles")
                language_map(part.get("descs"), f"{pw}.descs")
                sutras = part.get("sutras")
                if not isinstance(sutras, list) or not sutras:
                    fail(f"{pw}.sutras", "must be a non-empty array")
                    continue
                if len(sutras) != 1:
                    fail(f"{pw}.sutras", f"must contain exactly one verse, got {len(sutras)}")

                part_ids = []
                for vi, verse in enumerate(sutras, 1):
                    vw = f"{pw} verse {vi}"
                    if not exact_object(verse, VERSE_KEYS, vw):
                        continue
                    verse_id = verse_number(verse.get("n"),
                                            (chapter_num, expected_verse), f"{vw}.n")
                    expected_verse += 1
                    if verse_id is not None:
                        part_ids.append(verse_id)
                        theme_ids.append(verse_id)
                        chapter_ids.append(verse_id)

                    nonempty_text(verse.get("d"), f"{vw}.d")
                    nonempty_text(verse.get("t"), f"{vw}.t")
                    language_map(verse.get("lits"), f"{vw}.lits")
                    language_map(verse.get("paras"), f"{vw}.paras")

                    flow = verse.get("flow")
                    if not isinstance(flow, list):
                        fail(f"{vw}.flow", "must be an array")
                        continue
                    pada_count = 0
                    speaker_count = 0
                    for fi, item in enumerate(flow, 1):
                        fw = f"{vw}.flow {fi}"
                        if not isinstance(item, dict):
                            fail(fw, f"must be an object, got {type(item).__name__}")
                            continue
                        kind = item.get("k")
                        if kind == "p":
                            pada_count += 1
                            exact_object(item, FLOW_PAD_KEYS, fw)
                            syllables = item.get("n")
                            if type(syllables) is not int or syllables <= 0:
                                fail(f"{fw}.n", "must be a positive integer")
                        elif kind == "s":
                            speaker_count += 1
                            exact_object(item, FLOW_SPEAKER_KEYS, fw)
                        else:
                            fail(f"{fw}.k", "must be 'p' (pāda) or 's' (speaker)")
                            exact_object(item, FLOW_PAD_KEYS | FLOW_SPEAKER_KEYS, fw)
                        nonempty_text(item.get("d"), f"{fw}.d")
                        nonempty_text(item.get("t"), f"{fw}.t")
                        words = item.get("words")
                        if not isinstance(words, list) or not words:
                            fail(f"{fw}.words", "must be a non-empty array")
                            continue
                        for wi, word in enumerate(words, 1):
                            ww = f"{fw}.words {wi}"
                            if not isinstance(word, list) or len(word) != 5:
                                fail(ww, "must be a five-string [deva, iast, en, ne, hi] row")
                                continue
                            for field, value in zip(("deva", "iast", "en", "ne", "hi"), word):
                                nonempty_text(value, f"{ww}.{field}")
                    if pada_count != 4:
                        fail(f"{vw}.flow", f"must contain exactly four pāda rows, got {pada_count}")
                    if speaker_count > 1:
                        fail(f"{vw}.flow", "may contain at most one speaker row")

                range_matches(part.get("range"), part_ids, f"{pw}.range", chapter_num)
            range_matches(theme.get("range"), theme_ids, f"{tw}.range", chapter_num)

        if declared_verses is not None and len(chapter_ids) != declared_verses:
            fail(f"{where}.verses", f"declares {declared_verses} but contains {len(chapter_ids)} verse records")
        total_verses += len(chapter_ids)

    if total_verses != 700:
        fail("chapters", f"must contain exactly 700 verse records, got {total_verses}")
    return errors
