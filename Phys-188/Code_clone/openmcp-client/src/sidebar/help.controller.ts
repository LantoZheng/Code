import * as vscode from 'vscode';
import { SidebarItem } from './common.js';
import { RegisterTreeDataProvider } from '../common/index.js';
import { t } from '../i18n/index.js';

@RegisterTreeDataProvider('openmcp.sidebar.help')
export class HelpProvider implements vscode.TreeDataProvider<SidebarItem> {

    constructor(private context: vscode.ExtensionContext) {
    }

    // 实现 TreeDataProvider 接口
    getTreeItem(element: SidebarItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: SidebarItem): Thenable<SidebarItem[]> {
        // 返回子节点
        return Promise.resolve([
            new SidebarItem(t('quick-start'), vscode.TreeItemCollapsibleState.None, {
                command: 'vscode.open',
                title: 'Open Guide',
                arguments: [vscode.Uri.parse('https://openmcp.kirigaya.cn/plugin-tutorial/usage/connect-mcp.html')]
            }, 'book'),
            new SidebarItem(t('read-document'), vscode.TreeItemCollapsibleState.None, {
                command: 'vscode.open',
                title: 'Open Documentation',
                arguments: [vscode.Uri.parse('https://openmcp.kirigaya.cn')]
            }, 'file-text'),
            new SidebarItem(t('report-issue'), vscode.TreeItemCollapsibleState.None, {
                command: 'vscode.open',
                title: 'Report Issue',
                arguments: [vscode.Uri.parse('https://github.com/LSTM-Kirigaya/openmcp-client/issues')]
            }, 'bug'),
            new SidebarItem(t('join-project'), vscode.TreeItemCollapsibleState.None, {
                command: 'vscode.open',
                title: 'Join Project',
                arguments: [vscode.Uri.parse('https://qm.qq.com/cgi-bin/qm/qr?k=C6ZUTZvfqWoI12lWe7L93cWa1hUsuVT0&jump_from=webapi&authKey=McW6B1ogTPjPDrCyGttS890tMZGQ1KB3QLuG4aqVNRaYp4vlTSgf2c6dMcNjMuBD')]
            }, 'organization'),
            new SidebarItem(t('comment-plugin'), vscode.TreeItemCollapsibleState.None, {
                command: 'vscode.open',
                title: 'Review Extension',
                arguments: [vscode.Uri.parse('https://marketplace.visualstudio.com/items?itemName=kirigaya.openmcp&ssr=false#review-details')]
            }, 'feedback')
        ]);
    }
}

