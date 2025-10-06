import { useMessageBridge } from "@/api/message-bridge";
import { reactive, type Reactive } from "vue";
import type { IConnectionResult, ConnectionTypeOptionItem, IConnectionArgs, IConnectionEnvironment, McpOptions, McpClientGetCommonOption } from "./type";
import { ElMessage } from "element-plus";
import { loadPanels } from "@/hook/panel";
import { getPlatform } from "@/api/platform";
import type { PromptsGetResponse, PromptsListResponse, PromptTemplate, Resources, ResourcesListResponse, ResourcesReadResponse, ResourceTemplate, ResourceTemplatesListResponse, ToolCallResponse, ToolItem, ToolsListResponse } from "@/hook/type";
import { mcpSetting } from "@/hook/mcp";
import chalk from "chalk";
import I18n from '@/i18n';

const { t } = I18n.global;

export const connectionSelectDataViewOption: ConnectionTypeOptionItem[] = [
    {
        value: 'STDIO',
        label: 'STDIO'
    },
    {
        value: 'SSE',
        label: 'SSE'
    },
    {
        value: 'STREAMABLE_HTTP',
        label: 'STREAMABLE_HTTP'
    }
]

function prettifyMapKeys(keys: MapIterator<string>) {
    const result: string[] = [];
    for (const key of keys) {
        result.push('+ ' + key);
    }
    return result.join('\n');
}

function _processSchemaNode(node: any, defs: Record<string, any> = {}): any {
    // Handle $ref references
    if ('$ref' in node) {
        const refPath = node['$ref'];
        if (refPath.startsWith('#/$defs/')) {
            const refName = refPath.split('/').pop();
            if (refName && refName in defs) {
                // Process the referenced definition
                return _processSchemaNode(defs[refName], defs);
            }
        }
    }

    // Start with a new schema object
    const result: Record<string, any> = {};

    // Copy the basic properties
    if ('type' in node) {
        result.type = node.type;
    }

    // Handle anyOf (often used for optional fields with None)
    if ('anyOf' in node) {
        const nonNullTypes = node.anyOf.filter((t: any) => t?.type !== 'null');
        if (nonNullTypes.length > 0) {
            // Process the first non-null type
            const processed = _processSchemaNode(nonNullTypes[0], defs);
            Object.assign(result, processed);
        }
    }

    // Handle description
    if ('description' in node) {
        result.description = node.description;
    }

    // Handle object properties recursively
    if (node?.type === 'object' && 'properties' in node) {
        result.type = 'object';
        result.properties = {};

        // Process each property
        for (const [propName, propSchema] of Object.entries(node.properties)) {
            result.properties[propName] = _processSchemaNode(propSchema as any, defs);
        }

        // Add required fields if present
        if ('required' in node) {
            result.required = node.required;
        }
    }

    // Handle arrays
    if (node?.type === 'array' && 'items' in node) {
        result.type = 'array';
        result.items = _processSchemaNode(node.items, defs);
    }

    return result;
}

export class McpClient {
    // 连接入参
    public connectionArgs: IConnectionArgs;
    // 连接出参
    public connectionResult: IConnectionResult;

    // 预设环境变量，初始化的时候会去获取它们
    public presetsEnvironment: string[] = ['HOME', 'LOGNAME', 'PATH', 'SHELL', 'TERM', 'USER'];
    // 环境变量
    public connectionEnvironment: IConnectionEnvironment;

    // logger 面板的 ref
    public connectionLogRef: any = null;
    // setting 面板的 ref
    public connectionSettingRef: any = null;

    public tools: Map<string, ToolItem> | null = null;
    public promptTemplates: Map<string, PromptTemplate> | null = null;
    public resources: Map<string, Resources> | null = null;
    public resourceTemplates: Map<string, ResourceTemplate> | null = null;

    constructor(
        public clientVersion: string = '0.0.1',
        public clientNamePrefix: string = 'openmcp.connect'
    ) {
        // 连接入参
        this.connectionArgs = {
            connectionType: 'STDIO',
            commandString: '',
            cwd: '',
            url: '',
            oauth: ''
        };

        // 连接出参
        this.connectionResult = {
            success: false,
            reuseConntion: false,
            status: 'disconnected',
            clientId: '',
            name: '',
            version: '',
            logString: []
        };

        // 环境变量
        this.connectionEnvironment = {
            data: [],
            newKey: '',
            newValue: ''
        };
    }

    async acquireConnectionSignature(args: IConnectionArgs) {
        this.connectionArgs.connectionType = args.connectionType;
        this.connectionArgs.commandString = args.commandString || '';
        this.connectionArgs.cwd = args.cwd || '';
        this.connectionArgs.url = args.url || '';
        this.connectionArgs.oauth = args.oauth || '';
        this.connectionArgs.env = args.env || {};
    }

    get clientId() {
        return this.connectionResult.clientId;
    }

    get name() {
        return this.connectionResult.name;
    }

    get version() {
        return this.connectionResult.version;
    }

    get status() {
        return this.connectionResult.status;
    }

    get connected() {
        return this.connectionResult.success;
    }

    get env() {
        const env = {} as Record<string, string>;
        this.connectionEnvironment.data.forEach(item => {
            env[item.key] = item.value;
        });
        return env;
    }

    public async getTools(option?: McpClientGetCommonOption) {

        const {
            cache = true
        } = option || {};

        if (cache && this.tools) {
            return this.tools;
        }

        const bridge = useMessageBridge();

        const { code, msg } = await bridge.commandRequest<ToolsListResponse>('tools/list', { clientId: this.clientId });
        if (code !== 200) {
            return new Map<string, ToolItem>();
        }

        this.tools = new Map<string, ToolItem>();
        msg.tools.forEach(tool => {
            console.log(tool.inputSchema);
            
            // const standardSchema = _processSchemaNode(tool.inputSchema, tool.inputSchema.$defs || {});

            // tool.inputSchema = standardSchema;

            this.tools!.set(tool.name, tool);
        });

        return this.tools;
    }

    public async getPromptTemplates(option?: McpClientGetCommonOption) {

        const {
            cache = true
        } = option || {};

        if (cache && this.promptTemplates) {
            return this.promptTemplates;
        }

        const bridge = useMessageBridge();

        const { code, msg } = await bridge.commandRequest<PromptsListResponse>('prompts/list', { clientId: this.clientId });

        if (code !== 200) {
            return new Map<string, PromptTemplate>();
        }

        this.promptTemplates = new Map<string, PromptTemplate>();
        msg.prompts.forEach(template => {
            this.promptTemplates!.set(template.name, template);
        });

        return this.promptTemplates;
    }

    public async getResources(option?: McpClientGetCommonOption) {

        const {
            cache = true
        } = option || {};

        if (cache && this.resources) {
            return this.resources;
        }

        const bridge = useMessageBridge();

        const { code, msg } = await bridge.commandRequest<ResourcesListResponse>('resources/list', { clientId: this.clientId });
        if (code !== 200) {
            return new Map<string, Resources>();
        }

        this.resources = new Map<string, Resources>();
        msg.resources.forEach(resource => {
            this.resources!.set(resource.name, resource);
        });
        return this.resources;
    }

    public async getResourceTemplates(option?: McpClientGetCommonOption) {

        const {
            cache = true
        } = option || {};

        if (cache && this.resourceTemplates) {
            return this.resourceTemplates;
        }

        const bridge = useMessageBridge();

        const { code, msg } = await bridge.commandRequest<ResourceTemplatesListResponse>('resources/templates/list', { clientId: this.clientId });
        if (code !== 200) {
            return new Map();
        }
        this.resourceTemplates = new Map<string, ResourceTemplate>();
        msg.resourceTemplates.forEach(template => {
            this.resourceTemplates!.set(template.name, template);
        });
        return this.resourceTemplates;
    }

    private get commandAndArgs() {
        const commandString = this.connectionArgs.commandString;

        if (!commandString) {
            return { command: '', args: [] };
        }

        const args = commandString.split(' ');
        const command = args.shift() || '';

        return { command, args };
    }

    get connectOption() {
        const { command, args } = this.commandAndArgs;
        const url = this.connectionArgs.url;
        const cwd = this.connectionArgs.cwd;
        const oauth = this.connectionArgs.oauth;
        const connectionType = this.connectionArgs.connectionType;

        const clientName = this.clientNamePrefix + '.' + this.connectionArgs.connectionType;
        const clientVersion = this.clientVersion;

        // 合并 this.env 和 this.connectionArgs.env
        const env = {
            // 软件层面设置的 env
            ...this.env,
            // sdk 层面设置的 env
            ...this.connectionArgs.env
        };

        const option: McpOptions = {
            connectionType,
            command,
            args,
            url,
            cwd,
            oauth,
            clientName,
            clientVersion,
            env,
            serverInfo: {
                name: this.connectionResult.name,
                version: this.connectionResult.version
            }
        };

        return option;
    }

    public async connect() {
        const bridge = useMessageBridge();
        const { code, msg } = await bridge.commandRequest<IConnectionResult>('connect', this.connectOption);

        this.connectionResult.success = (code === 200);

        if (code !== 200) {
            const message = msg.toString();
            this.connectionResult.logString.push({
                type: 'error',
                title: t('connect-fail'),
                message
            });

            ElMessage.error(message);
            return false;
        } else {
            this.connectionResult.logString.push({
                type: 'info',
                title: msg.name + ' ' + msg.version + ' ' + t('connect-success'),
                message: JSON.stringify(msg, null, 2)
            });
        }

        this.connectionResult.reuseConntion = msg.reuseConntion;
        this.connectionResult.status = msg.status;
        this.connectionResult.clientId = msg.clientId;
        this.connectionResult.name = msg.name;
        this.connectionResult.version = msg.version;

        // 刷新所有资源
        const tools = await this.getTools({ cache: false });
        this.connectionResult.logString.push({
            type: 'info',
            title: `${this.name}'s tools loaded (${tools.size})`,
            message: prettifyMapKeys(tools.keys())
        });

        const prompts = await this.getPromptTemplates({ cache: false });
        this.connectionResult.logString.push({
            type: 'info',
            title: `${this.name}'s prompts loaded (${prompts.size})`,
            message: prettifyMapKeys(prompts.keys())
        });

        const resources = await this.getResources({ cache: false });
        this.connectionResult.logString.push({
            type: 'info',
            title: `${this.name}'s resources loaded (${resources.size})`,
            message: prettifyMapKeys(resources.keys())
        });

        const resourceTemplates = await this.getResourceTemplates({ cache: false });
        this.connectionResult.logString.push({
            type: 'info',
            title: `${this.name}'s resourceTemplates loaded (${resourceTemplates.size})`,
            message: prettifyMapKeys(resourceTemplates.keys())
        });

        return true;
    }

    public async disconnect() {
        const bridge = useMessageBridge();
        const { code, msg } = await bridge.commandRequest<IConnectionResult>('disconnect', {
            clientId: this.connectionResult.clientId,
        });

        this.connectionResult.success = (code === 200);

        if (code !== 200) {
            const message = msg.toString();
            this.connectionResult.logString.push({
                type: 'error',
                title: t('disconnect-fail'),
                message
            });

            ElMessage.error(message);
            return false;
        } else {
            this.connectionResult.logString.push({
                type: 'info',
                title: t('disconnect-success'),
                message: JSON.stringify(msg, null, 2)
            });
        }

        // 清理本地连接状态
        this.connectionResult.status = 'disconnected';
        this.connectionResult.success = false;
        this.connectionResult.clientId = '';
        this.connectionResult.name = '';
        this.connectionResult.version = '';
        this.connectionResult.reuseConntion = false;

        return true;
    }


    /**
     * @description 处理环境变量开关
     * - 开启时，刷新预设环境变量的数值
     * - 关闭时，清空预设环境变量的数值
     * @param enabled 
     */
    public async handleEnvSwitch(enabled: boolean) {
        const presetVars = this.presetsEnvironment;
        if (enabled) {
            const values = await this.lookupEnvVar(presetVars);

            const env = this.connectOption.env || {};

            if (values) {
                // 将 key values 合并进 connectionEnv.data 中
                for (let i = 0; i < presetVars.length; i++) {
                    const varName = presetVars[i];
                    const varValue = values[i];

                    if (Object.hasOwn(env, varName)) {
                        // 若已有相同的 key, 采用原本的
                    } else {
                        env[varName] = varValue;
                    }
                }

                for (const varName of Object.keys(env)) {
                    this.connectionEnvironment.data.push({ key: varName, value: env[varName] });
                }
            }
        } else {
            // 清空 connectionEnv.data 中所有 key 为 presetVars 的项
            const reserveItems = this.connectionEnvironment.data.filter(item => !presetVars.includes(item.key));
            this.connectionEnvironment.data = reserveItems;
        }
    }


    /**
     * @description 查询环境变量
     * @param varNames
     * @returns 
     */
    public async lookupEnvVar(varNames: string[]) {
        const bridge = useMessageBridge();
        const { code, msg } = await bridge.commandRequest('lookup-env-var', {
            keys: varNames
        });

        if (code === 200) {

            this.connectionResult.logString.push({
                type: 'info',
                title: t('preset-env-sync.success')
            });

            return msg;
        } else {
            this.connectionResult.logString.push({
                type: 'error',
                title: t('preset-env-sync.fail'),
                message: msg.toString()
            });
        }
    }

    // 添加资源刷新方法，支持超时控制
    public async refreshAllResources(timeoutMs = 30000): Promise<void> {
        const controller = new AbortController();
        const signal = controller.signal;

        // 设置超时
        const timeoutId = setTimeout(() => {
            controller.abort();
            console.error(`[REFRESH TIMEOUT] Client ${this.clientId}`);
        }, timeoutMs);

        try {
            console.log(`[REFRESH START] Client ${this.clientId}`);

            // 按顺序刷新资源
            await this.getTools({ cache: false });
            await this.getPromptTemplates({ cache: false });
            await this.getResources({ cache: false });
            await this.getResourceTemplates({ cache: false });
            console.log(chalk.gray(`[${new Date().toLocaleString()}]`),
                chalk.green(`🚀 [${this.name}] REFRESH COMPLETE`));
        } catch (error) {
            if (signal.aborted) {
                throw new Error(`Refresh timed out after ${timeoutMs}ms`);
            }
            console.error(`[REFRESH ERROR] Client ${this.clientId}:`, error);
            console.error(
                chalk.gray(`[${new Date().toLocaleString()}]`),
                chalk.red(`🚀 [${this.name}] REFRESH FAILED`),
                error
            );
            throw error;
        } finally {
            clearTimeout(timeoutId);
        }
    }
}


class McpClientAdapter {
    public clients: Reactive<McpClient[]> = reactive([]);
    public currentClientIndex: number = 0;
    public refreshSignal = reactive({ value: 0 });

    private defaultClient: McpClient = new McpClient();
    public connectLogListenerCancel: (() => void) | null = null;
    public connectrefreshListener: (() => void) | null = null;

    constructor(
        public platform: string
    ) {
        if (platform !== 'nodejs') {
            this.addConnectRefreshListener();
        }
    }

    /**
     * @description 获取连接参数签名
     * @returns 
     */
    public async getLaunchSignature(): Promise<IConnectionArgs[]> {

        const bridge = useMessageBridge();
        const { code, msg } = await bridge.commandRequest(this.platform + '/launch-signature');

        if (code !== 200) {
            const message = msg.toString();
            ElMessage.error(message);
            return [];
        }

        // 判断一下版本，新版本的 msg 应该是数组，老版本是对象
        // 返回的数组的第一个为主节点，其余为从节点
        if (Array.isArray(msg)) {
            return msg;
        }
        return [msg];
    }

    get masterNode() {
        if (this.clients.length === 0) {
            return this.defaultClient;
        }
        return this.clients[0];
    }

    public async saveLaunchSignature() {
        const bridge = useMessageBridge();

        const options: McpOptions[] = [];

        for (const client of this.clients) {
            const option = client.connectOption;
            const env = {} as Record<string, string>;

            for (const item of client.connectionEnvironment.data) {
                env[item.key] = item.value;
            }

            option.env = env;
            options.push(option);
        }

        // 同步成功的连接参数到后端，更新 vscode treeview 中的列表
        const deserializeOption = JSON.parse(JSON.stringify(options));

        bridge.postMessage({
            command: platform + '/update-connection-signature',
            data: deserializeOption
        });
    }

    private findClientIndexByUuid(uuid: string): number {
        // 检查客户端数组是否存在且不为空
        if (!this.clients || this.clients.length === 0) {
            return -1;
        }

        const index = this.clients.findIndex(client => client.clientId === uuid);
        return index;
    }

    /**
     * @description register HMR
     */
    public addConnectRefreshListener() {
        // 创建对于 connect/refresh 的监听        
        if (!this.connectrefreshListener) {
            const bridge = useMessageBridge();
            this.connectrefreshListener = bridge.addCommandListener('connect/refresh', async (message) => {
                const { code, msg } = message;

                console.log('refresh');


                if (code === 200) {
                    // 查找目标客户端
                    const clientIndex = this.findClientIndexByUuid(msg.uuid);

                    if (clientIndex > -1) {
                        // 刷新该客户端的所有资源
                        console.log('clientIndex', clientIndex);

                        await this.clients[clientIndex].refreshAllResources();

                        // 更新 refreshSignal，所有 watch refreshSignal 的部分会发生更新
                        this.refreshSignal.value++;
                    } else {
                        console.error(
                            chalk.gray(`[${new Date().toLocaleString()}]`),
                            chalk.red(`No client found with ID: ${msg.uuid}`),
                        );
                    }
                }
            }, { once: false });
        }
    }

    public async launch() {
        // 创建对于 log/output 的监听
        if (!this.connectLogListenerCancel) {
            const bridge = useMessageBridge();
            this.connectLogListenerCancel = bridge.addCommandListener('connect/log', (message) => {
                const { code, msg } = message;

                const client = this.clients.at(-1);

                if (!client) {
                    return;
                }

                client.connectionResult.logString.push({
                    type: code === 200 ? 'info' : 'error',
                    title: msg.title,
                    message: msg.message
                });

            }, { once: false });
        }

        const launchSignature = await this.getLaunchSignature();

        let allOk = true;

        for (const item of launchSignature) {

            // 创建一个新的客户端            
            const client = new McpClient();

            // 同步连接参数
            await client.acquireConnectionSignature(item);

            // 同步环境变量
            await client.handleEnvSwitch(true);

            this.clients.push(client);

            // 连接
            const ok = await client.connect();

            let wrapperChalk = chalk as any;

            if (platform === 'web') {
                wrapperChalk = {
                    gray: (s: string) => s,
                    green: (s: string) => s,
                    red: (s: string) => s
                }
            }

            if (ok) {
                console.log(
                    wrapperChalk.gray(`[${new Date().toLocaleString()}]`),
                    wrapperChalk.green(`🚀 [${client.name}] ${client.version} connected`)
                );
            } else {
                console.log(
                    wrapperChalk.gray(`[${new Date().toLocaleString()}]`),
                    wrapperChalk.red(`× fail to connect `),
                    wrapperChalk.red(JSON.stringify(client.connectionResult.logString, null, 2))
                );
            }

            allOk &&= ok;
        }

        // 如果全部成功，保存连接参数
        if (allOk) {
            this.saveLaunchSignature();
        }
    }

    public async readResource(resourceUri?: string) {
        if (!resourceUri) {
            return undefined;
        }

        // TODO: 如果遇到不同服务器的同名 tool，请拓展解决方案
        // 目前只找到第一个匹配 toolName 的工具进行调用
        let clientId = this.clients[0].clientId;

        for (const client of this.clients) {
            const resources = await client.getResources();
            const resource = resources.get(resourceUri);
            if (resource) {
                clientId = client.clientId;
                break;
            }
        }

        const bridge = useMessageBridge();
        const { code, msg } = await bridge.commandRequest<ResourcesReadResponse>('resources/read', { clientId, resourceUri });

        return msg;
    }

    public async readPromptTemplate(promptId: string, args?: Record<string, any>) {
        // TODO: 如果遇到不同服务器的同名 tool，请拓展解决方案
        // 目前只找到第一个匹配 toolName 的工具进行调用
        let clientId = this.clients[0].clientId;

        for (const client of this.clients) {
            const promptTemplates = await client.getPromptTemplates();
            const promptTemplate = promptTemplates.get(promptId);
            if (promptTemplate) {
                clientId = client.clientId;
                break;
            }
        }

        const bridge = useMessageBridge();
        const { code, msg } = await bridge.commandRequest<PromptsGetResponse>('prompts/get', { clientId, promptId, args });
        return msg;
    }

    public async callTool(toolName: string, toolArgs: Record<string, any>) {
        // TODO: 如果遇到不同服务器的同名 tool，请拓展解决方案
        // 目前只找到第一个匹配 toolName 的工具进行调用
        let clientId = this.clients[0].clientId;

        for (const client of this.clients) {
            const tools = await client.getTools();
            const tool = tools.get(toolName);
            if (tool) {
                clientId = client.clientId;
                break;
            }
        }

        const bridge = useMessageBridge();
        const { msg } = await bridge.commandRequest<ToolCallResponse>('tools/call', {
            clientId,
            toolName,
            toolArgs: JSON.parse(JSON.stringify(toolArgs)),
            callToolOption: {
                timeout: mcpSetting.timeout * 1000
            }
        });

        return msg;
    }

    public get connected() {
        return this.clients.length > 0 && this.clients[0].connectionResult.success;
    }

    public async loadPanels() {
        const masterNode = this.clients[0];
        await loadPanels(masterNode);
    }
}

const platform = getPlatform();
export const mcpClientAdapter = reactive(
    new McpClientAdapter(platform)
);

export interface ISegmentViewItem {
    value: any;
    label: string;
    client: McpClient;
    index: number;
}

export const segmentsView = reactive<ISegmentViewItem[]>([]);