#!/bin/zsh
set -euo pipefail
cd -- "$(dirname -- "$0")"
restore_status=0
if python3 scripts/install_local_mod.py --mod zen-find --restore-highlights 2>&1 | tee restore-zen-find-highlights.log; then
  printf '\nPress Enter to exit.\n'
else
  restore_status=1
  printf '\nRestore did not complete. Read the message above.\nPress Enter to exit.\n'
fi
read -r reply
exit "$restore_status"
