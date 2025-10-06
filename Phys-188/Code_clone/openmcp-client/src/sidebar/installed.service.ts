import { getConnectionConfig, panels, saveConnectionConfig, getFirstValidPathFromCommand, McpOptions } from "../global.js";
import * as vscode from 'vscode';
import { t } from "../i18n/index.js";

export async function deleteInstalledConnection(item: McpOptions[] | McpOptions) {
    // 弹出确认对话框
    const masterNode = Array.isArray(item) ? item[0] : item;
    const name = masterNode.name || 'unknown node name';
    
    const res = await vscode.window.showWarningMessage(
        t("ensure-delete-connection", name),
        { modal: true },
        { title: t('confirm'), value: true },
    );

    const confirm = res?.value;

    if (!confirm) {
        return; // 用户取消删除
    }


    const installedConnection = getConnectionConfig();

    // 从配置中移除该连接项
    const index = installedConnection.items.indexOf(item);
    

    if (index !== -1) {
        installedConnection.items.splice(index, 1);

        // 保存更新后的配置
        saveConnectionConfig();

        // 刷新侧边栏视图
        vscode.commands.executeCommand('openmcp.sidebar.installed-connection.refresh');

        // 如果该连接有对应的webview面板，则关闭它
        const filePath = masterNode.filePath || '';
        const panel = panels.get(filePath);
        panel?.dispose();
        panels.delete(filePath);
    }
}

export async function changeInstalledConnectionName(item: McpOptions[] | McpOptions) {
    // 获取当前连接项
    const masterNode = Array.isArray(item) ? item[0] : item;
    const currentName = masterNode.name || '';

    // 弹出输入框让用户输入新的服务器名称
    const newName = await vscode.window.showInputBox({
        prompt: t('openmcp.sidebar.installed-connection.changeConnectionName.title'),
        value: currentName,
        ignoreFocusOut: true,
        validateInput: (value) => {
            if (!value || value.trim() === '') {
                return t('error.connectionNameRequired');
            }
            return null;
        }
    });

    // 用户取消或输入无效名称
    if (!newName || newName.trim() === '' || newName === currentName) {
        return;
    }

    // 获取已安装的连接配置
    const installedConnection = getConnectionConfig();

    // 更新 panel 标题
    if (masterNode.name && panels.has(masterNode.name)) {
        const panel = panels.get(masterNode.name)!;
        panel.title = 'OpenMCP ' + newName.trim();
    }

    // 更新连接名称
    masterNode.name = newName.trim();
    masterNode.rename = true;

    // 保存更新后的配置
    saveConnectionConfig();

    // 刷新侧边栏视图
    vscode.commands.executeCommand('openmcp.sidebar.installed-connection.refresh');
}