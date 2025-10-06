Start MCP on Copilot

This tiny VS Code extension will start your user-level MCP wrapper (`~/.local/bin/word-mcp-run`) when Copilot is detected on the system or when VS Code starts and Copilot is already installed.

Note about shell environment
--------------------------------
The extension starts the wrapper using your login shell (the value of `$SHELL`, falling back to `/bin/zsh`) in interactive mode. That means your `~/.zshrc` (or the shell's equivalent) will be sourced before the wrapper runs. This makes user-installed tools (conda, pyenv shims, custom PATH) available to the wrapper process.

If you prefer the old behaviour (start without sourcing interactive shell config), edit `extension.js` and change the spawn call to run the Python executable directly instead of via `SHELL -ic`.

Verification
--------------------------------
1. Install/enable Copilot in VS Code and open the extension host. The wrapper should start automatically.
2. Confirm a PID file is written to `~/.local/share/mcp-servers/wolfram/wolfram_mcp_server.pid` and the process is running.
3. If the wrapper fails to find your python (or other tools), ensure `~/.zshrc` exports PATH or initialises your tool managers (conda/pyenv) for interactive shells.


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
