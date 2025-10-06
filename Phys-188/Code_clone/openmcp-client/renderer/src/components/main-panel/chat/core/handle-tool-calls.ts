import type { ToolCallContent, ToolCallResponse } from "@/hook/type";
import { MessageState, type ToolCall } from "../chat-box/chat";
import { mcpClientAdapter } from "@/views/connect/core";
import type { BasicLlmDescription } from "@/views/setting/llm";
import type OpenAI from "openai";

export interface TaskLoopChatOption {
    id?: string
    proxyServer?: string
    enableXmlWrapper?: boolean
}
export type ChatCompletionCreateParamsBase = OpenAI.Chat.Completions.ChatCompletionCreateParams & TaskLoopChatOption;

export interface ToolCallResult {
    id?: string;
    index: number;
    state: MessageState;
    content: ToolCallContent[];
}

export type IToolCallIndex = number;

export async function handleToolCalls(toolCall: ToolCall): Promise<ToolCallResult> {

    if (!toolCall.function) {
        return {
            index: toolCall.index,
            id: toolCall.id,
            content: [{
                type: 'error',
                text: 'no tool function'
            }],
            state: MessageState.NoToolFunction
        }
    }

    // 反序列化 streaming 来的参数字符串
    // TODO: check as string
    const toolName = toolCall.function.name as string;
    const argsResult = deserializeToolCallResponse(toolCall.function.arguments as string);
    
    if (argsResult.error) {
        return {
            index: toolCall.index,
            id: toolCall.id,
            content: [{
                type: 'error',
                text: parseErrorObject(argsResult.error)
            }],
            state: MessageState.ParseJsonError
        };
    }

    const toolArgs = argsResult.value;

    // 进行调用，根据结果返回不同的值
    const toolResponse = await mcpClientAdapter.callTool(toolName, toolArgs);
    const response = handleToolResponse(toolResponse);

    return {
        index: toolCall.index,
        id: toolCall.id,
        ...response
    };
}

function deserializeToolCallResponse(toolArgs: string) {
    try {
        const args = JSON.parse(toolArgs);
        return {
            value: args,
            error: undefined
        }
    } catch (error) {
        return {
            value: undefined,
            error
        }
    }
}

export function handleToolResponse(toolResponse: ToolCallResponse) {
    if (typeof toolResponse === 'string') {

        return {
            content: [{
                type: 'error',
                text: toolResponse
            }],
            state: MessageState.ToolCall
        }

    } else if (!toolResponse.isError) {

        return {
            content: toolResponse.content,
            state: MessageState.Success
        };

    } else {

        return {
            content: toolResponse.content,
            state: MessageState.ToolCall
        };

    }
}

function parseErrorObject(error: any): string {
    if (typeof error === 'string') {
        return error;
    } else if (typeof error === 'object') {
        return JSON.stringify(error, null, 2);
    } else {
        return error.toString();
    }
}


/**
 * @description 将工具调用的ID映射为索引
 * @param toolCall 工具调用对象
 * @param callId2Index ID到索引的映射表
 * @returns 映射后的索引值
 */
export function idAsIndexAdapter(toolCall: ToolCall | string, callId2Index: Map<string, number>): IToolCallIndex {
    // grok 采用 id 作为 index，需要将 id 映射到 zero-based 的 index
    const id = typeof toolCall === 'string' ? toolCall : toolCall.id;
    if (!id) {
        return 0;
    }
    if (!callId2Index.has(id)) {
        callId2Index.set(id, callId2Index.size);
    }
    return callId2Index.get(id)!;
}


/**
 * @description 单次调用的索引适配器（暂未实现）
 * @param toolCall 工具调用对象
 * @returns 固定返回0
 */
export function singleCallIndexAdapter(toolCall: ToolCall): IToolCallIndex {
    // TODO: 等待后续支持
    return 0;
}

/**
 * @description
 * @param toolCall 
 * @returns 
 */
export function defaultIndexAdapter(toolCall: ToolCall): IToolCallIndex {
    return toolCall.index || 0;
}

export function getToolCallIndexAdapter(llm: BasicLlmDescription, chatData: ChatCompletionCreateParamsBase) {

    // 如果是 xml 模式，那么 index adapter 必须是 idAsIndexAdapter

    if (chatData.enableXmlWrapper) {
        const callId2Index = new Map<string, number>();
        return (toolCall: ToolCall) => idAsIndexAdapter(toolCall, callId2Index);
    }

    if (llm.userModel.startsWith('gemini')) {
        return singleCallIndexAdapter;
    }

    if (llm.userModel.startsWith('grok')) {
        const callId2Index = new Map<string, number>();
        return (toolCall: ToolCall) => idAsIndexAdapter(toolCall, callId2Index);
    }

    return defaultIndexAdapter;
}

export function getIdAsIndexAdapter() {
    const callId2Index = new Map<string, number>();
    return (toolCall: ToolCall) => idAsIndexAdapter(toolCall, callId2Index);
}