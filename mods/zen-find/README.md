# Zen Find · 0.2.0

**Keep search close to where you look.**

The native ⌘F / Ctrl+F bar becomes a floating card at the top right of each page pane. It includes a clear input focus, match count, previous/next actions, native filters, and a close button. It overlays the page without resizing it, with 14 px corners and a 160 ms entrance animation.

[Installation & updates](../../docs/INSTALLATION.md) · [All mods](../../README.md)

```sh
# Install or update the panel; preserve search preferences:
python3 scripts/install_local_mod.py --mod zen-find

# Optionally also apply match colors and enable Highlight All:
python3 scripts/install_local_mod.py --mod zen-find --with-highlights
```

Quit Zen before either command. Reopen a text page, press ⌘F / Ctrl+F, and search for a repeated word. `Enter` goes forward, `Shift+Enter` goes back, and `Escape` closes the panel.

## Match colors

The optional `--with-highlights` installer flag enables Highlight All and applies lavender to all matches and peach to the current match. Five native preferences are changed; their original values are saved. Ordinary mouse-selection colors are not modified.

**The CSS toggle does not reset these preferences.** With Zen closed, run:

```sh
python3 scripts/install_local_mod.py --mod zen-find --restore-highlights
```

Or choose **6** in `install.command`. If `user.js` owns any of these preferences, palette installation/restoration stops before writing; the panel-only option remains available. PDF viewers and site-owned search controls may render matches differently.

## Version 0.2

The input, previous/next controls, and close button share a 36 px row. Native filters form equal-width columns and collapse to one column in narrow panes. The match count has a separate footer. Input focus uses one inset ring rather than stacked border, outline, and shadow.

The existing match palette is unchanged. Use the panel-only command when updating to preserve your current preferences.

## Compatibility

Version 0.1.1 changes `grid-area` to `browserstack`: in the inspected native layout, absolute positioning still used the bottom findbar grid area's bounds and could place the panel outside the visible page. The correction is retained in 0.2.0; its layout, match count, and Enter / Shift+Enter navigation have been checked in native Zen on macOS.

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
