import * as vscode from 'vscode';
import * as os from 'os';
import * as fspath from 'path';
import * as fs from 'fs';
import { t } from './i18n';

export type FsPath = string;
export const panels = new Map<FsPath, vscode.WebviewPanel>();

export interface IConnectionConfig {
    items: (McpOptions[] | McpOptions)[];
}

export type ConnectionType = 'STDIO' | 'SSE' | 'STREAMABLE_HTTP';

export interface McpOptions {
    connectionType: ConnectionType;
    command?: string;

    // STDIO 特定选项
    args?: string[];
    cwd?: string;
    env?: Record<string, string>;

    // SSE 特定选项
    url?: string;
    oauth?: any;

    // 通用客户端选项
    clientName?: string;
    clientVersion?: string;
    serverInfo?: {
        name: string
        version: string
    }

    // vscode 专用
    filePath?: string;
    name?: string;
    version?: string;
    type?: ConnectionType;
    rename?: boolean;

    [key: string]: any;
}


export const CONNECTION_CONFIG_NAME = 'connection.json';

let _connectionConfig: IConnectionConfig | undefined;
let _workspaceConnectionConfig: IConnectionConfig | undefined;

/**
 * @description 获取全局的连接信息，全局文件信息都是绝对路径
 * @returns 
 */
export function getConnectionConfig() {
    if (_connectionConfig) {
        return _connectionConfig;
    }
    const homeDir = os.homedir();
    const configDir = fspath.join(homeDir, '.openmcp');
    const connectionConfig = fspath.join(configDir, CONNECTION_CONFIG_NAME);
    if (!fs.existsSync(connectionConfig)) {
        fs.mkdirSync(configDir, { recursive: true });
        fs.writeFileSync(connectionConfig, JSON.stringify({ items: [] }), 'utf-8');
    }

    const rawConnectionString = fs.readFileSync(connectionConfig, 'utf-8');
    let connection;
    try {
        connection = JSON.parse(rawConnectionString) as IConnectionConfig;

        // 对连接信息进行校验
        if (!connection.items) {
            connection = { items: [] };
        }

        connection.items = connection.items.filter(item => {
            if (Array.isArray(item) && item.length === 0) {
                return false;
            }
            return true;
        });

    } catch (error) {
        connection = { items: [] };
    }

    _connectionConfig = connection;
    return connection;
}

/**
 * @description 获取工作区的连接信息，默认是 {workspace}/.openmcp/connection.json
 * @returns 
 */
export function getWorkspaceConnectionConfigPath() {
    const workspace = getWorkspacePath();
    if (!workspace) {
       return null; // 如果没有工作区，则返回 null
    }
    const configDir = fspath.join(workspace, '.openmcp');
     if (!fs.existsSync(configDir)) {
        fs.mkdirSync(configDir, { recursive: true }); // 递归创建目录
    }
    const connectionConfig = fspath.join(configDir, CONNECTION_CONFIG_NAME);
    return connectionConfig;
}

/**
 * @description 获取工作区的连接信息，工作区的连接文件的路径都是相对路径，以 {workspace} 开头
 * @param workspace 
 */
export function getWorkspaceConnectionConfig():IConnectionConfig| null {
    if (_workspaceConnectionConfig) {
        return _workspaceConnectionConfig;
    }

    const workspace = getWorkspacePath();
    if (!workspace) {
       return null; // 如果没有工作区，则返回 null
    }
    const configDir = fspath.join(workspace, '.openmcp');
    const connectionConfig = fspath.join(configDir, CONNECTION_CONFIG_NAME);

    if (!fs.existsSync(connectionConfig)) {
        fs.mkdirSync(configDir, { recursive: true });
        fs.writeFileSync(connectionConfig, JSON.stringify({ items: [] }), 'utf-8');
    }

    const rawConnectionString = fs.readFileSync(connectionConfig, 'utf-8');

    let connection;
    try {
        connection = JSON.parse(rawConnectionString) as IConnectionConfig;

        // 对连接信息进行校验
        if (!connection.items) {
            connection = { items: [] };
        }

        connection.items = connection.items.filter(item => {
            if (Array.isArray(item) && item.length === 0) {
                return false;
            }
            return true;
        });

    } catch (error) {
        connection = { items: [] };
    }

    const workspacePath = getWorkspacePath();
    for (let item of connection.items) {
        for (let connection of detachMcpOptionAsArray(item)) {
            const connectionType = (connection.type || connection.connectionType).toUpperCase() as ConnectionType;
            connection.type = undefined;
            connection.connectionType = connectionType;

            if (connection.filePath && connection.filePath.startsWith('{workspace}')) {
                connection.filePath = connection.filePath.replace('{workspace}', workspacePath).replace(/\\/g, '/');
            }
            if (connectionType === 'STDIO' && connection.cwd && connection.cwd.startsWith('{workspace}')) {
                connection.cwd = connection.cwd.replace('{workspace}', workspacePath).replace(/\\/g, '/');
            }
        }
    }

    _workspaceConnectionConfig = connection;
    return connection;
}

export function getInstalledConnectionConfigPath() {
    const homeDir = os.homedir();
    const configDir = fspath.join(homeDir, '.openmcp');
    const connectionConfig = fspath.join(configDir, CONNECTION_CONFIG_NAME);
    return connectionConfig;
}

/**
 * @description 保存连接信息到全局配置文件，这个部分和「安装的连接」对应
 * @returns 
 */
export function saveConnectionConfig() {
    if (!_connectionConfig) {
        return;
    }

    const connectionConfig = getInstalledConnectionConfigPath();

    fs.writeFileSync(connectionConfig, JSON.stringify(_connectionConfig, null, 2), 'utf-8');
}

export function saveWorkspaceConnectionConfig(workspace: string) {

    if (!_workspaceConnectionConfig) {
        return;
    }

    const connectionConfig = JSON.parse(JSON.stringify(_workspaceConnectionConfig)) as IConnectionConfig;

    const configDir = fspath.join(workspace, '.openmcp');
    const connectionConfigPath = fspath.join(configDir, CONNECTION_CONFIG_NAME);

    const workspacePath = getWorkspacePath();
    for (let item of connectionConfig.items) {
        for (let connection of detachMcpOptionAsArray(item)) {
            console.log(connection);
            
            const connectionType = (connection.type || connection.connectionType).toUpperCase() as ConnectionType;
            connection.type = undefined;
            connection.connectionType = connectionType;

            if (connection.filePath && connection.filePath.replace(/\\/g, '/').startsWith(workspacePath)) {
                connection.filePath = connection.filePath.replace(workspacePath, '{workspace}').replace(/\\/g, '/');
            }
            if (connectionType === 'STDIO' && connection.cwd && connection.cwd.replace(/\\/g, '/').startsWith(workspacePath)) {
                connection.cwd = connection.cwd.replace(workspacePath, '{workspace}').replace(/\\/g, '/');
            }
        }
    }
    fs.writeFileSync(connectionConfigPath, JSON.stringify(connectionConfig, null, 2), 'utf-8');
}


export function updateWorkspaceConnectionConfig(
    name: string,
    data: McpOptions[]
) {
    const connectionItem = getWorkspaceConnectionConfigItemByName(name);
    const workspaceConnectionConfig = getWorkspaceConnectionConfig();
    if (!workspaceConnectionConfig) {
        console.error('没有工作区连接配置文件，请先创建一个工作区连接');
        return;
    }

    data.forEach(item => {
        item.cwd = item.cwd?.replace(/\\/g, '/');
        item.name = item.serverInfo?.name;
        item.version = item.serverInfo?.version;
        item.type = undefined;
    });

    console.log('get connectionItem: ', data);

    // 如果存在，替换老的 connectionItem
    if (connectionItem) {
        const index = workspaceConnectionConfig.items.indexOf(connectionItem);
        if (index !== -1) {
            // check rename value
            const oldNItem = detachMcpOptionAsItem(workspaceConnectionConfig.items[index]);
            if (oldNItem.rename) {
                // if renamed, reserve user defined name
                const newNItem = detachMcpOptionAsItem(data);
                newNItem.name = oldNItem.name;
            }

            workspaceConnectionConfig.items[index] = data;
        } else {
            // insert new one
            workspaceConnectionConfig.items.unshift(data);
        }
    } else {
        workspaceConnectionConfig.items.unshift(data);
    }
    
    const workspacePath = getWorkspacePath();
    saveWorkspaceConnectionConfig(workspacePath);
    vscode.commands.executeCommand('openmcp.sidebar.workspace-connection.refresh');

}

export function updateInstalledConnectionConfig(
    name: string,
    data: McpOptions[]
) {
    const connectionItem = getInstalledConnectionConfigItemByName(name);
    const installedConnectionConfig = getConnectionConfig();

    // 对于第一个 item 添加 filePath
    // 对路径进行标准化
    data.forEach(item => {
        item.cwd = item.cwd?.replace(/\\/g, '/');
        item.name = item.serverInfo?.name;
        item.version = item.serverInfo?.version;
        item.type = undefined;
    });

    console.log('get connectionItem: ', data);

    if (connectionItem) {
        const index = installedConnectionConfig.items.indexOf(connectionItem);
        if (index !== -1) {
            installedConnectionConfig.items[index] = data;
        } else {
            installedConnectionConfig.items.unshift(data);
        }
    } else {
        installedConnectionConfig.items.unshift(data);
    }
    
    saveConnectionConfig();
    vscode.commands.executeCommand('openmcp.sidebar.installed-connection.refresh');
}


function normaliseConnectionFilePath(item: McpOptions, workspace: string) {
    if (item.filePath) {
        if (item.filePath.startsWith('{workspace}')) {
            return item.filePath.replace('{workspace}', workspace).replace(/\\/g, '/');
        } else {
            return item.filePath.replace(/\\/g, '/');
        }
    }

    return undefined;
}

export function getWorkspacePath() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    console.log('getWorkspacePath: ', vscode.workspace.workspaceFolders);
    return (workspaceFolder?.uri.fsPath || '').replace(/\\/g, '/');
}

/**
 * @description 根据输入的文件路径，获取该文件的 mcp 连接签名
 * @param absPath 
 */
export function getWorkspaceConnectionConfigItemByPath(absPath: string) {
    const workspacePath = getWorkspacePath();
    const workspaceConnectionConfig = getWorkspaceConnectionConfig();
    if (!workspaceConnectionConfig) {
        return null; // 如果没有工作区连接配置文件，则返回 null
    }


    const normaliseAbsPath = absPath.replace(/\\/g, '/');
    for (let item of workspaceConnectionConfig.items) {
        const nItem = detachMcpOptionAsItem(item);

        const filePath = normaliseConnectionFilePath(nItem, workspacePath);
        if (filePath === normaliseAbsPath) {
            return item;
        }
    }

    return undefined;
}

/**
 * @description 根据输入的名称，获取该文件的 mcp 连接签名
 * @param absPath 
 */
export function getWorkspaceConnectionConfigItemByName(name: string) {
    const workspaceConnectionConfig = getWorkspaceConnectionConfig();
    if (!workspaceConnectionConfig) {
        return null; // 如果没有工作区连接配置文件，则返回 null
    }
    for (let item of workspaceConnectionConfig.items) {
        const nItem = detachMcpOptionAsItem(item);
        if (nItem.name === name) {
            return item;
        }
    }

    return undefined;
}

/**
 * @description 根据输入的名称，获取该文件的 mcp 连接签名
 * @param absPath 
 */
export function getInstalledConnectionConfigItemByName(name: string) {
    const installedConnectionConfig = getConnectionConfig();

    for (let item of installedConnectionConfig.items) {
        const nItem = detachMcpOptionAsItem(item);

        if (nItem.name) {
            return item;
        }
    }

    return undefined;
}


/**
 * @description 根据输入的文件路径，获取该文件的 mcp 连接签名
 * @param absPath 
 */
export function getInstalledConnectionConfigItemByPath(absPath: string) {
    const installedConnectionConfig = getConnectionConfig();

    const normaliseAbsPath = absPath.replace(/\\/g, '/');
    for (let item of installedConnectionConfig.items) {
        const nItem = detachMcpOptionAsItem(item);

        const filePath = (nItem.filePath || '').replace(/\\/g, '/');
        if (filePath === normaliseAbsPath) {
            return item;
        }
    }

    return undefined;
}


export async function getFirstValidPathFromCommand(command: string, cwd: string): Promise<string | undefined> {
    // 分割命令字符串
    const parts = command.split(' ');

    // 遍历命令部分，寻找第一个可能是路径的部分
    for (let i = 1; i < parts.length; i++) {
        const part = parts[i];

        // 跳过以 '-' 开头的参数
        if (part.startsWith('-')) continue;

        // 处理相对路径
        let fullPath = part;
        if (!fspath.isAbsolute(part)) {
            fullPath = fspath.join(cwd, part);
        }

        console.log(fullPath);

        if (fs.existsSync(fullPath)) {
            return fullPath;
        }
    }

    return undefined;
}


export async function exportFile(filename: string, content: any) {
    // 使用 vscode 的 api，创建文件导出窗口，询问用户
    const uri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file(filename),
        filters: {
            'JSON': ['json']
        }
    });

    if (uri) {
        fs.writeFileSync(uri.fsPath, content, 'utf-8');
    }
}

export function detachMcpOptionAsItem(data: McpOptions | McpOptions[]): McpOptions {
    return Array.isArray(data) ? data[0] : data;
}

export function detachMcpOptionAsArray(data: McpOptions | McpOptions[]): McpOptions[] {
    return Array.isArray(data) ? data : [data];
}