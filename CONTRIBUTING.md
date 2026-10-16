# Contributing

Thanks for helping make these small browser details better. Focused fixes, compatibility reports, and clear visual evidence are welcome.

## Report a problem

Use the bug-report template and include the mod/version, full Zen version, operating system, theme, sidebar mode, installation method, and reproduction steps. Tell us what happened and what you expected. Capture demo content and remove personal URLs or titles from logs and screenshots.

## Work on a mod

Each package lives in `mods/<name>/`:

- `chrome.css`: browser UI styling, scoped to the control it changes.
- `mod.json`: stable ID, name, author, version, dates, and tags.
- `README.md`: behavior, installation, customization, and validation status.
- Optional preference files must document every changed preference and its restore path.

Keep an existing mod's ID stable when updating it. For a new package, generate a new UUID and add it to the installer's `--mod` choices. New packages also need a launcher, documentation, and a catalog entry.

## Design and compatibility guidelines

1. Let Zen own visibility, input behavior, focus order, tab state, and drag-and-drop. Avoid replacing native controls with decorative imitations.
2. Scope selectors narrowly. A rule for folder headings must not restyle unrelated popups or generic tab groups.
3. Keep hit targets usable. Test icon, arrow, label, badge, hover, selected, and focus states together at the smallest supported width.
4. Use theme variables with sensible fallbacks. Check light, dark, high contrast, and forced colors where available.
5. Respect reduced motion. Animate short visual transitions rather than large layout shifts.
6. Preserve keyboard focus and native labels. Do not convey state through color alone.
7. Avoid fixed assumptions about private browser markup. Record the exact builds tested; do not equate a selector fallback with verified backward compatibility.
8. Keep runtime CSS free of remote assets and network dependencies.

## Visual checks

Record **pass**, **fail**, or **not tested** with the exact Zen build and OS. Review the actual browser UI before marking native validation complete.

| Mod | Required cases |
| --- | --- |
| All | Light/dark themes, narrow window, keyboard focus, reduced motion, enable/disable, coexistence with the other collection mods. |
| Peek | Loaded/unloaded tabs, long title, pinned tab, missing image, fast hover changes, screen edges. |
| Find | Open/close, matches/no matches, long query, Enter/Shift+Enter/Escape, native filters, small window, Split View, fullscreen. |
| Folders | Open/closed/hover/selected states, adjacent open folders, three nesting levels, narrow/wide sidebar, custom icon, drag-and-drop. |

The folder fixture helps catch geometry issues. It does not test the XUL browser shell, real drag-and-drop, or integration with other Zen components. Follow the [screenshot guide](docs/SCREENSHOTS.md) for review images.

## Installer changes

Use a temporary profile for write tests. Check that unrelated registry entries and CSS survive, disabled mods stay disabled, repeated installs are idempotent, failures roll back, and Find preferences restore correctly. Do not test a new write path against your only daily profile.

The installer has no third-party Python dependencies. Review its plan against an existing profile without writing:

```sh
python3 scripts/install_local_mod.py --mod zen-folders --dry-run
```

## Pull requests

Describe the visible problem and the resulting behavior. Include before/after captures for appearance changes and list exactly what you tested. Update the package version, its `updatedAt`, and `CHANGELOG.md` when shipping a behavior change. Keep unrelated refactors out of a small visual fix.

Original contributions are provided under this repository's MIT license. Retain attribution and original licensing for any upstream material; generated Zen fixture assets are not covered by the project's MIT grant.
