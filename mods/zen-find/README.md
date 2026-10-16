# Zen Find · 0.1.1

**Keep search close to where you look.**

The native ⌘F / Ctrl+F bar becomes a floating card at the top right of each page pane. It includes a clear input focus, match count, previous/next actions, native filters, and a close button. It overlays the page without resizing it, with 16 px corners and a 180 ms entrance animation.

[Installation & updates](../../docs/INSTALLATION.md) · [All mods](../../README.md)

```sh
# Panel and optional native search palette:
python3 scripts/install_local_mod.py --mod zen-find

# Panel only; keep existing search preferences:
python3 scripts/install_local_mod.py --mod zen-find --no-highlights
```

Quit Zen before either command. Reopen a text page, press ⌘F / Ctrl+F, and search for a repeated word. `Enter` goes forward, `Shift+Enter` goes back, and `Escape` closes the panel.

## Match colors

The standard installer enables Highlight All and applies lavender to all matches and peach to the current match. Five native preferences are changed; their original values are saved. Ordinary mouse-selection colors are not modified.

**The CSS toggle does not reset these preferences.** With Zen closed, run:

```sh
python3 scripts/install_local_mod.py --mod zen-find --restore-highlights
```

Or use `restore-zen-find-highlights.command`. If `user.js` owns any of these preferences, palette installation/restoration stops before writing; the panel-only option remains available. PDF viewers and site-owned search controls may render matches differently.

## Compatibility

Version 0.1.1 changes `grid-area` to `browserstack`: in the inspected native layout, absolute positioning still used the bottom findbar grid area's bounds and could place the panel outside the visible page. The correction is implemented but native visual confirmation remains pending.

Sources inspected: `findbar.js`, `findbar.css`, `tabbrowser/content-area.css`, and native highlighter preferences in Zen 1.23.2b. Older builds, Split View, fullscreen, and small windows still need visual validation. Other findbar mods may conflict.

## Customize

With custom stylesheets enabled, add to `userChrome.css`:

```css
#tabbrowser-tabpanels findbar {
  --zen-find-width: 460px;
  --zen-find-radius: 14px;
}
```

Check long queries, no matches, every native filter, keyboard navigation, both themes, reduced motion, and that the closed bar cannot intercept clicks.
