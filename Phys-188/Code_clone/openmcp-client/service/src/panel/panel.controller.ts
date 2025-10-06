import { Controller } from "../common/index.js";
import { PostMessageble } from "../hook/adapter.js";
import { RequestData } from "../common/index.dto.js";
import { getClient } from "../mcp/connect.service.js";
import { systemPromptDB } from "../hook/db.js";
import { loadTabSaveConfig, saveTabSaveConfig } from "./panel.service.js";

export class PanelController {
    @Controller('panel/save')
    async savePanel(data: RequestData, webview: PostMessageble) {
        const client = getClient(data.clientId);
        const serverInfo = client?.getServerVersion();
        saveTabSaveConfig(serverInfo, data);

        return {
            code: 200,
            msg: 'Settings saved successfully'
        };
    }

    @Controller('panel/load')
    async loadPanel(data: RequestData, webview: PostMessageble) {
        const client = getClient(data.clientId);
        const serverInfo = client?.getServerVersion();
        const config = loadTabSaveConfig(serverInfo);

        return {
            code: 200,
            msg: config
        };
    }

    @Controller('system-prompts/set')
    async setSystemPrompt(data: RequestData, webview: PostMessageble) {
        const client = getClient(data.clientId);
        const { name, content } = data;

        await systemPromptDB.insert({
            id: name,
            name,
            content
        });

        return {
            code: 200,
            msg: 'Settings saved successfully'
        }
    }

    @Controller('system-prompts/delete')
    async deleteSystemPrompt(data: RequestData, webview: PostMessageble) {
        const client = getClient(data.clientId);
        const { name } = data;
        await systemPromptDB.delete(name);
        return {
            code: 200,
            msg: 'Settings saved successfully'
        }
    }

    @Controller('system-prompts/save')
    async saveSystemPrompts(data: RequestData, webview: PostMessageble) {
        const client = getClient(data.clientId);
        const { prompts } = data;
        
        await Promise.all(prompts.map((prompt: any) => {
            systemPromptDB.insert({
                id: prompt.name,
                name: prompt.name,
                content: prompt.content
            })
        }));

        return {
            code: 200,
            msg: 'Settings saved successfully'
        }
    }

    @Controller('system-prompts/load')
    async loadSystemPrompts(data: RequestData, webview: PostMessageble) {
        const queryPrompts = await systemPromptDB.findAll();
        const prompts = [];
        for (const prompt of queryPrompts) {
            prompts.push({
                name: prompt.name,
                content: prompt.content
            })
        }
        
        return {
            code: 200,
            msg: prompts
        }
    }
}