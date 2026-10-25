"""Check pure package allowlists and ACL without OpenWrt or host changes."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ROOT / 'firmware/openwrt'
NAMES = ('routowrt-external-forwarding', 'routowrt-external-manager', 'luci-app-routowrt-external')
spec = importlib.util.spec_from_file_location('external_stage', PACKAGES / NAMES[1] / 'tools/stage-files.py')
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)


class ExternalPackages(unittest.TestCase):
    def test_shared_sources_stage_only_the_external_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            all_files = set()
            for name in NAMES:
                output = Path(directory).resolve() / name
                manifest = stage.stage(PACKAGES / name / 'payload.json', PACKAGES, output)
                actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
                self.assertEqual(actual, {entry['path'] for entry in manifest['files']})
                all_files |= actual
                for entry in manifest['files']:
                    self.assertEqual((output / entry['path']).read_bytes(), (PACKAGES / entry['source']).read_bytes())
            modules = {p for p in all_files if p.startswith('usr/share/ucode/routowrt/')}
            self.assertEqual(modules, {'usr/share/ucode/routowrt/' + name for name in
                ('store.uc', 'job-worker.uc', 'external.uc', 'external-controller.uc', 'external-model.uc')})
            self.assertFalse(any('rules/' in p or 'policies/' in p or p.endswith('.srs') or 'sing-box' in p
                                 or 'scheduled' in p or 'fetch' in p or 'core-run' in p for p in all_files))
            self.assertNotIn('usr/libexec/routowrt-forwarding', all_files)
            self.assertNotIn('www/luci-static/resources/view/routowrt/app.js', all_files)
            store = (Path(directory) / NAMES[1] / 'usr/share/ucode/routowrt/store.uc').read_text(encoding='utf-8')
            self.assertNotIn('routowrt.model', store)
            self.assertNotIn('routowrt.subscription', store)

    def test_package_dependencies_and_private_acl_keep_the_boundary(self):
        for name in NAMES:
            text = (PACKAGES / name / 'Makefile').read_text()
            dependency = text.split('  DEPENDS:=', 1)[1].splitlines()[0]
            self.assertFalse(any(term in dependency for term in ('+routowrt-core', '+routowrt-manager ', '+uclient-fetch', '+ca-bundle', '+ucode-mod-digest')))
            self.assertIn('CONFLICTS:=', text)
            self.assertIn('PKG_FILE_DEPENDS:=', text)
        acl = json.loads((PACKAGES / NAMES[1] / 'files/usr/share/rpcd/acl.d/routowrt.json').read_text())['luci-app-routowrt']
        self.assertEqual(set(acl['read']['ubus']['routowrt']), {'capabilities', 'job_status', 'external_status'})
        self.assertEqual(set(acl['write']['ubus']['routowrt']), {'external_get', 'external_save', 'external_apply', 'external_disable'})
        defaults = (PACKAGES / NAMES[1] / 'files/etc/uci-defaults/95-routowrt-external').read_text()
        self.assertNotIn('/etc/crontabs', defaults)

    def test_payload_path_cannot_include_local_or_escape(self):
        for value in ('../secret', '.local/lab/secret', '/etc/shadow', 'source/../secret'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                stage.relative(value)


if __name__ == '__main__':
    unittest.main()
