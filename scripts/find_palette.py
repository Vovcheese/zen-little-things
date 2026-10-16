"""Reversible changes to native find colors, applied only with Zen closed."""
import json
import re


def pref_pattern(name):
    return re.compile(
        rb'(?m)^[ \t]*user_pref\("' + re.escape(name.encode())
        + rb'"[ \t]*,[^\r\n]*\);[^\r\n]*(?:\r?\n|$)'
    )


def prepare_palette(profile, package, restore=False):
    prefs = profile / 'prefs.js'
    state_file = profile / 'zen-find-highlight-state.json'
    original = prefs.read_bytes() if prefs.exists() else b''
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    if restore:
        if not state.get('active'):
            return {}
        palette = state['palette']
    else:
        palette = json.loads((package / 'highlight-prefs.json').read_text())

    user_js = profile / 'user.js'
    if user_js.exists():
        for name in palette:
            if pref_pattern(name).search(user_js.read_bytes()):
                raise ValueError(f'Preference {name} is set in user.js. To install only the panel, use --no-highlights.')

    if not restore and not state.get('active'):
        state = {
            'active': True, 'palette': palette,
            'original': {name: [m.group().decode('utf-8') for m in pref_pattern(name).finditer(original)]
                         for name in palette},
        }
    updated = original
    for name, value in palette.items():
        updated = pref_pattern(name).sub(b'', updated)
        if restore:
            addition = ''.join(state['original'][name]).encode()
        else:
            addition = ('user_pref(' + json.dumps(name) + ', ' + json.dumps(value) + ');\n').encode()
        if addition:
            if updated and not updated.endswith(b'\n'):
                updated += b'\n'
            updated += addition
    state['active'] = not restore
    writes = {
        prefs: updated,
        state_file: (json.dumps(state, ensure_ascii=False, indent=2) + '\n').encode(),
    }
    return {path: data for path, data in writes.items()
            if not path.exists() or path.read_bytes() != data}
