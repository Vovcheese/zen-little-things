#!/bin/zsh
set -euo pipefail
cd -- "$(dirname -- "$0")"
log_file="$PWD/install-zen-find.log"
printf 'Zen Find — local panel and search palette installation\n' | tee "$log_file"
install_status=0
if python3 scripts/install_local_mod.py --mod zen-find 2>&1 | tee -a "$log_file"; then
  printf '\nPress Enter to exit.\n'
else
  install_status=1
  printf '\nInstallation did not complete. See install-zen-find.log.\nPress Enter to exit.\n'
fi
read -r reply
exit "$install_status"
