import * as vscode from 'vscode';
import { RegisterCommand, RegisterTreeDataProvider } from '../common/index.js';
import { ConnectionViewItem } from './common.js';
import { getConnectionConfig, getInstalledConnectionConfigPath, saveConnectionConfig } from '../global.js';
import { changeInstalledConnectionName, deleteInstalledConnection } from './installed.service.js';
import { revealOpenMcpWebviewPanel } from '../webview/webview.service.js';
import { acquireUserCustomConnection } from './workspace.service.js';

@RegisterTreeDataProvider('openmcp.sidebar.installed-connection')
export class McpInstalledConnectProvider implements vscode.TreeDataProvider<ConnectionViewItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<ConnectionViewItem | undefined | null | void> = new vscode.EventEmitter<ConnectionViewItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<ConnectionViewItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private context: vscode.ExtensionContext) {}

    // 实现 TreeDataProvider 接口
    getTreeItem(element: ConnectionViewItem): vscode.TreeItem {
        element.contextValue = 'installed-item';
        return element;
    }

    getChildren(element?: ConnectionViewItem): Thenable<ConnectionViewItem[]> {
        // TODO: 读取 configDir 下的所有文件，作为子节点
        const connection = getConnectionConfig();
        const sidebarItems = connection.items.map((item, index) => {
            // 连接的名字
            const nItem = Array.isArray(item)? item[0] : item;
            const itemName = `${nItem.name} (${nItem.type || nItem.connectionType})`
            return new ConnectionViewItem(itemName, vscode.TreeItemCollapsibleState.None, item, 'server');
        })
        
        // 返回子节点
        return Promise.resolve(sidebarItems);
    }

    @RegisterCommand('revealWebviewPanel')
    public revealWebviewPanel(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const item = view.item;
        console.log(item);
        
        const masterNode = Array.isArray(item)? item[0] : item;
        const name = masterNode.filePath || masterNode.name || '';
        revealOpenMcpWebviewPanel(context, 'installed', name, item);
    }

    @RegisterCommand('refresh')
    public refresh(context: vscode.ExtensionContext): void {
        this._onDidChangeTreeData.fire();
    }

    @RegisterCommand('addConnection')
    public async addConnection(context: vscode.ExtensionContext) {
        const item = await acquireUserCustomConnection();

        if (item.length === 0) {
            return;
        }

        const connectionConfig = getConnectionConfig();
        connectionConfig.items.push(item);
        
        saveConnectionConfig();

        // 刷新侧边栏视图
        vscode.commands.executeCommand('openmcp.sidebar.installed-connection.refresh');
    }

    @RegisterCommand('openConfiguration')
    public async openConfiguration(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const configPath = getInstalledConnectionConfigPath();
        const uri = vscode.Uri.file(configPath);
        vscode.commands.executeCommand('vscode.open', uri);
    }

    @RegisterCommand('deleteConnection')
    public async deleteConnection(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const connectionItem = view.item;
        await deleteInstalledConnection(connectionItem);
    }

    @RegisterCommand('changeConnectionName')
    public async changeConnectionName(context: vscode.ExtensionContext, view: ConnectionViewItem) {
        const connectionItem = view.item;
        await changeInstalledConnectionName(connectionItem);
    }
}
