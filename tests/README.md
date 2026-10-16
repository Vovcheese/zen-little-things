# Testing status

These pages are development tools, not browser extensions. Fixtures approximate native XUL controls in HTML; they cannot certify native popup behavior, keyboard navigation, or drag-and-drop.

## Installer checks

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -p 'test_*.py'
zsh -n install.command
```

The six regression tests use temporary profiles. They cover first installation, creating `chrome`, preserving unrelated mods and disabled state, repeat installation, opt-in colors and restoration, styling-only updates, dry runs, rollback, and stopping the menu after a failed installation. These tests do not write to your real profile.

## Find and Peek

On macOS with Zen installed at `/Applications/Zen.app`:

```sh
python3 tests/build_ui_preview.py
```

Open the generated `ui-preview.html` in a browser. Use the controls to inspect both themes, a 300 px page pane, long titles and translated filter labels, no matches, a missing thumbnail, closed search, and RTL. **Check layout** measures button alignment, containment, overlap, and the preview frame/canvas borders.

The generator uses current package CSS. Regenerate after editing a mod. The generated HTML contains extracted upstream styles and is ignored by Git.

### Peek 0.2.1 regression check

In Chrome on macOS, the translucent-theme fixture retains an opaque base and a single frame in both light and dark color schemes. A text-only card stays opaque. The surface has no whole-card fade; only the thumbnail animates. This checks the CSS surface, not macOS popup compositing.

### 0.2.0 fixture observations

Checked in Chrome on macOS:

- Light and dark layouts: one preview frame, no canvas border.
- Wide and 300 px panes: input, previous, next, and close controls aligned at 36 px high; no overlap detected.
- Long page title: clamped to three lines, domain stays below it.
- Long translated filter labels: fit within a single-column narrow layout.
- No-match text and missing thumbnail: visible error feedback and a compact text-only preview.
- RTL narrow layout: mirrored controls remain contained and aligned.

Native Zen 1.23.2b on macOS: Find opens at the top right with aligned controls and a match footer; searching `ideas` shows 1 of 7 matches, Enter advances to 2 of 7, and Shift+Enter returns to 1 of 7. Filter toggles, no matches, Escape, small native windows, and Split View remain pending. Peek 0.2.0 received a native transparency report; the installed 0.2.1 CSS now matches the package and is enabled. A native light-theme text-only preview was observed over page content: the background is opaque, the frame is clean, and the native container indicator is visible. Thumbnail and dark-theme native checks remain pending. Reduced motion and forced-colors rules are present but were not exercised in the fixture run.

## Native browser check

After installing the current CSS and restarting Zen, open `ui-demo.html` as a regular browser tab. Search for `ideas` using ⌘F / Ctrl+F. Verify Enter/Shift+Enter, every native filter, no matches, Escape, and that a closed panel does not intercept input. Test a small window and Split View separately.

For Peek, keep the demo tab loaded, switch to another test tab, then hover the demo tab. Inspect the outer corners and thumbnail edge at native display scale. Verify a text-only preview and any native note/container controls you use.

## Folders

```sh
python3 tests/build_folders_preview.py
```

Open `folders-preview.html`. See the folder package README for its separate validation status.
