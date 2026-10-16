# Zen Folders · 0.2.0

**A clearer home for your tabs.**

Readable folder rows for narrow and expanded sidebars. Version 0.2 replaces layered group boxes with a single surface per heading, a separate expand arrow, and a quiet guide for the contents.

[Installation & updates](../../docs/INSTALLATION.md) · [All mods](../../README.md)

```sh
python3 scripts/install_local_mod.py --mod zen-folders
```

Quit Zen, run the command, then reopen **Settings → Zen Mods**. Running it again updates an existing installation.

## The details

- Right-facing arrow when closed; down-facing arrow when open.
- A subtle heading tint and accent marker for open folders.
- Separate space for the icon and arrow, without the native skew extending into the arrow.
- Matching inset hover surfaces for folder headings and narrow-sidebar tabs.
- One guide per outer folder; nested folders do not stack parallel guide lines.
- Native labels and indentation in the wide sidebar, plus keyboard focus styling.
- A 140 ms arrow transition, disabled with reduced motion.

In the narrow sidebar, folder names remain in Zen's native tooltips. Expand the sidebar to read the complete hierarchy with names. Native collapse behavior, tab visibility, drag-and-drop, and custom folder icons remain browser-owned.

## Validation status

Selectors were inspected against Zen 1.23.2b on macOS. The HTML fixture was visually checked in Chrome with light/dark themes, narrow/wide layouts, and three levels of nesting. Seven headings stayed within the rail; narrow rows measured 48 × 40 px with a conservative 4 px icon-to-arrow gap.

The fixture approximates browser geometry. **Native Zen validation of 0.2.0 is still pending.** Older versions with a different folder structure are not claimed as tested; without `zen-folder`, these rules do not apply.

Build the optional fixture on a Mac with Zen installed at `/Applications/Zen.app`:

```sh
python3 tests/build_folders_preview.py
```

Open `tests/folders-preview.html`. Generated files include upstream native styles/icons and are excluded from Git; see [third-party notes](../../docs/THIRD_PARTY.md).

## Customize

With custom stylesheets enabled, add to `userChrome.css`:

```css
#tabbrowser-tabs zen-folder {
  --zf-accent: #9874c4;
  --zf-radius: 8px;
}
```
