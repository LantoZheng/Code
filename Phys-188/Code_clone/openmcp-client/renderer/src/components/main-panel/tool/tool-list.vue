<template>
    <el-collapse :expand-icon-position="'left'" v-model="tabStorage.activeNames">
        <el-collapse-item v-for="(client, index) in mcpClientAdapter.clients" :name="index" :class="[]">

            <!-- header -->
            <template #title>
                <h3 class="resource-template">
                    <span>tools/list</span>
                    <span class="iconfont icon-restart" @click.stop="reloadTools(client, { first: false })"></span>

                    <span>
                        <span class="cilent-name-tag">
                            {{ client.name }}
                        </span>
                    </span>
                </h3>
            </template>

            <!-- body -->
            <div class="tool-list-container-scrollbar">
                <el-scrollbar height="fit-content">
                    <div class="tool-list-container-scrollbar">
                        <el-scrollbar height="fit-content" v-if="(client.tools?.size || 0) > 0">
                            <div class="tool-list-container">
                                <div class="item" :class="{ 'active': tabStorage.currentToolName === tool.name }"
                                    v-for="tool of client.tools?.values()" :key="tool.name" @click="handleClick(tool)">
                                    <span>{{ tool.name }}</span>
                                    <br>
                                    <span class="tool-description">{{ tool.description || '' }}</span>
                                </div>
                            </div>
                        </el-scrollbar>
                        <div v-else style="padding: 10px;">
                            <div class="empty-description">
                                <span class="iconfont icon-empty"
                                    style="font-size: 22px; opacity: 0.4; margin-right: 6px;"></span>
                                <span style="opacity: 0.6;">No tools found.</span>
                            </div>
                        </div>
                    </div>
                </el-scrollbar>
            </div>
        </el-collapse-item>
    </el-collapse>
</template>

<script setup lang="ts">
import { onMounted, defineProps, type Reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import type { ToolStorage } from './tools';
import { tabs } from '../panel';
import { ElMessage } from 'element-plus';
import { McpClient, mcpClientAdapter } from '@/views/connect/core';

const { t } = useI18n();

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    }
});

const tab = tabs.content[props.tabId];
const tabStorage = tab.storage as ToolStorage;

async function reloadTools(client: Reactive<McpClient>, option: { first: boolean }) {
    await client.getTools({ cache: false });

    if (!option.first) {
        ElMessage({
            message: t('finish-refresh'),
            type: 'success',
            duration: 3000,
            showClose: true,
        });
    }
}

function handleClick(tool: { name: string }) {
    tabStorage.currentToolName = tool.name;
    tabStorage.lastToolCallResponse = undefined;
}

onMounted(async () => {
    if (tabStorage.currentToolName === undefined) {
        const masterNode = mcpClientAdapter.masterNode;
        const tool = masterNode.tools?.values().next();
        tabStorage.currentToolName = tool?.value?.name || '';
    }
});

</script>

<style>
.tool-list-container-scrollbar {
    background-color: var(--background);
    margin-bottom: 10px;
    border-radius: .5em;
}

.tool-list-container {
    height: fit-content;
    display: flex;
    flex-direction: column;
    padding: 10px;
}

.tool-list-function-container {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.tool-list-function-container button {
    width: 175px;
}

.tool-list-container>.item {
    margin: 3px;
    padding: 5px 10px;
    border-radius: .3em;
    user-select: none;
    cursor: pointer;
    align-items: center;
    justify-content: space-between;
    transition: var(--animation-3s);
}

.tool-list-container>.item:active {
	transform: scale(0.95);
	transition: var(--animation-3s);
}

.tool-list-container>.item:hover {
    background-color: var(--main-light-color);
    transition: var(--animation-3s);
}

.tool-list-container>.item.active {
    background-color: var(--main-light-color);
    transition: var(--animation-3s);
}

.tool-list-container>.item>span:first-child {
    min-width: 120px;
    max-width: 250px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex-shrink: 0;
}

.tool-list-container>.item>span:last-child {
    min-width: 120px;
    max-width: 250px;
    overflow: visible;
    white-space: normal;
    word-wrap: break-word;
}

.resource-template .cilent-name-tag {
    margin-left: 10px;
    background-color: var(--main-color);
    padding: 2px 5px;
    border-radius: .3em;
    height: fit-content;
    font-size: 13px;
    font-weight: 200;
    color: black;
}

.tool-description {
    opacity: 0.6;
    font-size: 12.5px;
}

.empty-description {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--el-text-color-placeholder, #bbb);
    font-size: 15px;
    min-height: 40px;
}
</style>