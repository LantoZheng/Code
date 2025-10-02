Start MCP on Copilot

This tiny VS Code extension will start your user-level MCP wrapper (`~/.local/bin/word-mcp-run`) when Copilot is detected on the system or when VS Code starts and Copilot is already installed.

Install locally:

1. Build VSIX (requires `vsce` or `npm`):
   - npm i -g vsce
   - vsce package
2. Install VSIX to VS Code:
   - code --install-extension start-mcp-on-copilot-0.1.0.vsix

Notes:
- The extension is intentionally minimal and runs only on startup. It does not modify user settings.
- It checks for `~/.vscode/extensions/*copilot*` to detect Copilot presence.
- Requires `~/.local/bin/word-mcp-run` wrapper created earlier.
