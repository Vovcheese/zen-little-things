#!/bin/zsh
set -euo pipefail
cd -- "$(dirname -- "$0")"
log_file="$PWD/install-zen-peek.log"
{
  printf 'Zen Peek — local Zen Mods installation\n'
  printf 'Project directory: %s\n' "$PWD"
  date '+Started: %Y-%m-%d %H:%M:%S %Z'
} | tee "$log_file"
install_status=0
if python3 scripts/install_local_mod.py 2>&1 | tee -a "$log_file"; then
  printf '\nPress Enter to close the installer.\n'
else
  install_status=1
  printf '\nInstallation did not complete. Details saved to:\n%s\nPress Enter to exit.\n' "$log_file"
fi
read -r reply
exit "$install_status"
