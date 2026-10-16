"""One entry point for local installation, updates, and optional search colors."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPTIONS = {
    '1': [('zen-peek', []), ('zen-find', []), ('zen-folders', [])],
    '2': [('zen-peek', [])],
    '3': [('zen-find', [])],
    '4': [('zen-folders', [])],
    '5': [('zen-find', ['--with-highlights'])],
    '6': [('zen-find', ['--restore-highlights'])],
}


def main():
    if sys.version_info < (3, 9):
        print('Python 3.9 or newer is required.')
        return 1
    if sys.platform != 'darwin':
        print('This installer supports macOS. For manual CSS installation, see docs/INSTALLATION.md.')
        return 1
    print('''
Zen Little Things
Install or update your mods

  1  All three mods
  2  Peek       Tab previews
  3  Find       Search at the top right
  4  Folders    Sidebar folder styling

  5  Find + optional match colors (also enables Highlight All)
  6  Restore previous match colors and Highlight All setting
  0  Exit

Options 1–4 keep your search preferences unchanged.
Quit Zen completely with Cmd+Q before continuing.
''')
    while True:
        try:
            choice = input('Choose 0–6: ').strip()
        except (EOFError, KeyboardInterrupt):
            print('\nCancelled. No new action started.')
            return 0
        if choice == '0':
            return 0
        if choice in OPTIONS:
            break
        print('Enter a number from 0 to 6.')
    completed = []
    for mod, flags in OPTIONS[choice]:
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/install_local_mod.py'), '--mod', mod, *flags])
        if result.returncode:
            print('\nStopped. Read the error above.')
            if completed:
                print('Already installed or updated: ' + ', '.join(completed))
            return result.returncode
        completed.append(mod)
    print('\nDone. Reopen Zen → Settings → Zen Mods.')
    if choice in ('1', '2'):
        print('For Peek, enable browser.tabs.hoverPreview.enabled and browser.tabs.hoverPreview.showThumbnails in about:config.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
