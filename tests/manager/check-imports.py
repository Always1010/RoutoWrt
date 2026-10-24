"""Compile real manager modules without calling them or touching device state."""
from pathlib import Path
import os
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
package = root / 'firmware/openwrt/routowrt-manager/files/usr/share'
ucode = sys.argv[1] if len(sys.argv) == 2 else 'ucode'
result = subprocess.run(
    [ucode, '-L', str(package / 'ucode'), '-e',
     "import { call } from 'routowrt.store'; "
     "import { sampleTraffic } from 'routowrt.traffic'; "
     "import { sampleStatus } from 'routowrt.status'; "
     "import { selectionPlan } from 'routowrt.selection'; "
     "print('PASS real manager module imports\\n');"],
    env={**os.environ, 'ROUTOWRT_POLICY_DIR': str(package / 'routowrt/policies')},
    check=False,
)
raise SystemExit(result.returncode)
