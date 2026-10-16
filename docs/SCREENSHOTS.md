# Screenshots and visual evidence

The README currently uses an original SVG illustration, explicitly labeled as such. It is not proof of native rendering. Add real captures only after the corresponding mod has been checked in Zen.

## Prepare a clean scene

Use a test profile or a workspace with demo tabs only. Pick a simple text page, a documentation page, and folders named Projects, Design, and Archive. Avoid account menus, personal tab titles, meeting windows, profile paths, and notifications.

Use the same window size, zoom, theme, and sidebar mode for a before/after pair. Capture at native display scale; do not stretch screenshots. Crop to the relevant browser area while retaining enough context to show where the control appears.

## Capture list

| Filename | What to show |
| --- | --- |
| `peek-dark.png` | Hover card on a loaded demo tab, including title, domain, and thumbnail. |
| `find-light.png` | Top-right native search panel with a query, count, controls, and visible page matches. |
| `folders-narrow-dark.png` | An open folder, a closed folder, a nested folder, and a selected tab. |
| `folders-wide-light.png` | The same hierarchy with names and indentation visible. |

Store reviewed images under `docs/assets/screenshots/`. Add a caption containing the mod version, Zen version, OS, theme, and capture date. State whether the image is native Zen UI, an HTML fixture, or an illustration.

For a short animation, show a single interaction in 3–6 seconds: a hover, search opening, or folder expand/collapse. A static image must still explain the feature.

## Before publishing

Check the whole image at full resolution for personal content and accidental overlays. Confirm that the displayed version matches the documentation. Do not present edited, generated, or fixture images as native screenshots. Do not reuse the local `sidebar.png` or `bad-sidebar.png` development captures in a release.
