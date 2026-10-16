"""Register a packaged mod in the native local Zen registry. No dependencies."""
from pathlib import Path
from datetime import datetime
import argparse
import configparser
import json
import os
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'mods/zen-peek'


def default_profile():
    base = Path.home() / 'Library/Application Support/zen'
    config = configparser.ConfigParser()
    config.read(base / 'profiles.ini')
    defaults = {config[s]['Default'] for s in config.sections()
                if s.startswith('Install') and config[s].get('Default')}
    if len(defaults) != 1:
        raise ValueError('Could not determine a single default Zen profile.')
    profile = Path(defaults.pop())
    return profile if profile.is_absolute() else base / profile


def without_legacy_import(data):
    # Match only standalone imports written by the earlier installer.
    # Preserve other bytes, including BOM, line endings and Catppuccin styles.
    bom = b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b''
    return bom + re.sub(
        rb'(?m)^[ \t]*@import[ \t]+url\([ \t]*["\x27]zen-peek\.css["\x27][ \t]*\);[ \t]*(?:\r?\n|$)',
        b'', data[len(bom):],
    )


def prepare(profile, package=PACKAGE):
    chrome = profile / 'chrome'
    if not chrome.is_dir():
        raise ValueError(f'Chrome folder not found: {chrome}')
    registry = profile / 'zen-themes.json'
    mods = json.loads(registry.read_text()) if registry.exists() else {}
    if not isinstance(mods, dict):
        raise ValueError('Invalid zen-themes.json; no changes made.')
    for key, item in mods.items():
        if (not isinstance(item, dict) or item.get('id') != key
                or not re.fullmatch(r'[A-Za-z0-9_-]+', key)):
            raise ValueError(f'Unknown registry format for mod {key}; no changes made.')

    metadata = json.loads((package / 'mod.json').read_text())
    mod_id = metadata['id']
    folder = chrome / 'zen-themes' / mod_id
    previous = mods.get(mod_id, {})
    if previous and previous.get('name') != metadata['name']:
        raise ValueError('This ID belongs to another mod; no changes made.')
    mods[mod_id] = {
        **previous, **metadata,
        'style': (folder / 'chrome.css').as_uri(),
        'readme': (folder / 'readme.md').as_uri(),
        'enabled': previous.get('enabled', True),
    }
    css = (package / 'chrome.css').read_bytes()
    readme = package / 'README.md'
    if not readme.exists():
        readme = ROOT / 'README.md'
    writes = {
        folder / 'chrome.css': css,
        folder / 'readme.md': readme.read_bytes(),
        registry: (json.dumps(mods, ensure_ascii=False, indent=2) + '\n').encode(),
    }
    user_css = chrome / 'userChrome.css'
    if package.name == 'zen-peek' and user_css.exists():
        writes[user_css] = without_legacy_import(user_css.read_bytes())

    # This build loads a cached stylesheet at startup. Rebuild it from all enabled
    # mods, as the native manager does. Read everything before any profile writes.
    chunks = [b'/* Zen Mods - local cache rebuilt by the local mod installer.\n'
              b' * Managed by Zen; changes will be overwritten. */\n']
    for item in mods.values():
        if item.get('enabled', True):
            mod_css = (css if item['id'] == mod_id else
                       (chrome / 'zen-themes' / item['id'] / 'chrome.css').read_bytes())
            chunks.extend([b'\n', mod_css, b'\n'])
    chunks.append(b'\n/* End of Zen Mods */\n')
    writes[chrome / 'zen-themes.css'] = b''.join(chunks)
    return {p: content for p, content in writes.items()
            if not p.exists() or p.read_bytes() != content}


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.zen-peek-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as output:
            output.write(content)
        if path.exists():
            shutil.copymode(path, temporary)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def install(profile, writes):
    if not writes:
        return None
    backup = profile / 'zen-mods-backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    originals = {p: p.read_bytes() if p.exists() else None for p in writes}
    for path, content in originals.items():
        if content is not None:
            target = backup / path.relative_to(profile)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    changed = []
    try:
        for path, content in writes.items():
            atomic_write(path, content)
            changed.append(path)
        for path, content in writes.items():
            if path.read_bytes() != content:
                raise OSError(f'Written file verification failed: {path}')
    except Exception:
        for path in reversed(changed):
            if originals[path] is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, originals[path])
        raise
    return backup if backup.exists() else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Show planned changes without writing')
    parser.add_argument('--mod', choices=['zen-peek', 'zen-find', 'zen-folders'], default='zen-peek')
    parser.add_argument('--no-highlights', action='store_true', help='Keep existing search highlight preferences')
    parser.add_argument('--restore-highlights', action='store_true', help='Restore search preferences saved before installing the Zen Find palette')
    args = parser.parse_args()
    try:
        if not args.dry_run:
            check = subprocess.run(['pgrep', '-ix', 'zen'], capture_output=True)
            if check.returncode == 0:
                raise ValueError('Quit Zen completely with Cmd+Q, then run the installer again.')
            if check.returncode != 1:
                raise ValueError('Could not check whether Zen is closed. Installation cancelled.')
        profile = default_profile().resolve()
        package = ROOT / 'mods' / args.mod
        metadata = json.loads((package / 'mod.json').read_text())
        if args.restore_highlights and args.mod != 'zen-find':
            raise ValueError('--restore-highlights requires --mod zen-find.')
        writes = {} if args.restore_highlights else prepare(profile, package)
        if args.mod == 'zen-find' and (args.restore_highlights or not args.no_highlights):
            from find_palette import prepare_palette
            writes.update(prepare_palette(profile, package, restore=args.restore_highlights))
        print('Profile:', profile)
        if args.dry_run:
            for path in writes:
                print('Will update:', path.relative_to(profile))
            print('Dry run complete. The profile was not changed.')
            return
        backup = install(profile, writes)
        if backup:
            print('Backup:', backup)
        if args.restore_highlights:
            print('Previous search preferences restored (or already restored). Reopen Zen.')
        else:
            print(f'\n{metadata["name"]} registered locally. Existing mods and styles were preserved.')
            print(f'Open Zen → Settings → Zen Mods. Look for {metadata["name"]} (v{metadata["version"]}).')
            if args.mod == 'zen-peek':
                print('Any legacy standalone import was removed; use the Zen Mods toggle to manage this mod.')
            elif args.mod == 'zen-find' and not args.no_highlights:
                print('Search palette applied. To restore: restore-zen-find-highlights.command.')
    except (OSError, ValueError, configparser.Error) as error:
        raise SystemExit(f'Error: {error}') from error


if __name__ == '__main__':
    main()
