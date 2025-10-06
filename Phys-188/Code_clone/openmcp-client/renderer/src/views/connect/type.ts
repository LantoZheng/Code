
export type ConnectionType = 'STDIO' | 'SSE' | 'STREAMABLE_HTTP';

export interface ConnectionTypeOptionItem {
    value: ConnectionType;
    label: string;
}


export interface IConnectionResult {
    info?: string
    success: boolean
    reuseConntion: boolean
    status: string
    clientId: string
    name: string
    version: string
    logString: {
        type: 'info' | 'error' | 'warning',
        title: string
        message?: string
    }[]
}



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
    serverInfo: {
        name: string
        version: string
    }
}

export interface EnvItem {
    key: string
    value: string
}


export interface IConnectionEnvironment {
    data: EnvItem[]
    newKey: string
    newValue: string
}

export interface IConnectionArgs {
    connectionType: ConnectionType;
    commandString?: string;
    cwd?: string;
    url?: string;
    oauth?: string;
    env?: Record<string, string>;
}


export interface ConnectionResult {
    status: string
    clientId: string
    name: string
    version: string
}

export interface McpClientGetCommonOption {
    cache: boolean;
}