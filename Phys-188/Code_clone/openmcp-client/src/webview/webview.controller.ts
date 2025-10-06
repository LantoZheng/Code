import * as vscode from 'vscode';
import { RegisterCommand } from "../common/index.js";
import { getDefaultLanunchSignature, getWorkspacePath, revealOpenMcpWebviewPanel } from './webview.service.js';
import { getWorkspaceConnectionConfigItemByPath } from '../global.js';
import path from 'path';

export class WebviewController {
    @RegisterCommand('openmcp.showOpenMCP')
    async showOpenMCP(context: vscode.ExtensionContext, uri: vscode.Uri) {        
        const connectionItem = getWorkspaceConnectionConfigItemByPath(uri.fsPath);
                
        if (!connectionItem) {
            // 项目不存在连接信息
            const cwd = path.dirname(uri.fsPath);
            const signature = getDefaultLanunchSignature(uri.fsPath, cwd);

            if (!signature) {
                vscode.window.showErrorMessage('OpenMCP: Cannot acquire launch parameters');
                return;
            }

            revealOpenMcpWebviewPanel(context, 'workspace', uri.fsPath, {
                connectionType: 'STDIO',
                name: 'OpenMCP',
                command: signature.command,
                args: signature.args,
                cwd
            });
        } else {
            revealOpenMcpWebviewPanel(context, 'workspace', uri.fsPath, connectionItem);
        }

    }
}