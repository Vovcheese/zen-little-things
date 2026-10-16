"""Installer regression checks. Every profile write stays in a temporary folder."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import install_local_mod as installer
import install_menu as menu


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.profile = Path(self.temp.name).resolve()
        self.original_prefs = b'user_pref("unrelated.setting", true);\nuser_pref("findbar.highlightAll", false);\n'
        (self.profile / 'prefs.js').write_bytes(self.original_prefs)

    def run_cli(self, *args):
        with patch.object(sys, 'argv', ['installer', *args]), \
             patch.object(sys, 'platform', 'darwin'), \
             patch.object(installer, 'default_profile', return_value=self.profile), \
             patch.object(installer.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1)), \
             contextlib.redirect_stdout(io.StringIO()):
            installer.main()

    def test_first_install_creates_chrome_and_keeps_preferences(self):
        self.run_cli('--mod', 'zen-find')
        self.assertTrue((self.profile / 'chrome/zen-themes.css').exists())
        self.assertEqual((self.profile / 'prefs.js').read_bytes(), self.original_prefs)
        self.assertFalse((self.profile / 'zen-find-highlight-state.json').exists())

    def test_update_preserves_other_mods_disabled_state_and_custom_css(self):
        chrome = self.profile / 'chrome'
        other = chrome / 'zen-themes/other-mod/chrome.css'
        other.parent.mkdir(parents=True)
        other.write_text('/* unrelated mod */')
        custom = b'/* custom */\n:root { --my-color: red; }\n'
        (chrome / 'userChrome.css').write_bytes(custom)
        package = installer.ROOT / 'mods/zen-peek'
        meta = json.loads((package / 'mod.json').read_text())
        registry = {'other-mod': {'id': 'other-mod', 'name': 'Other', 'enabled': True},
                    meta['id']: {**meta, 'enabled': False}}
        (self.profile / 'zen-themes.json').write_text(json.dumps(registry))
        self.run_cli('--mod', 'zen-peek')
        result = json.loads((self.profile / 'zen-themes.json').read_text())
        self.assertFalse(result[meta['id']]['enabled'])
        self.assertEqual(result['other-mod'], registry['other-mod'])
        self.assertEqual((chrome / 'userChrome.css').read_bytes(), custom)
        cache = (chrome / 'zen-themes.css').read_text()
        self.assertIn('/* unrelated mod */', cache)
        self.assertNotIn('Zen Peek 0.2.1', cache)
        self.assertEqual(installer.prepare(self.profile, package), {})

    def test_palette_opt_in_and_restore(self):
        self.run_cli('--mod', 'zen-find', '--with-highlights')
        applied = (self.profile / 'prefs.js').read_bytes()
        self.assertNotEqual(applied, self.original_prefs)
        self.run_cli('--mod', 'zen-find')
        self.assertEqual((self.profile / 'prefs.js').read_bytes(), applied)
        self.run_cli('--mod', 'zen-find', '--restore-highlights')
        self.assertEqual((self.profile / 'prefs.js').read_bytes(), self.original_prefs)

    def test_legacy_no_highlights_and_dry_run_write_nothing(self):
        self.run_cli('--mod', 'zen-find', '--no-highlights', '--dry-run')
        self.assertEqual(sorted(p.name for p in self.profile.iterdir()), ['prefs.js'])

    def test_mid_install_failure_restores_written_files(self):
        existing = self.profile / 'existing.css'
        existing.write_bytes(b'original')
        new = self.profile / 'new.css'
        atomic = installer.atomic_write
        def fail_second(path, data):
            if path == new:
                raise OSError('simulated write failure')
            atomic(path, data)
        with patch.object(installer, 'atomic_write', side_effect=fail_second):
            with self.assertRaises(OSError):
                installer.install(self.profile, {existing: b'changed', new: b'new'})
        self.assertEqual(existing.read_bytes(), b'original')
        self.assertFalse(new.exists())

    def test_menu_all_uses_style_only_and_stops_on_failure(self):
        with patch.object(sys, 'platform', 'darwin'), \
             patch('builtins.input', return_value='1'), \
             patch.object(menu.subprocess, 'run', side_effect=[subprocess.CompletedProcess([], 0), subprocess.CompletedProcess([], 1)]) as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(menu.main(), 1)
        self.assertEqual(run.call_count, 2)
        self.assertNotIn('--with-highlights', str(run.call_args_list))
        self.assertIn('Already installed or updated: zen-peek', output.getvalue())


if __name__ == '__main__':
    unittest.main()
