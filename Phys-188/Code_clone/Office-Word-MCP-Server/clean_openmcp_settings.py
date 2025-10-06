#!/usr/bin/env python3
"""
clean_openmcp_settings.py

Remove command/args/env keys from the word-document-server entry in
VS Code user settings.json and ensure it's configured for streamable-http URL.

Run: python3 clean_openmcp_settings.py
"""
import json
import os
import shutil
from datetime import datetime

HOME = os.path.expanduser("~")
settings_path = os.path.join(HOME, "Library", "Application Support", "Code", "User", "settings.json")
backup_path = settings_path + ".bak.clean." + datetime.now().strftime("%Y%m%dT%H%M%S")

# Desired minimal entry
minimal = {
    "transport": "streamable-http",
    "url": "http://127.0.0.1:8931/mcp",
    "description": "Word Document Server (user-global, streamable-http)"
}

print("Cleaning openmcp word-document-server entry in settings.json...")
if not os.path.exists(settings_path):
    print("settings.json not found at", settings_path)
    raise SystemExit(2)

shutil.copy2(settings_path, backup_path)
print("Backup written to:", backup_path)

with open(settings_path, "r", encoding="utf-8") as f:
    data = json.load(f)

oc = data.get("openmcp.client", {})
mc = oc.get("mcpConfig", {})
servers = mc.get("mcpServers", {})
wd = servers.get("word-document-server")

if wd is None:
    print("No existing 'word-document-server' entry found. Inserting minimal entry.")
    servers["word-document-server"] = minimal
else:
    # Remove command/args/env if present
    for k in ["command", "args", "env"]:
        if k in wd:
            wd.pop(k, None)
    # Merge/overwrite minimal fields
    wd.update(minimal)
    servers["word-document-server"] = wd

# Put back nested structure
mc["mcpServers"] = servers
oc["mcpConfig"] = mc
data["openmcp.client"] = oc

with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated settings.json written. New 'word-document-server' entry:")
print(json.dumps(servers["word-document-server"], indent=2, ensure_ascii=False))
print("Done.")
