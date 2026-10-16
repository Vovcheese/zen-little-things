# Installation

[← Back to the collection](../README.md)

## Choose one method

| Method | Zen Mods toggle | Platform |
| --- | --- | --- |
| Local installer | Yes | macOS; uses the default profile from `profiles.ini` |
| Manual `userChrome.css` | No | Platform-independent procedure; Windows/Linux not validated |

Do not install the same CSS through both methods. A duplicate `@import` keeps the styling active even after its Zen Mods toggle is off.

## Local installer on macOS

You need Python **3.9 or later**, a downloaded copy of this repository, and an existing Zen profile. Run `python3 --version` to check Python. There are no pip dependencies.

1. Open Zen → `about:support` → **Profile Folder**. Create a folder named `chrome` inside that profile if it does not exist.
2. For **Zen Peek**, open `about:config` and set both `browser.tabs.hoverPreview.enabled` and `browser.tabs.hoverPreview.showThumbnails` to `true`.
3. Quit Zen using **⌘Q**. Closing a window is not enough.
4. Open Terminal in the extracted repository directory and run the command for your mod:

   | Mod | Command | Finder shortcut |
   | --- | --- | --- |
   | Peek | `python3 scripts/install_local_mod.py --mod zen-peek` | `install-zen-peek.command` |
   | Find + highlights | `python3 scripts/install_local_mod.py --mod zen-find` | `install-zen-find.command` |
   | Find panel only | `python3 scripts/install_local_mod.py --mod zen-find --no-highlights` | `update-zen-find.command` |
   | Folders | `python3 scripts/install_local_mod.py --mod zen-folders` | `install-zen-folders.command` |

5. Reopen Zen → **Settings → Zen Mods** and check the mod name and version.

Preview the planned file changes without writing or quitting Zen:

```sh
python3 scripts/install_local_mod.py --mod zen-folders --dry-run
python3 scripts/install_local_mod.py --mod zen-find --no-highlights --dry-run
```

The installer looks for a single default profile under `~/Library/Application Support/zen`. It stops if profile selection is ambiguous. It does not support selecting an arbitrary profile from the command line.

### What gets changed

- A local entry in `zen-themes.json` and files in `chrome/zen-themes/<mod-id>/`.
- `chrome/zen-themes.css`, rebuilt using all enabled registered mods.
- With Peek, a legacy standalone `@import url("zen-peek.css");` is removed from `userChrome.css` to avoid duplicate loading. Other CSS is preserved.
- With Find's standard install, five preferences and a record of their original values. See below.

Existing files that will change are backed up under `<profile>/zen-mods-backups/<timestamp>/`. A failed write triggers rollback of files already changed. The installer does not close Zen for you.

This uses Zen's internal local registry format, inspected in 1.23.2b. A future Zen update may change that format. Store update checks may report that these local IDs are not in the marketplace. Exporting the mod list does not transfer the local CSS files to another computer.

## Update or remove

To update, download the new project, quit Zen, and run the same installer again. The existing enabled/disabled state is retained. There is no automatic update service.

To disable or remove locally registered CSS, use the corresponding controls in **Settings → Zen Mods**, then restart if necessary. To remove a manual installation, delete its import and copied CSS file, then restart. Remove any custom variable overrides you added if you no longer need them.

Backups remain in the profile. Restoring a backup manually should be done with Zen closed and only for the files you intend to revert; an old full registry can also revert later changes to other mods.

## Restore search highlights

Find's default install sets `findbar.highlightAll` and four native match color preferences, listed in [`highlight-prefs.json`](../mods/zen-find/highlight-prefs.json). These are profile settings, separate from the CSS toggle.

With Zen closed, restore their saved values:

```sh
python3 scripts/install_local_mod.py --mod zen-find --restore-highlights
```

Or double-click `restore-zen-find-highlights.command`. This restores the values captured before the palette was first applied; it does not remove the Find CSS. Installing Find normally again reapplies the palette.

If one of these preferences is set in `user.js`, the palette operation stops before writing. Use `--no-highlights` to install only the panel. Ordinary mouse-selection colors are not changed by this package.

## Manual CSS installation

This method does not add a Zen Mods entry and does not apply Find's optional preference palette.

1. In `about:config`, set `toolkit.legacyUserProfileCustomizations.stylesheets` to `true`. For Peek, also enable the two hover-preview preferences above. Browser debugging preferences are not needed for installation.
2. Open the profile folder from `about:support` and create `chrome` if needed.
3. Copy your chosen `mods/<name>/chrome.css` into it with a unique filename: `zen-peek.css`, `zen-find.css`, or `zen-folders.css`.
4. Add only the corresponding imports to `chrome/userChrome.css`. Create the file if needed; preserve existing styles. Imports belong before normal rules and before `@namespace`, after `@charset` if present.

   ```css
   @import url("zen-peek.css");
   @import url("zen-find.css");
   @import url("zen-folders.css");
   ```

5. Restart Zen completely.

Zen documents the [profile folder and custom stylesheet workflow](https://docs.zen-browser.app/guides/live-editing). Its live-editing developer-tool setup is optional and is not required for these installation steps.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Mod missing from Settings | Manual CSS never creates an entry. For a local install, check the installer output and that Zen uses the selected default profile. |
| Nothing changed | Quit and reopen Zen. Check that the mod is enabled, the correct profile was used, and another mod does not override the same controls. |
| No preview image | Peek needs native hover previews and thumbnails enabled. A selected, unloaded, or uncaptured tab may have no image. |
| Find panel missing | Check that Find is at least 0.1.1. Open a normal text page and use ⌘F / Ctrl+F. Report the Zen build if the panel still does not appear. |
| Search colors remain after disabling Find | Restore the profile preferences using the command above. |
| Cannot determine profile | The installer requires exactly one default profile in the macOS Zen configuration. Use the manual CSS route for another profile. |
| Python or Finder launcher fails | Run the Python command in Terminal to see the error. Finder wrappers write a local `.log` file; remove personal paths before sharing it. |

When reporting a rendering problem, include which other mods style the same area and whether it reproduces with those mods disabled.
