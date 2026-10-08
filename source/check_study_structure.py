#!/usr/bin/env python3
"""Lock the reviewed story maps and their one-verse, trilingual pearls.

Six verses is an editorial guideline, not a mechanical chopping rule. Longer
passages need an explicit reason below; a new exception must be reviewed.
This checker only reads source and built data, and never repairs either.
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPROVED_MAPS = {
    1: ['1.01–1.03', '1.04–1.09', '1.10–1.11', '1.12–1.13', '1.14–1.19',
        '1.20–1.25', '1.26–1.30', '1.31–1.37', '1.38–1.44', '1.45–1.47'],
    2: ['2.01–2.03', '2.04–2.06', '2.07–2.10', '2.11–2.15', '2.16–2.18',
        '2.19–2.21', '2.22–2.25', '2.26–2.30', '2.31–2.34', '2.35–2.38',
        '2.39–2.41', '2.42–2.46', '2.47–2.50', '2.51–2.53', '2.54–2.58',
        '2.59–2.61', '2.62–2.63', '2.64–2.68', '2.69–2.72'],
    17: ['17.01–17.03', '17.04–17.04', '17.05–17.06', '17.07–17.07',
         '17.08–17.10', '17.11–17.13', '17.14–17.16', '17.17–17.19',
         '17.20–17.22', '17.23–17.27', '17.28–17.28'],
}
LONG_THEME_EXCEPTIONS = {
    '1.31–1.37': (7, "Arjuna's single argument that victory cannot justify killing his kin."),
    '1.38–1.44': (7, 'One causal argument: family destruction, lost dharma, and fallen ancestors.'),
    '6.37–6.43': (7, "Arjuna's question about the fallen yogi and Kṛṣṇa's reassuring answer."),
    '7.24–7.30': (7, 'The contrast between the veiled Lord and those who come to know him.'),
    '10.27–10.34': (8, 'A continuous catalogue of divine manifestations in beings and the world.'),
    '18.49–18.55': (7, 'One progression from renunciation through Brahman-realisation to devotion.'),
}


def literal_assignment(path, name):
    for node in ast.parse(Path(path).read_text(encoding='utf-8')).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f'{path}: missing {name}')


def load_book(root=ROOT):
    root = Path(root)
    metadata = literal_assignment(root / 'source/gita_data.py', 'CHAPTERS')
    english, localized, built = {}, {}, {}
    for ch in range(1, 19):
        suffix = '' if ch == 1 else str(ch)
        english[ch] = literal_assignment(root / 'source' / f'gita_data{suffix}.py', f'CH{ch}_THEMES')
        raw = (root / 'data' / f'ch{ch}.js').read_text(encoding='utf-8')
        built[ch] = json.loads(raw[raw.index('=') + 1:].rstrip().rstrip(';'))
    for lang in ('ne', 'hi'):
        localized[lang] = literal_assignment(root / 'source' / f'themes_{lang}.py', f'THEMES_{lang.upper()}')
    return metadata, english, localized, built


def audit(metadata, english, localized, built):
    errors, checks = [], 0
    titles, long_ranges = {}, set()

    def ok(condition, label):
        nonlocal checks
        checks += 1
        if not condition:
            errors.append(label)

    ok(len(metadata) == 18 and [row[0] for row in metadata] == list(range(1, 19)),
       'chapter metadata must cover chapters 1–18 in order')
    ok(sum(len(ts) for ts in english.values()) == 208, 'the reviewed book has 208 themes')
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
    return errors, checks


def main():
    try:
        errors, checks = audit(*load_book())
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(f'study structure: FAILED — {exc}')
        return 1
    if errors:
        for error in errors:
            print('  ✗', error)
        print(f'study structure: {checks} checks, {len(errors)} failed')
        return 1
    print(f'study structure: {checks} checks passed — 208 story themes, 700 pearls, three languages')
    if '--explain' in __import__('sys').argv:
        for rng, (count, reason) in LONG_THEME_EXCEPTIONS.items():
            print(f'  {rng} ({count} verses): {reason}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
