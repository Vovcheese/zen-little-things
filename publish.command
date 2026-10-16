#!/bin/zsh
# Publish the reviewed project files using the user's normal Git credentials.
set -euo pipefail
cd -- "$(dirname -- "$0")"

finish() {
  local publish_exit=$?
  if (( publish_exit != 0 )); then
    printf '\nPublication did not complete. Read the Git error above.\n'
    printf 'Your local files and any created commit have been kept.\n'
  fi
  printf '\nPress Enter to close.\n'
  read -r reply || true
  exit "$publish_exit"
}
trap finish EXIT

expected_remote='https://github.com/Vovcheese/zen-little-things.git'
if [[ "$(git remote get-url --push origin)" != "$expected_remote" ]]; then
  printf 'Unexpected push destination. Expected: %s\n' "$expected_remote"
  exit 1
fi
if [[ "$(git branch --show-current)" != 'main' ]]; then
  printf 'Switch to main before running this publisher.\n'
  exit 1
fi
if ! git diff --cached --quiet; then
  printf 'There are already staged changes. Review and commit or unstage them first.\n'
  exit 1
fi

# Explicit paths keep personal captures, local logs, and generated fixtures out.
files=(
  .gitattributes .gitignore
  .github/ISSUE_TEMPLATE/bug_report.md
  .github/ISSUE_TEMPLATE/feature_request.md
  .github/pull_request_template.md
  README.md CHANGELOG.md CONTRIBUTING.md LICENSE THIRD_PARTY.md
  docs/INSTALLATION.md docs/PUBLISHING.md docs/SCREENSHOTS.md
  docs/assets/overview.svg
  mods/zen-peek/README.md mods/zen-peek/chrome.css mods/zen-peek/mod.json
  mods/zen-find/README.md mods/zen-find/chrome.css mods/zen-find/mod.json
  mods/zen-find/highlight-prefs.json
  mods/zen-folders/README.md mods/zen-folders/chrome.css mods/zen-folders/mod.json
  scripts/install_local_mod.py scripts/find_palette.py
  tests/build_folders_preview.py
  install-zen-peek.command install-zen-find.command install-zen-folders.command
  update-zen-find.command restore-zen-find-highlights.command publish.command
)
git add -- "${files[@]}"
git diff --cached --check
git diff --cached --stat
if ! git diff --cached --quiet; then
  git commit -m "Prepare Zen Little Things public preview" \
    -m "Add three independent Zen CSS mods, local installers, English guides, MIT licensing, and an illustrated overview. Document validation gaps and exclude local profile data and development captures."
fi
git push -u origin main
printf '\nPublished: https://github.com/Vovcheese/zen-little-things\n'
