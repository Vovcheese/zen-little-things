# Zen Peek · 0.2.1

**Know which tab you are opening.**

A CSS treatment for Zen's native tab hover preview: a 320 px card, a title of up to three lines, a separate domain, and a larger thumbnail with its original aspect ratio. Rounded corners and an opaque card follow the browser theme. Only the thumbnail fades in over 160 ms; reduced motion disables this animation.

[Installation & updates](../../docs/INSTALLATION.md) · [All mods](../../README.md)

```sh
python3 scripts/install_local_mod.py --mod zen-peek
```

Enable `browser.tabs.hoverPreview.enabled` and `browser.tabs.hoverPreview.showThumbnails` in `about:config`. Quit Zen before installation, reopen it, and hover over another loaded tab.

## Version 0.2

The content surface draws one frame. The thumbnail canvas has no border and is clipped only by its wrapper, avoiding doubled rounded edges. Current and legacy panel color variables are supplied. Version 0.2.1 composites the theme background over an opaque system surface and removes the whole-card fade after a native transparency report. The thumbnail keeps its entrance animation.

## Behavior & limits

Zen owns the hover delay, panel position, tab switching, and screenshot capture. CSS cannot create a missing native preview or force an unloaded tab to provide a thumbnail. The thumbnail is a snapshot, not live video. Zen may reuse an open panel between tabs, so the entrance animation is not guaranteed to restart on every hover.

The selectors support the inspected current content wrapper and an older direct-child arrangement. On Zen 1.23.2b / Gecko 157.0.1 on macOS, the installed 0.2.1 text-only preview was visually checked in the light theme: its background is opaque, the frame is clean, and the native container indicator remains visible. Native thumbnail, dark-theme, and older-build checks remain pending. An HTML fixture checks both themes, a long title, and thumbnail/frame styling. Other mods targeting `#tab-preview-panel` may conflict.

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
