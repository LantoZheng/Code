<template>
    <el-tooltip :content="t('tool-use')" placement="top" effect="light">
        <div class="setting-button" :class="{ 'active': availableToolsNum > 0 }" size="small" @click="toggleTools">
            <span class="iconfont icon-tool badge-outer">
                <span class="badge-inner">
                    {{ availableToolsNum }}
                </span>
            </span>
        </div>

    </el-tooltip>

    <el-dialog v-model="showToolsDialog" width="800px">

        <template #header>
            <div>
                <span>{{ t('tool-manage') }}</span>
                <el-tooltip :content="t('enable-xml-wrapper')" placement="top" effect="light">
                    <span class="xml-tag" :class="{
                        'active': tabStorage.settings.enableXmlWrapper
                    }" @click="tabStorage.settings.enableXmlWrapper = !tabStorage.settings.enableXmlWrapper">xml</span>
                </el-tooltip>
            </div>
        </template>

        <div class="tools-dialog-container">
            <el-scrollbar height="400px" class="tools-list">
                <div v-for="(tool, index) in tabStorage.settings.enableTools" :key="index" class="tool-item">
                    <div class="tool-info">
                        <div class="tool-name">{{ tool.name }}</div>
                        <div v-if="tool.description" class="tool-description">{{ tool.description }}</div>
                    </div>
                    <el-switch v-model="tool.enabled" />
                </div>
            </el-scrollbar>

            <el-scrollbar height="400px" class="schema-viewer">
                <!-- 如果激活 xml 指令包裹，则展示对应的 prompt -->
                <div v-if="tabStorage.settings.enableXmlWrapper" v-html="activeToolsXmlPrompt" />
                <!-- 如果是普通模式，则展示普通的工具列表 -->
                <div v-else v-html="activeToolsSchemaHTML" />
            </el-scrollbar>
        </div>
        <template #footer>
            <el-button type="primary" @click="enableAllTools">{{ t('enable-all-tools') }}</el-button>
            <el-button type="danger" @click="disableAllTools">{{ t('disable-all-tools') }}</el-button>
            <el-button type="primary" @click="showToolsDialog = false">{{ t("cancel") }}</el-button>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, inject, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { type ChatStorage, type EnableToolItem, getToolSchema } from '../chat';
import { markdownToHtml } from '@/components/main-panel/chat/markdown/markdown';
import { mcpClientAdapter } from '@/views/connect/core';
import { toolSchemaToPromptDescription } from '../../core/xml-wrapper';

const { t } = useI18n();

const tabStorage = inject('tabStorage') as ChatStorage;

const showToolsDialog = ref(false);

const availableToolsNum = computed(() => {
    return tabStorage.settings.enableTools.filter(tool => tool.enabled).length;
});

// 修改 toggleTools 方法
const toggleTools = () => {
    showToolsDialog.value = true;
};


const activeToolsSchemaHTML = computed(() => {
    const toolsSchema = getToolSchema(tabStorage.settings.enableTools);
    const jsonString = JSON.stringify(toolsSchema, null, 2);

    return markdownToHtml(
        "```json\n" + jsonString + "\n```"
    );
});

const activeToolsXmlPrompt = computed(() => {    
    const prompt = toolSchemaToPromptDescription(tabStorage.settings.enableTools);
    return markdownToHtml(
        "```markdown\n" + prompt + "\n```"
    );
});

// 新增方法 - 激活所有工具
const enableAllTools = () => {
    tabStorage.settings.enableTools.forEach(tool => {
        tool.enabled = true;
    });
};

// 新增方法 - 禁用所有工具
const disableAllTools = () => {
    tabStorage.settings.enableTools.forEach(tool => {
        tool.enabled = false;
    });
};

// 更新工具列表的方法
const updateToolsList = async () => {
    // 将新的 tool 和并进入 tabStorage.settings.enableTools 中
    // 只需要保证 enable 信息同步即可，其余工具默认开启
    const disableToolNames = new Set<string>(
        tabStorage.settings.enableTools
            .filter(tool => !tool.enabled)
            .map(tool => tool.name)
    );

    const newTools: EnableToolItem[] = [];

    for (const client of mcpClientAdapter.clients) {
        const tools = await client.getTools({ cache: false });
        if (tools) {
            for (const tool of tools.values()) {
                const enabled = !disableToolNames.has(tool.name);

                newTools.push({
                    name: tool.name,
                    description: tool.description,
                    inputSchema: tool.inputSchema,
                    enabled
                });
            }
        }
    }

    tabStorage.settings.enableTools = newTools;
}



onMounted(async () => {
    await updateToolsList();
    watch(() => mcpClientAdapter.refreshSignal.value, async () => {
        await updateToolsList();
    });
});

</script>

<style scoped>
.xml-tag {
    margin-left: 10px;
    border-radius: .5em;
    padding: 2px 5px;
    font-size: 12px;
    font-weight: 900;
    color: black;
    background-color: var(--main-color);
    opacity: 0.3;
    transition: var(--animation-3s);
    cursor: pointer;
}

.xml-tag.active {
    opacity: 1;
    transition: var(--animation-3s);
}
</style>