"""Check the independent LuCI, rpcd and ACL integration boundaries without tools."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
packages = root / "firmware/openwrt"
manager = packages / "routowrt-manager/files/usr/share/rpcd"
ui = packages / "luci-app-routowrt"

api = (ui / "htdocs/luci-static/resources/routowrt/api.js").read_text(encoding="utf-8")
definitions = api.split("var definitions = {", 1)[1].split("};", 1)[0]
ui_methods = set(re.findall(r"\b([A-Za-z_]+)\s*:\s*\[", definitions))

rpc = (manager / "ucode/routowrt").read_text(encoding="utf-8")
mapping = rpc.split("for(let method,args in {", 1)[1].split("}) {", 1)[0]
rpc_methods, depth = set(), 0
for token in re.finditer(r"([A-Za-z_]+)\s*:|[{}]", mapping):
    value = token.group()
    if token.group(1) and depth == 0:
        rpc_methods.add(token.group(1))
    elif value == "{":
        depth += 1
    elif value == "}":
        depth -= 1

acl = json.loads((manager / "acl.d/routowrt.json").read_text(encoding="utf-8"))
menu = json.loads((ui / "root/usr/share/luci/menu.d/luci-app-routowrt.json").read_text(encoding="utf-8"))
groups = menu["admin/services/routowrt"]["depends"]["acl"]
assert len(groups) == 1 and groups[0] in acl, "menu references a missing ACL group"
grant = acl[groups[0]]
read = set(grant["read"]["ubus"]["routowrt"])
write = set(grant["write"]["ubus"]["routowrt"])
assert ui_methods == rpc_methods, f"UI/RPC methods differ: {ui_methods ^ rpc_methods}"
check_params = ["nodeId", "subscriptionId", "nodeIds", "scope", "retryFailed"]
ui_check = re.search(r"\bcheck\s*:\s*\[([^]]*)\]", definitions).group(1)
rpc_check = re.search(r"\bcheck\s*:\s*\{([^}]*)\}", mapping).group(1)
assert re.findall(r"'([^']+)'", ui_check) == check_params, "UI check argument order changed"
assert re.findall(r"\b([A-Za-z]+)\s*:", rpc_check) == check_params, "RPC batch check arguments differ"
assert read | write == rpc_methods, "RPC methods are missing from or over-granted by ACL"
assert not read & {"get", "export", "save", "refresh", "apply", "select", "rollback", "service", "check", "cancel_check"}, "read ACL exposes credentials or actions"
assert read.isdisjoint(write), "method appears in both permission sets"
for permission in ("read", "write"):
    assert set(grant[permission]) == {"ubus"}, "ACL grants direct file or UCI access"
    assert set(grant[permission]["ubus"]) == {"routowrt"}, "ACL grants unrelated ubus objects"
    assert "*" not in grant[permission]["ubus"]["routowrt"], "wildcard RPC permission"
assert menu["admin/services/routowrt"]["action"]["path"] == "routowrt/app"
assert (ui / "htdocs/luci-static/resources/view/routowrt/app.js").is_file()
print(f"PASS {len(rpc_methods)} UI/RPC methods, private credential actions, minimal ACL and menu binding")
