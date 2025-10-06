import { Client } from "@modelcontextprotocol/sdk/client/index.js";

import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import type { McpOptions, McpTransport, IServerVersion, ToolCallResponse, ToolCallContent } from './client.dto.js';
import { PostMessageble } from "../hook/adapter.js";
import { createOcrWorker, saveBase64ImageData } from "./ocr.service.js";
import { OAuthClient } from "./auth.service.js";
import { UnauthorizedError } from '@modelcontextprotocol/sdk/client/auth.js';
import { OAuthClientProvider } from '@modelcontextprotocol/sdk/client/auth.js';
// 增强的客户端类
export class McpClient {
    private client: Client;
    private transport?: McpTransport;
    private options: McpOptions;
    private serverVersion: IServerVersion;
    private oAuthClient: OAuthClient;
    private oauthPovider?: OAuthClientProvider;

    constructor(options: McpOptions) {
        this.options = options;
        this.serverVersion = undefined;

        this.client = new Client(
            {
                name: "openmcp test local client",
                version: "0.0.1"
            },
            {
                capabilities: {
                    prompts: {},
                    resources: {},
                    tools: {}
                }
            }
        );

        this.oAuthClient = new OAuthClient();
    }

    // 连接方法
    public async connect(): Promise<void> {
        if (!this.oauthPovider){
            this.oauthPovider = await this.oAuthClient.getOAuthProvider();
        }

        const env = { ...process.env, ...this.options.env } as Record<string, string>;        

        // 根据连接类型创建传输层
        switch (this.options.connectionType) {
            case 'STDIO':
                this.transport = new StdioClientTransport({
                    command: this.options.command || '',
                    args: this.options.args || [],
                    cwd: this.options.cwd || process.cwd(),
                    stderr: 'pipe',
                    env
                });

                break;
            case 'SSE':
                if (!this.options.url) {
                    throw new Error('URL is required for SSE connection');
                }
                this.transport = new SSEClientTransport(
                    new URL(this.options.url),
                    {
                        authProvider: this.oauthPovider
                    }
                );

                break;

            case 'STREAMABLE_HTTP':
                if (!this.options.url) {
                    throw new Error('URL is required for STREAMABLE_HTTP connection');
                }
                this.transport = new StreamableHTTPClientTransport(
                    new URL(this.options.url),
                    {
                        authProvider:this.oauthPovider
                    }
                );
                break;
            default:
                throw new Error(`Unsupported connection type: ${this.options.connectionType}`);
        }

        // 建立连接
        if (this.transport) {
            try {
                // console.log(`🔌 Connecting to MCP server via ${this.options.connectionType}...`);
                await this.client.connect(this.transport);
                // console.log(`✅ Connected to MCP server via ${this.options.connectionType}`);
            } catch (error) {
                if (error instanceof UnauthorizedError) {
                    if (!(this.transport instanceof StreamableHTTPClientTransport) && !(this.transport instanceof SSEClientTransport)) {
                        console.error('❌ OAuth is only supported for StreamableHTTP and SSE transports. Please use one of these transports for OAuth authentication.');
                        return;
                    }
                    console.log('🔐 OAuth required - waiting for authorization...');
                    const callbackPromise = this.oAuthClient.waitForOAuthCallback();
                    const authCode = await callbackPromise;
                    await this.transport.finishAuth(authCode);
                    console.log('🔐 Authorization code received:', authCode);
                    console.log('🔌 Reconnecting with authenticated transport...');
                    await this.connect(); // 递归重试
                } else {
                    console.error('❌ Connection failed with non-auth error:', error);
                    throw error;
                }
            }
        }
    }


    public getServerVersion() {
        if (this.serverVersion) {
            return this.serverVersion;
        }

        const version = this.client.getServerVersion();
        this.serverVersion = version;
        return version;
    }

    // 断开连接
    public async disconnect(): Promise<void> {
        await this.client.close();
        console.log('Disconnected from MCP server');
    }

    // 列出提示
    public async listPrompts() {
        return await this.client.listPrompts();
    }

    // 获取提示
    public async getPrompt(name: string, args: Record<string, any> = {}) {        
        return await this.client.getPrompt({
            name, arguments: args
        });
    }

    // 列出资源
    public async listResources() {
        return await this.client.listResources();
    }

    // 列出所有模板资源
    public async listResourceTemplates() {
        return await this.client.listResourceTemplates();
    }

    // 读取资源
    public async readResource(uri: string) {
        return await this.client.readResource({
            uri
        });
    }

    // 列出所有工具
    public async listTools() {
        return await this.client.listTools();
    }

    // 调用工具
    public async callTool(options: { name: string; arguments: Record<string, any>, callToolOption?: any }) {
        const { callToolOption, ...methodArgs } = options;
        const res = await this.client.callTool(methodArgs, undefined, callToolOption);
        return res;
    }
}

// Connect 函数实现
export async function connect(options: McpOptions): Promise<McpClient> {
    const client = new McpClient(options);
    await client.connect();
    return client;
}

async function handleImage(
    content: ToolCallContent,
    webview: PostMessageble
) {
    if (content.data && content.mimeType) {
        const filename = saveBase64ImageData(content.data, content.mimeType);
        content.data = filename;

        // 加入工作线程
        const worker = createOcrWorker(filename, webview);

        content._meta = {
            ocr: true,
            workerId: worker.id
        };
    }
}


/**
 * @description 对 mcp server 返回的结果进行预处理
 * 对于特殊结果构造工作线程解析成文本或者其他格式的数据（比如 image url）
 * 0.x.x 受限于技术，暂时将所有结果转化成文本
 * @param response 
 * @returns 
 */
export function postProcessMcpToolcallResponse(
    response: ToolCallResponse,
    webview: PostMessageble
): ToolCallResponse {
    if (response.isError) {
        // 如果是错误响应，将其转换为错误信息
        return response;
    }

    // 将 content 中的图像 base64 提取出来，并保存到本地
    for (const content of response.content || []) {
        switch (content.type) {
            case 'image':
                handleImage(content, webview);
                break;

            default:
                break;
        }
    }

    return response;
}