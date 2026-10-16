"""Validate package metadata, local Markdown links, and Python syntax offline."""
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    docs = list(ROOT.glob('*.md'))
    for folder in ('docs', 'mods', 'tests', '.github'):
        docs.extend((ROOT / folder).rglob('*.md'))
    for path in docs:
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            target = target.split('#', 1)[0]
            if not target or re.match(r'[a-z]+:', target):
                continue
            if not (path.parent / unquote(target)).exists():
                errors.append(f'{path.relative_to(ROOT)}: missing link {target}')
    ids = set()
    for package in sorted((ROOT / 'mods').iterdir()):
        meta = json.loads((package / 'mod.json').read_text())
        if meta['id'] in ids:
            errors.append(f'{package.name}: duplicate mod ID')
        ids.add(meta['id'])
        if not re.fullmatch(r'\d+\.\d+\.\d+', meta['version']):
            errors.append(f'{package.name}: invalid version')
        for name in ('README.md', 'chrome.css'):
            if meta['version'] not in (package / name).read_text():
                errors.append(f'{package.name}/{name}: version does not match metadata')
    for folder in ('scripts', 'tests'):
        for path in (ROOT / folder).glob('*.py'):
            ast.parse(path.read_text(), filename=str(path))
    ET.parse(ROOT / 'docs/assets/overview.svg')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'OK: {len(docs)} Markdown files, 3 mod packages, Python syntax, and SVG.')


if __name__ == '__main__':
    main()
