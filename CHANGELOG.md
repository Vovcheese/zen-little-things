# Changelog

Versions belong to individual mods. These entries describe local development packages; no marketplace release is implied.

## 2026-10-16 · Simpler installation

- One `install.command` menu replaces the separate install, update, and restore launchers. Use the same menu for first installation and updates.
- Find now preserves search preferences by default. Apply its optional palette with menu option 5 or `--with-highlights`; `--no-highlights` remains compatible.
- The local installer creates the profile's `chrome` folder when needed.
- Shortened the README, consolidated installation help, and moved maintainer publishing notes out of the user guide.

## 2026-10-16 · Peek 0.2.1

- Composite the preview background over an opaque system surface, including themes with translucent colors.
- Remove the whole-card fade; retain the thumbnail animation over a solid background.
- Verified the installed patch in native Zen on macOS: the light-theme text-only preview has an opaque background and a single frame. Thumbnail and dark-theme native checks remain pending.

## 2026-10-16 · Find and Peek 0.2.0

- **Find:** equal-height input and navigation controls, responsive filter columns, a separate match footer, and a single inset focus ring.
- **Peek:** one outer frame, a borderless thumbnail clipped once, current panel color variables, and a fade without inner-frame scaling.
- Added a native demo page and a generated HTML layout fixture; fixture checks do not replace native Zen validation.
- Added `update-ui.command` to update both CSS packages without changing search preferences.

## 2026-10-16 · Public preview preparation

- Added English collection documentation, installation and contribution guides, publishing notes, and screenshot guidelines.
- Added MIT licensing for original project files and upstream fixture attribution.
- Added a labeled SVG design overview; native screenshot coverage remains pending.

### Zen Folders 0.2.0

- Replaced nested group fills and boxes with individual heading surfaces.
- Separated the folder icon and expand arrow; aligned narrow tab hover insets.
- Kept one outer content guide and reserved the focus outline for keyboard focus.
- Checked an HTML geometry fixture; native Zen validation remains pending.

### Zen Find 0.1.1

- Anchored the floating find bar to `browserstack` instead of the bottom findbar grid area to address the invisible-panel layout problem.
- Added a panel-only update launcher that keeps search preferences unchanged.
- Native visual confirmation of the fix remains pending.

### Initial packages

- **Zen Peek 0.1.0:** native hover-preview styling and local registration.
- **Zen Find 0.1.0:** floating search panel and reversible match palette.
- **Zen Folders 0.1.0:** initial folder styling, superseded by 0.2.0.
