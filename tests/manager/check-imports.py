"""Check real manager imports and, when host jsmin exists, compact modules."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
package = root / 'firmware/openwrt/routowrt-manager/files/usr/share'
ucode = sys.argv[1] if len(sys.argv) == 2 else 'ucode'
env = {**os.environ, 'ROUTOWRT_POLICY_DIR': str(package / 'routowrt/policies')}
imports = (
    "import { call, prepareCoreStart } from 'routowrt.store'; "
    "import { sampleTraffic } from 'routowrt.traffic'; "
    "import { sampleStatus } from 'routowrt.status'; "
    "import { selectionPlan } from 'routowrt.selection'; "
)


def check_imports(modules, label):
    result = subprocess.run(
        [ucode, '-L', str(modules), '-e', imports + f"print('PASS {label} manager module imports\\n');"],
        env=env, check=False,
    )
    if result.returncode:
        raise SystemExit(result.returncode)


check_imports(package / 'ucode', 'real')
jsmin = Path(shutil.which(ucode) or ucode).resolve().with_name('jsmin')
if jsmin.is_file() and os.access(jsmin, os.X_OK):
    with tempfile.TemporaryDirectory(prefix='routowrt-compact-imports-') as directory:
        modules = Path(directory)
        target = modules / 'routowrt'
        target.mkdir()
        for source in sorted((package / 'ucode/routowrt').glob('*.uc')):
            result = subprocess.run([str(jsmin)], input=source.read_bytes(),
                                    stdout=subprocess.PIPE, check=True)
            assert result.stdout.strip(), f'jsmin produced an empty module: {source.name}'
            (target / source.name).write_bytes(result.stdout)
        check_imports(modules, 'compact')
        # Run the existing contract suite against the actual compact imports,
        # including URL regexes, subscription identities and route/DNS policy.
        result = subprocess.run([ucode, '-L', str(modules), str(root / 'tests/manager/run.uc')],
                                env=env, check=False)
        if result.returncode:
            raise SystemExit(result.returncode)
