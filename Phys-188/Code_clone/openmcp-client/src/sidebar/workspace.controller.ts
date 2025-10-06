import * as vscode from 'vscode';
import { RegisterCommand, RegisterTreeDataProvider } from '../common/index.js';
import { getWorkspaceConnectionConfig, getWorkspaceConnectionConfigPath, getWorkspacePath, saveWorkspaceConnectionConfig } from '../global.js';
import { ConnectionViewItem } from './common.js';
import { revealOpenMcpWebviewPanel } from '../webview/webview.service.js';
import { acquireUserCustomConnection, changeUserConnectionName, deleteUserConnection } from './workspace.service.js';
import { t } from '../i18n/index.js';

@RegisterTreeDataProvider('openmcp.sidebar.workspace-connection')
export class McpWorkspaceConnectProvider implements vscode.TreeDataProvider<ConnectionViewItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<ConnectionViewItem | undefined | null | void> = new vscode.EventEmitter<ConnectionViewItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<ConnectionViewItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private context: vscode.ExtensionContext) { }

    // 实现 TreeDataProvider 接口
    getTreeItem(element: ConnectionViewItem): vscode.TreeItem {
        element.contextValue = 'workspace-item';
        return element;
    }
    getChildren(element?: ConnectionViewItem): Thenable<ConnectionViewItem[]> {
        // TODO: 读取 configDir 下的所有文件，作为子节点
        const connection = getWorkspaceConnectionConfig();

        // 校验 connection 和 connection.items
        if (!connection || !Array.isArray(connection.items)) {
            return Promise.resolve([]);
        }

        const sidebarItems = connection.items
            .filter(item => item !== null && item !== undefined)
            .map((item, index) => {
                // 连接的名字
                const nItem = Array.isArray(item) ? item[0] : item;
                if (!nItem || typeof nItem !== 'object') {
                    return null;
                }
                const name = nItem.name || '未命名';
                const type = nItem.type || nItem.connectionType || '未知类型';
                const itemName = `${name} (${type})`;
                return new ConnectionViewItem(itemName, vscode.TreeItemCollapsibleState.None, item, 'server');
            })
            .filter(Boolean) as ConnectionViewItem[]; // 过滤掉为 null 的项

        // 返回子节点
        return Promise.resolve(sidebarItems);
    }
    @RegisterCommand('revealWebviewPanel')
    public revealWebviewPanel(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const item = view.item;
        const masterNode = Array.isArray(item) ? item[0] : item;
        const name = masterNode.filePath || masterNode.name || '';
        revealOpenMcpWebviewPanel(context, 'workspace', name, item);
    }

    @RegisterCommand('refresh')
    public refresh(context: vscode.ExtensionContext): void {
        console.log(this);

        this._onDidChangeTreeData.fire(undefined);
    }

    @RegisterCommand('addConnection')
    public async addConnection(context: vscode.ExtensionContext) {
        const workspaceConnectionConfig = getWorkspaceConnectionConfig();
        if (!workspaceConnectionConfig) {
            vscode.window.showErrorMessage('OpenMCP: ' + t('error.notOpenWorkspace'));
            return;
        }
        const item = await acquireUserCustomConnection();

        if (item.length === 0) {
            return;
        }


        workspaceConnectionConfig.items.push(item);
        saveWorkspaceConnectionConfig(getWorkspacePath());

        // 刷新侧边栏视图
        vscode.commands.executeCommand('openmcp.sidebar.workspace-connection.refresh');
    }

    @RegisterCommand('openConfiguration')
    public async openConfiguration(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const configPath = getWorkspaceConnectionConfigPath();
        if (!configPath) {
            vscode.window.showErrorMessage('OpenMCP: ' + t('error.notOpenWorkspace'));
            return;
        }
        const uri = vscode.Uri.file(configPath);
        vscode.commands.executeCommand('vscode.open', uri);
    }

    @RegisterCommand('deleteConnection')
    public async deleteConnection(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const connectionItem = view.item;
        await deleteUserConnection(connectionItem);
    }

    @RegisterCommand('changeConnectionName')
    public async changeConnectionName(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const connectionItem = view.item;
        await changeUserConnectionName(connectionItem);
    }
}
