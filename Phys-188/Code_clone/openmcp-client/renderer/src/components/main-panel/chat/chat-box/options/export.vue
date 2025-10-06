<template>
    <el-tooltip :content="'导出 mcpconfig'" placement="top" effect="light">
        <div class="setting-button" @click="toggleDialog">
            <span class="iconfont icon-deploy">
            </span>
        </div>

    </el-tooltip>

    <el-dialog v-model="showDialog" width="800px">

        <template #header>
            <div>
                <div class="export-file-input">
                    <span>{{ t('export-filename') }}</span>
                    <el-input
                        v-model="exportFileName"
                        style="max-width: 300px"
                    >
                        <template #append>.json</template>
                    </el-input>
                    <span class="how-to-use"
                        @click="gotoHowtoUse"
                    >
                        <span class="iconfont icon-info"></span>
                        <span style="font-weight: 200;">{{ t('how-to-use') }}</span>
                    </span>
                </div>
            </div>
        </template>

        <div class="tools-dialog-container">
            <el-scrollbar height="400px" class="tools-list">
                <div v-html="exportJson">
                </div>
            </el-scrollbar>
<!-- 
            <el-scrollbar height="400px" class="tools-list">
                <div v-html="exampleCode"></div>
            </el-scrollbar> -->
        </div>

        <template #footer>
            <el-button type="primary" @click="copyCode">{{ t('copy') }}</el-button>
            <el-button type="primary" @click="exportCode">{{ t('export') }}</el-button>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, inject, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { type ChatStorage, type EnableToolItem, getToolSchema } from '../chat';
import { markdownToHtml } from '@/components/main-panel/chat/markdown/markdown';
import { llmManager, llms } from '@/views/setting/llm';
import { mcpClientAdapter } from '@/views/connect/core';
import { ElMessage } from 'element-plus';
import { useMessageBridge } from '@/api/message-bridge';
import { gotoWebsite } from '@/hook/util';

const { t, locale } = useI18n();

const showDialog = ref(false);
const exportJson = ref('');
const exportFileName = ref('mcpconfig');

// 修改 toggleDialog 方法
const toggleDialog = () => {
    showDialog.value = true;
};

const generateExportData = computed(() => {
    const currentLLM = llms[llmManager.currentModelIndex];

    const mcpServers = {} as any;
    for (const client of mcpClientAdapter.clients) {

        const option = client.connectOption;
        const type = option.connectionType;

        if (type === 'STDIO') {
            mcpServers[client.name] = {
                type: 'stdio',
                command: option.command,
                args: option.args,
                cwd: option.cwd,
                description: "",
            }
        } else if (type === 'SSE') {
            mcpServers[client.name] = {
                type: 'sse',
                url: option.url,
                description: "",
            }
        } else {
            mcpServers[client.name] = {
                type: 'http',
                url: option.url,
                description: "",
            }
        }

        if (client.connectionEnvironment.data.length > 0) {
            const env = {} as Record<string, string>;
            for (const item of client.connectionEnvironment.data) {
                env[item.key] = item.value;
            }

            mcpServers[client.name].env = env;
        }
    }

    const mcpconfig = {
        version: "0.0.1",
        namespace: "openmcp",
        mcpServers,
        defaultLLM: {
            baseURL: currentLLM.baseUrl,
            apiToken: currentLLM.userToken,
            model: currentLLM.userModel
        }
    };

    return JSON.stringify(mcpconfig, null, 2);
});

const innerMarkdownHtml = (code: string) => {
    const rawCode = markdownToHtml(code);
    const doc = new DOMParser().parseFromString(rawCode, 'text/html');
    const pres = doc.querySelectorAll('pre');

    if (pres.length < 2) {
        return '';
    }

    const inner = pres[1].outerHTML;
    return inner;
}

const exampleCode = computed(() => {
    return innerMarkdownHtml(
        '```typescript\n' +
        `import { OmAgent } from 'openmcp-sdk/service/sdk';

const agent = new OmAgent();

agent.loadMcpConfig('/path/to/${exportFileName.value}.json');

const prompt = await agent.getPrompt('hacknews', { topn: '5' });    
const res = await agent.ainvoke({ messages: prompt });

console.log('⚙️ Agent Response', res);
` +
        '\n```'
    );
});

const copyCode = async () => {
    try {
        await navigator.clipboard.writeText(generateExportData.value);
        ElMessage.success(t('copy-success'));
    } catch (error) {
        ElMessage.error(t('copy-fail'));
    }
}

const exportCode = async () => {
    const bridge = useMessageBridge();
    bridge.postMessage({
        command: 'vscode/export-file',
        data: {
            filename: exportFileName.value,
            content: generateExportData.value
        }
    })
}

const gotoHowtoUse = () => {
    if (locale.value === 'zh') {
        gotoWebsite('https://openmcp.kirigaya.cn/zh/sdk-tutorial/#%E4%BD%BF%E7%94%A8');
    } else if (locale.value === 'ja') {
        gotoWebsite('https://openmcp.kirigaya.cn/ja/sdk-tutorial/#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95');
    } else {
        gotoWebsite('https://openmcp.kirigaya.cn/sdk-tutorial/#usage');
    }
}

onMounted(async () => {
    exportJson.value = innerMarkdownHtml(
        '```json\n' + generateExportData.value + '\n```'
    );
});

</script>

<style scoped>

.export-file-input {
    display: flex;
    gap: 10px;
    align-items: center;
}

.tools-list {
    border-radius: .5em;
    border: 1px solid var(--main-color);
    padding: 5px;
}

.how-to-use {
    margin-left: 10px;
    font-size: 15px;
    cursor: pointer;
    background-color: var(--main-color);
    color: #1e1e1e;
    padding: 3px 5px;
    border-radius: .3em;
}

</style>
