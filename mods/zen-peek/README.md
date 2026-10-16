# Zen Peek · 0.1.0

**Know which tab you are opening.**

A CSS treatment for Zen's native tab hover preview: a 320 px card, a title of up to three lines, a separate domain, and a larger thumbnail with its original aspect ratio. Rounded corners and a 180 ms entrance animation follow the browser theme; reduced motion disables animation.

[Installation & updates](../../docs/INSTALLATION.md) · [All mods](../../README.md)

```sh
python3 scripts/install_local_mod.py --mod zen-peek
```

Enable `browser.tabs.hoverPreview.enabled` and `browser.tabs.hoverPreview.showThumbnails` in `about:config`. Quit Zen before installation, reopen it, and hover over another loaded tab.

## Behavior & limits

Zen owns the hover delay, panel position, tab switching, and screenshot capture. CSS cannot create a missing native preview or force an unloaded tab to provide a thumbnail. The thumbnail is a snapshot, not live video. Zen may reuse an open panel between tabs, so the entrance animation is not guaranteed to restart on every hover.

The selectors support the inspected current content wrapper and an older direct-child arrangement. Only Zen 1.23.2b / Gecko 157.0.1 markup on macOS has been inspected; older builds and native visual behavior are not yet validated. Other mods targeting `#tab-preview-panel` may conflict.

## Customize

With custom stylesheets enabled, add to `userChrome.css` after any imports:

```css
#tab-preview-panel {
  --zen-peek-width: 340px;
  --zen-peek-radius: 18px;
  --zen-peek-duration: 160ms;
}
```

Check long titles, missing thumbnails, pinned tabs, rapid hover changes, screen edges, both themes, and reduced motion. Keep native indicators and actions available.
