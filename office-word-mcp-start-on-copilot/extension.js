'use strict';
const cp = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

/**
 * Start the MCP wrapper if not already running.
 */
function startWrapper(context) {
  const home = os.homedir();
  // Launch the local WolframAlpha MCP server script that's bundled in the repo.
  // Prefer conda base Python if available (CONDA_PREFIX / CONDA_EXE), otherwise
  // fall back to the system Python used elsewhere in the repo.
  let python = '/opt/homebrew/opt/python@3.13/bin/python3.13';
  try {
    const condaPrefix = process.env.CONDA_PREFIX || null;
    const condaExe = process.env.CONDA_EXE || null;
    if (condaPrefix) {
      const candidate = path.join(condaPrefix, 'bin', 'python');
      if (fs.existsSync(candidate)) python = candidate;
    } else if (condaExe) {
      // condaExe might be /.../miniconda3/bin/conda
      const candidate = path.join(path.dirname(condaExe), 'python');
      if (fs.existsSync(candidate)) python = candidate;
    } else {
      // common local miniconda install location (macOS) - check and use if present
      const common = '/opt/homebrew/Caskroom/miniconda/base/bin/python';
      if (fs.existsSync(common)) python = common;
    }
  } catch (e) {
    // ignore and use fallback
  }
  const wrapper = path.join(__dirname, '..', 'Office-Word-MCP-Server', 'wolframalpha_mcp_server.py');
  if (!fs.existsSync(wrapper)) {
    console.warn('Wrapper not found:', wrapper);
    return;
  }

  // Check PID file for the wolfram server
  const pidDir = path.join(home, '.local', 'share', 'mcp-servers', 'wolfram');
  const pidFile = path.join(pidDir, 'wolfram_mcp_server.pid');
  if (fs.existsSync(pidFile)) {
    try {
      const pid = parseInt(fs.readFileSync(pidFile, 'utf8').trim(), 10);
      process.kill(pid, 0);
      // process running
      console.log('MCP wrapper already running (pid:', pid, ')');
      return;
    } catch (e) {
      // Not running
    }
  }

  // Spawn wrapper in background. Use the user's shell (prefer zsh) as an
  // interactive login-ish shell so that user zsh config (e.g. ~/.zshrc) is
  // sourced and environment customizations (PATH, conda initialisation, etc.)
  // are available to the wrapper process.
  try {
    // prefer user's SHELL if available, otherwise fallback to /bin/zsh
    const userShell = process.env.SHELL || '/bin/zsh';
    // Build a safe command to exec the python wrapper under the shell. We
    // wrap the wrapper path in single quotes and escape existing single quotes
    // to avoid injection issues.
    const safeWrapper = wrapper.replace(/'/g, "'\\''");
    const shellCmd = `exec ${python} '${safeWrapper}'`;

    // Use -i so zsh reads ~/.zshrc (interactive). Use -c to run the command.
    const child = cp.spawn(userShell, ['-ic', shellCmd], {
      detached: true,
      stdio: 'ignore',
      env: process.env
    });
    // Detach from parent
    child.unref();
    try {
      if (!fs.existsSync(pidDir)) fs.mkdirSync(pidDir, { recursive: true });
      fs.writeFileSync(pidFile, String(child.pid));
    } catch (e) {
      console.warn('Failed to write PID file:', e);
    }
    console.log('Started Wolfram MCP server (pid:', child.pid, ') at', wrapper);
  } catch (e) {
    console.error('Failed to start wrapper:', e);
  }
}

/**
 * Check if Copilot extension is installed/active, by id prefix 'github.copilot' or 'GitHub.copilot'
 */
function hasCopilotExtension() {
  try {
    const vscodeExtensionsPath = path.join(os.homedir(), '.vscode', 'extensions');
    if (!fs.existsSync(vscodeExtensionsPath)) return false;
    const files = fs.readdirSync(vscodeExtensionsPath);
    return files.some(f => f.toLowerCase().includes('copilot'));
  } catch (e) {
    return false;
  }
}

function activate(context) {
  // On startup, if Copilot extension is present start wrapper
  if (hasCopilotExtension()) {
    startWrapper(context);
  }

  // Also listen to file changes in extensions folder to detect Copilot install/uninstall
  const extensionsDir = path.join(os.homedir(), '.vscode', 'extensions');
  try {
    fs.watch(extensionsDir, { persistent: false }, (eventType, filename) => {
      if (!filename) return;
      if (filename.toLowerCase().includes('copilot')) {
        // wait a little for installation to finish
        setTimeout(() => startWrapper(context), 2000);
      }
    });
  } catch (e) {
    // ignore
  }
}

function deactivate() {}

module.exports = { activate, deactivate };
