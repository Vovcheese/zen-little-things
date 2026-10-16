# Third-party notes

The original CSS, Python helpers, documentation, and SVG overview in this project use the repository's MIT license.

`tests/build_folders_preview.py` and `tests/build_ui_preview.py` extract native CSS and an SVG icon from the user's installed Zen application when run locally. The generated `tests/folders-preview.html` and `tests/ui-preview.html` contain that upstream material and is excluded from version control. The MIT license does not relicense the extracted assets.

Zen's native folder stylesheet contains a Mozilla Public License 2.0 notice, which the fixture generator preserves. Refer to [Zen Browser's source and license](https://github.com/zen-browser/desktop) for the applicable upstream terms and source. If redistributing a generated fixture, review and retain the upstream notices and license obligations.

Zen Browser and related names identify the software these mods customize. This is an independent community project and does not claim official endorsement.
