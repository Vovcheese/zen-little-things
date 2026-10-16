<div align="center">

# Zen Little Things

**Small details. Clearer browsing.**

Three independent CSS mods for tab previews, page search, and sidebar folders in Zen Browser.

[Download](https://github.com/Vovcheese/zen-little-things/archive/refs/heads/main.zip) · [Explore the mods](#the-collection) · [Install](docs/INSTALLATION.md) · [Contribute](CONTRIBUTING.md) · [MIT license](LICENSE)

![Illustrated overview of Zen Peek, Zen Find, and Zen Folders](docs/assets/overview.svg)

*Design illustration, not a screenshot. Appearance depends on your Zen version and theme.*

</div>

## The collection

| Mod | What it changes | Version |
| --- | --- | --- |
| **[Zen Peek](mods/zen-peek/README.md)** | Readable tab previews with a larger thumbnail, multiline title, and gentle entrance animation. | `0.1.0` |
| **[Zen Find](mods/zen-find/README.md)** | A floating find bar at the top right, with optional lavender and peach match highlights. | `0.1.1` |
| **[Zen Folders](mods/zen-folders/README.md)** | Clear expand arrows, consistent row hovers, and a quiet guide for folder contents. | `0.2.0` |

Install one or combine all three. Each mod has its own toggle when installed locally into Zen Mods.

The styles build on native browser controls: Zen handles tab previews, searching, folder state, and drag-and-drop. There are no runtime scripts, external fonts, or network requests in the mod CSS. The optional installer uses Python's standard library.

## Get started

**macOS · Python 3.9+ · an existing Zen profile**

1. Download this repository using **Code → Download ZIP**, then extract it, or clone it.
2. In Zen, open `about:support` → **Profile Folder** and create a `chrome` folder inside it if needed. For Peek, enable both `browser.tabs.hoverPreview.enabled` and `browser.tabs.hoverPreview.showThumbnails` in `about:config`.
3. Quit Zen completely with **⌘Q**.
4. From the repository folder, run the installer for the mod you want:

   ```sh
   python3 scripts/install_local_mod.py --mod zen-peek
   python3 scripts/install_local_mod.py --mod zen-find
   python3 scripts/install_local_mod.py --mod zen-folders
   ```

   Each line installs one mod. Alternatively, double-click the matching `install-zen-*.command` file in Finder.

5. Reopen Zen → **Settings → Zen Mods**.

**Zen Find's standard installer also changes five search preferences**, including Highlight All and match colors. To install only its panel, add `--no-highlights`. Disabling the mod does not restore these preferences; use the restore command in the [installation guide](docs/INSTALLATION.md#restore-search-highlights).

The installer creates backups and preserves other registered mods. Local packages have no automatic updates: download the updated project and run the installer again.

**Windows / Linux:** the included installer is macOS-only. A [manual CSS route](docs/INSTALLATION.md#manual-css-installation) is documented, but has not been validated on those platforms.

## Compatibility & project status

This is an **experimental community project**, independent of the Zen Browser team. These packages are locally registered mods, not Zen Mods marketplace releases.

| Area | Current evidence |
| --- | --- |
| Reference build | Selectors inspected against Zen **1.23.2b / Gecko 157.0.1** on macOS. |
| Installer | Backup, registry merge, cache rebuild, repeat installation, and preference restoration checked with temporary profiles during development. |
| Peek | Native markup inspected; visual validation remains pending. |
| Find | Grid placement fix implemented; visual validation of the updated panel remains pending. |
| Folders | HTML fixture inspected in Chrome in light/dark themes and narrow/wide layouts. Native Zen validation of 0.2.0 remains pending. |
| Older Zen versions | Compatibility fallbacks exist where practical; no older release is claimed as tested. |

Native browser UI can change between releases. Use the [test matrix](CONTRIBUTING.md#visual-checks) when reporting compatibility; a fixture screenshot is not evidence that the real browser UI works.

## Make it yours

The mods use theme colors and expose a few CSS variables. Put overrides in `chrome/userChrome.css` with custom stylesheet loading enabled; for a manual install, place them after your imports.

```css
#tab-preview-panel {
  --zen-peek-width: 340px;
  --zen-peek-radius: 18px;
}

#tabbrowser-tabpanels findbar {
  --zen-find-width: 460px;
  --zen-find-radius: 14px;
}

#tabbrowser-tabs zen-folder {
  --zf-accent: #9874c4;
  --zf-radius: 8px;
}
```

## Help improve it

Bug reports are most useful with the mod version, Zen version, operating system, theme, installation method, and a small reproduction. Include a screenshot using demo content when possible.

See [Contributing](CONTRIBUTING.md) for implementation guidelines and [Screenshots](docs/SCREENSHOTS.md) for a repeatable capture setup. Changes are listed in the [changelog](CHANGELOG.md).

## License & credits

Original project code and documentation are available under the [MIT License](LICENSE), © 2026 v0vcheese.

Built for [Zen Browser](https://github.com/zen-browser/desktop). Locally generated test fixtures can contain Zen's native CSS and icons; those upstream assets retain their own license. See [third-party notes](THIRD_PARTY.md).
