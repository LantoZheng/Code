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
  const wrapper = path.join(home, '.local', 'bin', 'word-mcp-run');
  if (!fs.existsSync(wrapper)) {
    console.warn('Wrapper not found:', wrapper);
    return;
  }

  // Check PID file
  const pidFile = path.join(home, '.local', 'share', 'mcp-servers', 'office-word', 'word_mcp_server.pid');
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

  // Spawn wrapper in background
  try {
    cp.spawn(wrapper, [], {
      detached: true,
      stdio: 'ignore'
    }).unref();
    console.log('Started MCP wrapper:', wrapper);
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
