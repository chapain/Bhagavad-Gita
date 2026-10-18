#!/usr/bin/env python3
"""Lock the reviewed story maps and their one-verse, trilingual pearls.

Six verses is an editorial guideline, not a mechanical chopping rule. Longer
passages need an explicit reason below; a new exception must be reviewed.
This checker only reads source and built data, and never repairs either.
"""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = ROOT / 'source' / 'study_map_contract.json'
CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
APPROVED_MAPS = {int(ch): ranges for ch, ranges in CONTRACT['approved_maps'].items()}
LONG_THEME_EXCEPTIONS = {rng: (entry['verses'], entry['reason'])
                         for rng, entry in CONTRACT['long_theme_exceptions'].items()}
REVIEWED_TOTAL = sum(len(ranges) for ranges in APPROVED_MAPS.values())

# Advisory 1 allowlist: theme title deliberately equal to its part title.
# 2.19–2.21: the whole theme is that doctrine — 2.21 restates the same claim,
# so the theme name and the 2.19 pearl name are the same sentence on purpose.
SAME_TITLE_ALLOWED = {'2.19–2.21'}

# Advisory 2: a theme title may name a person only if the name (or a known
# alias for that person) appears in the theme's own EN text or, for a
# mid-speech continuation, in the verse immediately before the theme.
PERSON_NAMES = {
    'arjuna': ['arjuna', 'partha', 'son of kunti', 'kunti'],
    'krsna': ['krsna', 'krishna', 'bhagavan', 'blessed lord', 'madhusudana',
              'parantapa', 'kesava', 'janardana', 'hrisesikesa', 'prabhu'],
    'sanjaya': ['sanjaya'],
    'duryodhana': ['duryodhana'],
    'bhishma': ['bhishma', 'grandsire'],
    'dhritarashtra': ['dhritarashtra', 'blind king', 'o king', 'the king'],
    'drona': ['drona'],
    'karna': ['karna'],
}
PERSON_DISPLAY = {'arjuna': 'Arjuna', 'krsna': 'Kṛṣṇa', 'sanjaya': 'Sañjaya',
                  'duryodhana': 'Duryodhana', 'bhishma': 'Bhīṣma',
                  'dhritarashtra': 'Dhṛtarāṣṭra', 'drona': 'Droṇa',
                  'karna': 'Karṇa'}


def norm(s):
    """Lowercase and strip diacritics, so Kṛṣṇa == krsna for matching."""
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


def verse_text(source_verse):
    """Normalized EN working text of one verse: literals, paraphrase, speakers."""
    bits = [norm(source_verse['lits']['en']), norm(source_verse['paras']['en'])]
    for item in source_verse['flow']:
        if item.get('k') == 's':
            bits.append(norm(item['t']))
    return ' '.join(bits)


def load_book(root=ROOT):
    """Load the one-per-chapter source JSON and expose a review-friendly view.

    The audit's tuple representation is intentionally local to this checker;
    the repository stores each theme/part once, with all three language fields
    together in source/ch<N>.json.
    """
    root = Path(root)
    metadata, english, localized, built = [], {}, {"ne": {}, "hi": {}}, {}
    evidence = {}
    for ch in range(1, 19):
        source = json.loads((root / "source" / f"ch{ch}.json").read_text(encoding="utf-8"))
        raw = (root / "data" / f"ch{ch}.js").read_text(encoding="utf-8")
        built[ch] = json.loads(raw[raw.index("=") + 1:].rstrip().rstrip(";"))
        metadata.append((ch, source["names"]["en"], source["deva"],
                         source["verses"], source["subs"]["en"]))
        english[ch] = []
        localized["ne"][ch] = []
        localized["hi"][ch] = []
        # Per-verse evidence for the attribution advisory, in reading order,
        # so a theme opening mid-speech can draw on the speech it continues.
        verse_order = []
        for theme in source["themes"]:
            for part in theme["parts"]:
                sutra = part["sutras"][0]
                verse_order.append((part["range"].split("–")[0],
                                    verse_text(sutra),
                                    any(item.get('k') == 's' for item in sutra['flow'])))
        evidence[ch] = verse_order
        for theme in source["themes"]:
            rows = {lang: [] for lang in ("en", "ne", "hi")}
            for part in theme["parts"]:
                bounds = part["range"].split("–")
                if len(bounds) != 2:
                    raise ValueError(f"ch{ch}: malformed part range {part['range']!r}")
                for lang in rows:
                    rows[lang].append((part["titles"][lang], part["descs"][lang],
                                       bounds[0], bounds[1]))
            for lang, dest in (("en", english[ch]), ("ne", localized["ne"][ch]),
                               ("hi", localized["hi"][ch])):
                dest.append((theme["titles"][lang], theme["descs"][lang], rows[lang]))
    return metadata, english, localized, built, evidence


def audit(metadata, english, localized, built, evidence):
    errors, checks, advisories = [], 0, []
    titles, long_ranges = {}, set()

    def ok(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(label)

    ok(len(metadata) == 18 and [row[0] for row in metadata] == list(range(1, 19)),
       'chapter metadata must cover chapters 1–18 in order')
    ok(set(APPROVED_MAPS) == set(range(1, 19)), 'all 18 chapters require a reviewed map')
    ok(sum(len(ts) for ts in english.values()) == REVIEWED_TOTAL,
       f'the reviewed book has {REVIEWED_TOTAL} themes')
    for row in metadata:
        ch, count = row[0], row[3]
        themes = english[ch]
        payload = built[ch]
        ok(len(payload['themes']) == len(themes), f'chapter {ch}: built theme count differs from source')
        seen = [part[2] for _, _, parts in themes for part in parts]
        expected = [f'{ch}.{n:02d}' for n in range(1, count + 1)]
        ok(seen == expected, f'chapter {ch}: verse map has a gap, duplicate, or reordered verse')
        ranges = [f'{parts[0][2]}–{parts[-1][3]}' for _, _, parts in themes if parts]
        if ch in APPROVED_MAPS:
            ok(ranges == APPROVED_MAPS[ch], f'chapter {ch}: the reviewed story map changed')
        if ch == 2:
            ok(all(len(parts) <= 5 for _, _, parts in themes), 'chapter 2: each theme holds at most five verses')
        for lang in ('ne', 'hi'):
            ok(len(localized[lang].get(ch, [])) == len(themes), f'chapter {ch}: {lang} theme count differs')
        for ti, (title, desc, parts) in enumerate(themes):
            label = f'chapter {ch} theme {ti + 1}'
            ok(bool(parts), f'{label}: empty theme')
            if not parts:
                continue
            rng = f'{parts[0][2]}–{parts[-1][3]}'
            if len(parts) > 6:
                long_ranges.add(rng)
                exception = LONG_THEME_EXCEPTIONS.get(rng)
                ok(exception is not None and len(parts) == exception[0],
                   f'{rng}: more than six verses requires a reviewed exception')
            entries = {'en': (title, desc, parts)}
            for lang in ('ne', 'hi'):
                translations = localized[lang].get(ch, [])
                if ti < len(translations):
                    entries[lang] = translations[ti]
            generated = payload['themes'][ti] if ti < len(payload['themes']) else None
            for lang, (tt, td, ps) in entries.items():
                ok(bool(tt.strip()) and bool(td.strip()), f'{label}: missing {lang} title or description')
                ok([p[2:] for p in ps] == [p[2:] for p in parts], f'{label}: {lang} verse ranges are misaligned')
                if generated is not None:
                    ok(generated['titles'].get(lang) == tt and generated['descs'].get(lang) == td,
                       f'{label}: built {lang} teaching copy differs from source')
            if generated is not None:
                ok(generated['range'] == rng and len(generated['parts']) == len(parts),
                   f'{label}: built range or verse count differs from source')
            # Advisories (report-only, never fail the build): a theme title
            # lifted verbatim from one of its part titles, and a theme title
            # that names a person the verses — and the verse opening the
            # theme's speech — never name.
            verse_ids = [vid for vid, _text, _has in evidence.get(ch, [])]
            if parts[0][2] in verse_ids:
                i0 = verse_ids.index(parts[0][2])
                i1 = verse_ids.index(parts[-1][2]) + 1
                # Walk back through the continuation of the same speech to the
                # verse that opened it (a speaker item); the theme may name
                # whoever that speech belongs to.
                start = i0
                if i0 > 0:
                    start = i0 - 1
                    while start > 0 and not evidence[ch][start][2]:
                        start -= 1
                theme_text = ' '.join(evidence[ch][j][1] for j in range(start, i1))
                norm_title = norm(title)
                for part in parts:
                    if norm(part[0]) == norm_title and rng not in SAME_TITLE_ALLOWED:
                        advisories.append(f'{rng}: theme title lifts part title "{part[0]}"')
                        break
                for name, aliases in PERSON_NAMES.items():
                    if not re.search(rf'\b{re.escape(name)}\b', norm_title):
                        continue
                    if not any(alias in theme_text for alias in aliases):
                        advisories.append(f'{rng}: title names {PERSON_DISPLAY[name]}'
                                          ' but the theme and the verse before it never do')
            for pi, (pt, pd, start, end) in enumerate(parts):
                ok(start == end, f'{start}: a pearl must be exactly one verse')
                ok(bool(pt.strip()) and bool(pd.strip()), f'{start}: missing English title or description')
                ok(len(pt) <= 54, f'{start}: English verse title is too long for a card')
                ok(pt not in titles, f'{start}: duplicate English verse title with {titles.get(pt)}')
                titles[pt] = start
                generated_part = (generated['parts'][pi]
                                  if generated is not None and pi < len(generated['parts']) else None)
                if generated_part is not None:
                    ok([v['n'] for v in generated_part['sutras']] == [start]
                       and generated_part['range'] == f'{start}–{end}',
                       f'{start}: built verse ID or individual range changed')
                for lang, (_, _, ps) in entries.items():
                    if pi >= len(ps):
                        continue
                    lp = ps[pi]
                    ok(bool(lp[0].strip()) and bool(lp[1].strip()), f'{start}: missing {lang} verse copy')
                    if generated_part is not None:
                        ok(generated_part['titles'].get(lang) == lp[0]
                           and generated_part['descs'].get(lang) == lp[1],
                           f'{start}: built {lang} verse copy differs from source')
    ok(long_ranges == set(LONG_THEME_EXCEPTIONS), 'the reviewed longer passages changed')
    ok(len(titles) == 700, 'all 700 pearls must have distinct English titles')
    return errors, checks, advisories


def main():
    try:
        errors, checks, advisories = audit(*load_book())
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(f'study structure: FAILED — {exc}')
        return 1
    if errors:
        for error in errors:
            print('  ✗', error)
        print(f'study structure: {checks} checks, {len(errors)} failed')
        return 1
    # Advisories first, so the summary line stays the last line of output.
    for advisory in advisories:
        print(f'title advisory (report-only): {advisory}')
    print(f'study structure: {checks} checks passed — {REVIEWED_TOTAL} story themes, 700 pearls, three languages')
    if '--explain' in __import__('sys').argv:
        for rng, (count, reason) in LONG_THEME_EXCEPTIONS.items():
            print(f'  {rng} ({count} verses): {reason}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
