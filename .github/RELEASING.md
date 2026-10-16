# Maintainer release notes

## Prepare

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s tests -p 'test_*.py'
zsh -n install.command
git diff --check
git status --short
```

Keep native validation claims specific. See [testing status](../tests/README.md). Update changed mod versions and the changelog; installer-only changes do not need a CSS version bump. Root-level captures, logs, profile data, and generated fixtures must stay untracked.

## Publish to GitHub

From this repository, review the complete staged diff before committing:

```sh
git add -A
git diff --cached --stat
git diff --cached --check
git diff --cached
git commit -m "Simplify installation and polish Peek and Find"
git push origin main
```

The public repository is [Vovcheese/zen-little-things](https://github.com/Vovcheese/zen-little-things). Publishing to GitHub does not publish to the Zen Mods marketplace. Do not label the collection as stable or broadly compatible while the native test matrix remains incomplete.

## GitHub About

Description: `CSS mods for Zen Browser: readable tab previews, a floating search panel, and clearer sidebar folders.`

Topics: `zen-browser`, `zen-mods`, `userchrome`, `css`, `browser-customization`
