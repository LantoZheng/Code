import { parseString } from 'xml2js';
import { MessageState, type ToolCall } from '../chat-box/chat';
import { mcpClientAdapter } from '@/views/connect/core';
import { handleToolResponse, type IToolCallIndex, type ToolCallResult } from './handle-tool-calls';
import type { ChatStorage, EnableToolItem } from "../chat-box/chat";
import type { ToolCallContent } from '@/hook/type';

export interface XmlToolCall {
    server: string;
    name: string;
    callId: string;
    parameters: Record<string, string>;
}


export function toolSchemaToPromptDescription(enableTools: EnableToolItem[]) {
    let prompt = '';

    const tools = enableTools.filter(tool => tool.enabled);
    
    // 无参数的工具
    const noParamTools = tools.filter(tool => 
        !tool.inputSchema.required || tool.inputSchema.required.length === 0
    );
    
    if (noParamTools.length > 0) {
        noParamTools.forEach(tool => {
            prompt += `- ${tool.name}\n`;
            prompt += `**Description**: ${tool.description}\n\n`;
        });
    }
    
    // 有参数的工具
    const paramTools = tools.filter(tool => 
        tool.inputSchema.required && tool.inputSchema.required.length > 0
    );
    
    if (paramTools.length > 0) {
        paramTools.forEach(tool => {
            prompt += `- ${tool.name}\n`;
            prompt += `**Description**: ${tool.description}\n`;
            prompt += `**Parameters**:\n`;
            
            Object.entries(tool.inputSchema.properties).forEach(([name, prop]) => {
                const required = tool.inputSchema.required?.includes(name) || false;
                prompt += `- \`${name}\`: ${prop.description || 'No Description'} (${prop.type}) ${required ? '(required)' : ''}\n`;
            });
            
            prompt += '\n';
        });
    }
    
    return prompt;
}

export function getXmlWrapperPrompt(tools: EnableToolItem[], tabStorage: ChatStorage) {

    const toolPrompt = toolSchemaToPromptDescription(tools);
    const requests = [
        `ALWAYS analyze what function calls would be appropriate for the task`,
        `ALWAYS format your function call usage EXACTLY as specified in the schema`,
        `NEVER skip required parameters in function calls`,
        `NEVER invent functions that arent available to you`,
        `ALWAYS wait for function call execution results before continuing`,
        `After invoking a function, wait for the output in <function_results> tag and then continue with your response`,
        `NEVER mock or form <function_results> on your own, it will be provided to you after the execution`,
    ];

    if (!tabStorage.settings.parallelToolCalls) {
        requests.push(`NEVER invoke multiple functions in a single response`);
    }

    const requestString = requests.map((text, index) => {
        return `${index + 1}. ${text}`;
    }).join('\n');

    return `
[Start Fresh Session from here]

<SYSTEM>
You are OpenMCP Assistant with the capabilities of invoke functions and make the best use of it during your assistance, a knowledgeable assistant focused on answering questions and providing information on any topics.
In this environment you have access to a set of tools you can use to answer the user's question.
You have access to a set of functions you can use to answer the user's question. You do NOT currently have the ability to inspect files or interact with external resources, except by invoking the below functions.

Function Call Structure:
- All function calls should be wrapped in 'xml' codeblocks tags like \`\`\`xml ... \`\`\`. This is strict requirement.
- Wrap all function calls in 'function_calls' tags
- Each function call uses 'invoke' tags with a 'name' attribute
- Parameters use 'parameter' tags with 'name' attributes
- Parameter Formatting:
  - String/scalar parameters: written directly as values
  - Lists/objects: must use proper JSON format
  - Required parameters must always be included
  - Optional parameters should only be included when needed
  - If there is xml inside the parameter value, do not use CDATA for wrapping it, just give the xml directly

The instructions regarding 'invoke' specify that:
- When invoking functions, use the 'invoke' tag with a 'name' attribute specifying the function name.
- The invoke tag must be nested within an 'function_calls' block.
- Parameters for the function should be included as 'parameter' tags within the invoke tag, each with a 'name' attribute.
- Include all required parameters for each function call, while optional parameters should only be included when necessary.
- String and scalar parameters should be specified directly as values, while lists and objects should use proper JSON format.
- Do not refer to function/tool names when speaking directly to users - focus on what I'm doing rather than the tool I'm using.
- When invoking a function, ensure all necessary context is provided for the function to execute properly.
- Each 'invoke' tag should represent a single, complete function call with all its relevant parameters.
- DO not generate any <function_calls> tag in your thinking/resoning process, because those will be interpreted as a function call and executed. just formulate the correct parameters for the function call.

The instructions regarding 'call_id="$CALL_ID">
- It is a unique identifier for the function call.
- It is a number that is incremented by 1 for each new function call, starting from 1.

You can invoke one or more functions by writing a "<function_calls>" block like the following as part of your reply to the user, MAKE SURE TO INVOKE ONLY ONE FUNCTION AT A TIME, meaning only one '<function_calls>' tag in your output :

<Example>
\`\`\`xml
<function_calls>
<invoke name="$FUNCTION_NAME" call_id="$CALL_ID">
<parameter name="$PARAMETER_NAME_1">$PARAMETER_VALUE</parameter>
<parameter name="$PARAMETER_NAME_2">$PARAMETER_VALUE</parameter>
...
</invoke>
</function_calls>
\`\`\`
</Example>

String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.

When a user makes a request:
${requestString}

Answer the user's request using the relevant tool(s), if they are available. Check that all the required parameters for each tool call are provided or can reasonably be inferred from context. IF there are no relevant tools or there are missing values for required parameters, ask the user to supply these values; otherwise proceed with the tool calls. If the user provides a specific value for a parameter (for example provided in quotes), make sure to use that value EXACTLY. DO NOT make up values for or ask about optional parameters. Carefully analyze descriptive terms in the request as they may indicate required parameter values that should be included even if not explicitly quoted.

<Output Format>
<Start HERE>
## Thoughts
  - User Query Elaboration:
  - Thoughts:
  - Observations:
  - Solutions:
  - Function to be used:
  - call_id: $CALL_ID + 1 = $CALL_ID

\`\`\`xml
<function_calls>
<invoke name="$FUNCTION_NAME" call_id="$CALL_ID">
<parameter name="$PARAMETER_NAME_1">$PARAMETER_VALUE</parameter>
<parameter name="$PARAMETER_NAME_2">$PARAMETER_VALUE</parameter>
...
</invoke>
</function_calls>
\`\`\`
<End HERE>
</Output Format>

Do not use <Start HERE> and <End HERE> in your output, that is just output format reference to where to start and end your output.
## AVAILABLE TOOLS FOR SUPERASSISTANT

${toolPrompt}

- list_servers
**Description**: List all connected MCP servers and their capabilities

- get_server_info
**Description**: Get detailed information about a specific server
**Parameters**:
- \`serverName\`: Name of the server to get info for (string) (required)
</SYSTEM>

User Interaction Starts here:

`.trim();
}


export function getXmlResultPrompt(callId: string, result: string) {
    return `
\`\`\`xml
<function_results>
<result call_id="${callId}">
${result}
</result>
</function_results>
\`\`\`
    `.trim() + '\n\n';
}

export function getXmlsFromString(content: string) {
    const matches = content.matchAll(/```xml\n([\s\S]*?)\n```/g);
    return Array.from(matches).map(match => match[1].trim());
}


export async function getToolCallFromXmlString(xmlString: string): Promise<XmlToolCall | null> {
    try {
        const result = await new Promise<any>((resolve, reject) => {
            parseString(xmlString, (err, result) => {
                if (err) reject(err);
                else resolve(result);
            });
        });

        if (!result?.function_calls?.invoke) {
            return null;
        }

        const invoke = result.function_calls.invoke[0].$;
        const parameters: Record<string, any> = {};

        if (result.function_calls.invoke[0].parameter) {
            result.function_calls.invoke[0].parameter.forEach((param: any) => {
                const name = param.$.name as string;
                parameters[name] = param._;
            });
        }

        // name 可能是 neo4j-mcp.executeReadOnlyCypherQuery
        return {
            server: '',
            name: invoke.name,
            callId: invoke.call_id,
            parameters
        };
    } catch (error) {
        console.error('Failed to parse function calls:', error);
        return null;
    }
}


export async function getToolResultFromXmlString(xmlString: string) {
    try {
        const result = await new Promise<any>((resolve, reject) => {
            parseString(xmlString, (err, result) => {
                if (err) reject(err);
                else resolve(result);
            });
        });

        if (!result?.function_results?.result) {
            return null;
        }

        const resultData = result.function_results.result[0];
        const callId = resultData.$.call_id;
        
        // 提取所有评论文本
        const toolcallContent = [] as ToolCallContent[];
        const content = resultData._;

        toolcallContent.push({
            type: 'text',
            text: content
        });

        return {
            callId,
            toolcallContent
        };
    } catch (error) {
        console.error('Failed to parse function results:', error);
        return null;
    }
}

export function toNormaliseToolcall(xmlToolcall: XmlToolCall, toolcallIndexAdapter: (toolCall: ToolCall) => IToolCallIndex): ToolCall {
    const toolcall = {
        id: xmlToolcall.callId,
        index: -1,
        type: 'function',
        function: {
            name: xmlToolcall.name,
            arguments: JSON.stringify(xmlToolcall.parameters)
        }
    } as ToolCall;

    toolcall.index = toolcallIndexAdapter(toolcall);

    return toolcall;
}

export async function handleXmlWrapperToolcall(toolcall: XmlToolCall): Promise<ToolCallResult> {
    if (!toolcall) {
        return {
            index: 0,
            id: '',
            content: [{
                type: 'error',
                text: 'invalid xml'
            }],
            state: MessageState.InvalidXml
        }
    }
    
    const toolResponse = await mcpClientAdapter.callTool(toolcall.name, toolcall.parameters);
    const response = handleToolResponse(toolResponse);
    return {
        index: 0,
        id: toolcall.callId,
        ...response
    };
}