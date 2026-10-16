# Installation & help

[← Zen Little Things](../README.md)

## Recommended: macOS installer

You need Zen Browser, Python 3.9 or later, and an extracted copy of this repository. Open Zen at least once so it has a profile, then quit it with **⌘Q**.

Open **`install.command`** in the repository folder. If Finder cannot open it, open Terminal in that folder and run:

```sh
zsh install.command
```

| Choose | Action |
| --- | --- |
| **1** | Install or update all three mods |
| **2** | Install or update Peek |
| **3** | Install or update Find |
| **4** | Install or update Folders |
| **5** | Install Find and apply optional match colors |
| **6** | Restore the previous search colors and Highlight All setting |
| **0** | Exit |

Options 1–4 change the styling only. Installation and updates use the same menu. Reopen Zen and find each installed mod in **Settings → Zen Mods**.

### Enable tab previews

For Peek, set these preferences to `true` in `about:config`:

```text
browser.tabs.hoverPreview.enabled
browser.tabs.hoverPreview.showThumbnails
```

Hover another loaded tab. Zen controls whether a thumbnail is available; selected or unloaded tabs may show text only.

### Optional search colors

Menu option **5** enables Highlight All and applies lavender to all matches and peach to the current match. It changes [five native preferences](../mods/zen-find/highlight-prefs.json) and saves their previous values.

Turning off the Find mod does not undo these preferences. To restore them, quit Zen and choose **6**. This leaves the Find panel installed. If `user.js` manages any of those preferences, the color operation stops; choose **3** for styling only.

### Update, disable, or remove

Download and extract the latest ZIP, quit Zen, and run the installer again. Your enabled/disabled mod switches are retained; search settings change only when you choose option 5 or 6. Local mods do not update automatically.

Use **Settings → Zen Mods** to disable or remove a mod. Restart Zen if needed. Remove any custom CSS overrides you added separately.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| Python is missing | Install Python 3.9+ and check `python3 --version` in Terminal. |
| Installer says Zen is running | Use **⌘Q**; closing the window does not quit the app. |
| Cannot determine a default profile | Use the manual route below for your chosen profile. The installer only handles one unambiguous default macOS profile. |
| Mod is missing from Settings | Check the installer output and the active profile in `about:support`. Manual CSS does not create a Settings entry. |
| Styling did not change | Restart Zen, enable the mod, and check for another mod styling the same area. |
| No preview thumbnail | Enable both preferences above and hover a loaded, inactive tab. |
| Search is missing | Press ⌘F on an ordinary text page. Check that Zen Find 0.2.0 or newer is enabled. |
| Search colors remain after disabling Find | Quit Zen and choose **6** in the installer. |

Still stuck? [Open an issue](https://github.com/Vovcheese/zen-little-things/issues/new/choose) with your mod version, Zen version, OS, and the error or a screenshot using demo content.

## Manual CSS installation

For a non-default profile, or Windows/Linux, use this route. **Windows/Linux have not been validated.** This method does not add a Zen Mods entry or change search preferences. Do not combine it with a local registry install of the same mod.

1. In `about:config`, set `toolkit.legacyUserProfileCustomizations.stylesheets` to `true`. For Peek, also enable the two preview preferences above.
2. Open `about:support` → **Profile Folder** and create a `chrome` folder if needed.
3. Copy the desired mod's `chrome.css` into that folder with a unique name:

   | Source | Name in your `chrome` folder |
   | --- | --- |
   | `mods/zen-peek/chrome.css` | `zen-peek.css` |
   | `mods/zen-find/chrome.css` | `zen-find.css` |
   | `mods/zen-folders/chrome.css` | `zen-folders.css` |

4. Create or edit `chrome/userChrome.css`. Add only the imports for the mods you copied, before existing rules and `@namespace` (after `@charset`, if present):

   ```css
   @import url("zen-peek.css");
   @import url("zen-find.css");
   @import url("zen-folders.css");
   ```

5. Restart Zen completely. To update, replace the copied CSS; to remove, delete its import and copied file.

Browser debugging preferences are not required.

## Command-line options

Run these from the repository directory with Zen closed:

```sh
python3 scripts/install_local_mod.py --mod zen-peek
python3 scripts/install_local_mod.py --mod zen-find
python3 scripts/install_local_mod.py --mod zen-folders
```

Each line installs or updates one mod without changing search preferences. Find's colors are explicitly opt-in:

```sh
python3 scripts/install_local_mod.py --mod zen-find --with-highlights
python3 scripts/install_local_mod.py --mod zen-find --restore-highlights
```

To inspect planned changes without writing or quitting Zen, add `--dry-run`. The older `--no-highlights` option is still accepted and now matches the default.

## Files and backups

The installer reads the default profile from `~/Library/Application Support/zen/profiles.ini`. It creates `chrome` when needed and writes:

- Mod CSS and a README under `chrome/zen-themes/<mod-id>/`.
- A local entry in `zen-themes.json` and the combined `chrome/zen-themes.css` cache.
- Search preferences and their saved values only for the optional color operation.

Peek also removes its old standalone `zen-peek.css` import, if present, to prevent duplicate loading. Other styles are preserved.

Existing changed files are backed up to `<profile>/zen-mods-backups/<timestamp>/`. Each mod installation rolls back its own writes on failure. When installing all three, earlier successful mods remain installed if a later one fails; the menu reports them.

The local registry format was inspected in Zen 1.23.2b and can change in future versions. Store update checks may not recognize these local IDs. Exporting a mod list does not transfer its CSS files.
