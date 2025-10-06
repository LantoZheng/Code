import * as vscode from 'vscode';
import { McpOptions } from '../global.js';

export class SidebarItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly command?: vscode.Command,
        public readonly icon?: string
    ) {
        super(label, collapsibleState);
        this.command = command;
        this.iconPath = new vscode.ThemeIcon(icon || 'circle-outline');
    }
}

export class ConnectionViewItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly item: McpOptions[] | McpOptions,
        public readonly icon?: string
    ) {
        super(label, collapsibleState);
        this.iconPath = new vscode.ThemeIcon(icon || 'circle-outline');
    }
}