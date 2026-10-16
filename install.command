#!/bin/zsh
# Open from Finder or run: zsh install.command
set -euo pipefail
cd -- "$(dirname -- "$0")"
finish() {
  local install_exit=$?
  printf '\nPress Enter to close.\n'
  read -r reply || true
  exit "$install_exit"
}
trap finish EXIT
if ! command -v python3 >/dev/null 2>&1; then
  printf 'Python 3.9 or newer is required. Install Python, then run this file again.\n'
  exit 1
fi
python3 scripts/install_menu.py
