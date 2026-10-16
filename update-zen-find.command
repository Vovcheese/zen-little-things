#!/bin/zsh
set -euo pipefail
cd -- "$(dirname -- "$0")"
printf 'Zen Find — update the panel without changing search preferences\n' | tee update-zen-find.log
update_status=0
if python3 scripts/install_local_mod.py --mod zen-find --no-highlights 2>&1 | tee -a update-zen-find.log; then
  printf '\nOpen Zen and try Cmd+F on a page containing text.\nPress Enter to exit.\n'
else
  update_status=1
  printf '\nUpdate did not complete. See update-zen-find.log.\nPress Enter to exit.\n'
fi
read -r reply
exit "$update_status"
