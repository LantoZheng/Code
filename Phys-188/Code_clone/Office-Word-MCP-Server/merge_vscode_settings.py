#!/usr/bin/env python3
"""
merge_vscode_settings.py

Backup and merge a minimal OpenMCP MCP server entry into the user's
VS Code user settings.json (macOS path).

Behavior:
 - Backup existing settings.json to settings.json.bak.<timestamp>
 - If the file doesn't exist, create a new settings.json with the block.
 - If existing JSON is invalid, abort but leave a backup of the broken file.
 - If a previous "word-document-server" entry exists, save it to
   settings.json.previous_word-document-server.<timestamp>.json
 - Print a summary and exit with code 0 on success, non-zero on error.

Run: python3 merge_vscode_settings.py
"""

import json
import os
import sys
import shutil
from datetime import datetime

HOME = os.path.expanduser("~")
settings_path = os.path.join(HOME, "Library", "Application Support", "Code", "User", "settings.json")

timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
backup_path = settings_path + ".bak." + timestamp
prev_server_backup = settings_path + ".previous_word-document-server." + timestamp + ".json"

entry = {
    "openmcp.client": {
        "mcpConfig": {
            "mcpServers": {
                "word-document-server": {
                    "transport": "streamable-http",
                    "url": "http://127.0.0.1:8931/mcp",
                    "description": "Word Document Server (user-global, streamable-http)"
                }
            }
        }
    }
}


def deep_merge(a, b):
    """Merge b into a recursively and return a."""
    for k, v in b.items():
        if k in a and isinstance(a[k], dict) and isinstance(v, dict):
            deep_merge(a[k], v)
        else:
            a[k] = v
    return a


def main():
    print("Merging OpenMCP MCP server entry into VS Code user settings...")
    # Ensure directory exists
    settings_dir = os.path.dirname(settings_path)
    if not os.path.isdir(settings_dir):
        print(f"Creating settings directory: {settings_dir}")
        try:
            os.makedirs(settings_dir, exist_ok=True)
        except Exception as e:
            print("Failed to create settings directory:", e)
            sys.exit(2)

    # If settings.json exists, back it up
    if os.path.exists(settings_path):
        try:
            shutil.copy2(settings_path, backup_path)
            print(f"Backed up existing settings.json -> {backup_path}")
        except Exception as e:
            print("Failed to back up settings.json:", e)
            sys.exit(3)

    data = {}
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip() == "":
                    data = {}
                else:
                    data = json.loads(content)
        except json.JSONDecodeError as jde:
            print("ERROR: settings.json contains invalid JSON. Aborting merge.")
            print("A backup was written to:", backup_path)
            sys.exit(4)
        except Exception as e:
            print("Failed to read settings.json:", e)
            sys.exit(5)

    # If there is an existing word-document-server, save it separately
    try:
        existing = data.get("openmcp.client", {}).get("mcpConfig", {}).get("mcpServers", {}).get("word-document-server")
        if existing is not None:
            with open(prev_server_backup, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            print(f"Saved existing 'word-document-server' entry to {prev_server_backup}")
    except Exception as e:
        print("Warning: could not write previous server backup:", e)

    # Merge
    merged = deep_merge(data, entry)

    # Write merged settings
    try:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        print(f"Wrote merged settings.json to {settings_path}")
    except Exception as e:
        print("Failed to write merged settings.json:", e)
        # try to restore backup
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, settings_path)
                print("Restored original settings.json from backup due to failure.")
        except Exception:
            print("Also failed to restore backup. Manual recovery needed.")
        sys.exit(6)

    print("Merge complete. Please restart VS Code (or check OpenMCP output) to verify the connection.")
    print("Backup file:", backup_path)
    if os.path.exists(prev_server_backup):
        print("Previous server entry saved to:", prev_server_backup)


if __name__ == '__main__':
    main()
