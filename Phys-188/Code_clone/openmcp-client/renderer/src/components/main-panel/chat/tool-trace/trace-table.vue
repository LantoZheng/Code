<template>
    <div class="trace-table-container">
        <div class="column-selector">
            <el-popover placement="bottom" :width="300" trigger="click">
                <template #reference>
                    <el-button size="small">
                        <i class="iconfont icon-setting" />
                        &ensp;{{ t('table-setting') }}
                    </el-button>
                </template>
                <div class="column-selector-content">
                    <div class="column-selector-title">{{ t('select-columns-to-display') }}</div>
                    <el-checkbox v-for="column in allColumns" :key="column.prop" v-model="column.visible"
                        :label="column.label" />
                </div>
            </el-popover>
        </div>

        <el-scrollbar height="75%" width="100%">
            <el-table :data="tableData" style="width: 100%" row-class-name="trace-table-row"
                @row-click="handleRowClick">
                <el-table-column v-for="column in visibleColumns" :key="column.prop" :prop="column.prop"
                    :label="column.label" :width="column.width" :align="column.align" :show-overflow-tooltip="true">
                    <template #default="scope">
                        <template v-if="column.prop === 'status' && scope.row">
                            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
                        </template>
                        <template v-else-if="column.prop === 'toolName' && scope.row && scope.row.toolNames">
                            <div class="tool-names-container">
                                {{ scope.row.toolNames[0] }}

                                <el-tag v-if="scope.row.toolNames.length > 1" type="info">
                                    {{ scope.row.toolNames.length - 1 }}+
                                </el-tag>

                            </div>
                        </template>
                    </template>
                </el-table-column>
            </el-table>
        </el-scrollbar>

        <!-- 详细信息对话框 -->
        <el-dialog v-model="dialogVisible" width="80%" :title="t('details')" :before-close="handleDialogClose">
            <div v-if="selectedRow">
                <el-descriptions :column="1" border>
                    <el-descriptions-item :label="t('type')">{{ selectedRow.type }}</el-descriptions-item>
                    <el-descriptions-item v-if="selectedRow.content" :label="t('content')">
                        <pre class="content-pre">{{ selectedRow.content }}</pre>
                    </el-descriptions-item>
                    <el-descriptions-item v-if="selectedRow.toolCalls" :label="t('tool-call')">
                        <el-scrollbar height="300px">
                            <div v-for="(toolCall, index) in selectedRow.toolCalls" :key="index" class="tool-call-item">
                                <el-descriptions :column="1" size="small">
                                    <el-descriptions-item :label="t('toolbar.search.name')">
                                        <code>{{ toolCall.function?.name }}</code>
                                    </el-descriptions-item>
                                    <el-descriptions-item :label="t('arguments')">
                                        <div class="arguments-pre">
                                            {{ toolCall.function?.arguments }}
                                        </div>
                                    </el-descriptions-item>
                                    <el-descriptions-item :label="t('result')">
                                        <div class="arguments-pre">
                                            {{ selectedRow.toolResults[index] }}
                                        </div>
                                    </el-descriptions-item>
                                </el-descriptions>
                            </div>
                        </el-scrollbar>
                    </el-descriptions-item>

                    <el-descriptions-item :label="t('input-token')">{{ selectedRow.inputTokens }}</el-descriptions-item>
                    <el-descriptions-item :label="t('output-token')">{{ selectedRow.outputTokens
                        }}</el-descriptions-item>
                    <el-descriptions-item :label="t('total-token')">{{ selectedRow.totalTokens }}</el-descriptions-item>
                    <el-descriptions-item :label="t('cache-hit-ratio')">{{ selectedRow.cacheHitRate
                        }}</el-descriptions-item>
                    <el-descriptions-item :label="t('cumulative-tokens')">{{ selectedRow.cumulativeTokens
                        }}</el-descriptions-item>
                    <el-descriptions-item :label="t('duration-ms')">{{ selectedRow.duration }}</el-descriptions-item>
                    <el-descriptions-item :label="t('status')">
                        <el-tag :type="selectedRow.statusType">{{ selectedRow.status }}</el-tag>
                    </el-descriptions-item>
                </el-descriptions>
            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">{{ t('close') }}</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps, computed, reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import type { IRenderMessage, IToolRenderMessage } from '../chat-box/chat';

import JsonRender from '@/components/json-render/index.vue';


const { t } = useI18n();

const props = defineProps<{
    renderMessages: IRenderMessage[];
}>();

// 定义所有列
const allColumns = reactive([
    { prop: 'index', label: '#', width: 60, align: 'left', visible: true },
    { prop: 'type', label: t('type'), width: 150, align: 'left', visible: true },
    { prop: 'toolName', label: t('toolbar.search.name') + '/' + t("content"), width: undefined, align: 'left', visible: true },
    { prop: 'inputTokens', label: t('input-token'), width: 120, align: 'right', visible: true },
    { prop: 'outputTokens', label: t('output-token'), width: 120, align: 'right', visible: true },
    { prop: 'totalTokens', label: t('total-token'), width: 120, align: 'right', visible: true },
    { prop: 'cacheHitRate', label: t('cache-hit-ratio'), width: 120, align: 'right', visible: true },
    { prop: 'cumulativeTokens', label: t('cumulative-tokens'), width: 150, align: 'right', visible: true },
    { prop: 'duration', label: t('duration-ms'), width: 120, align: 'right', visible: true },
    { prop: 'status', label: t('status'), width: 100, align: 'center', visible: true }
]);

// 计算可见列
const visibleColumns = computed(() => {
    return allColumns.filter(column => column.visible);
});

// 表格数据
const tableData = computed(() => {
    const data = [];
    let cumulativeTokens = 0;

    for (let i = 0; i < props.renderMessages.length; i++) {
        const message = props.renderMessages[i];

        // 计算耗时（当前节点与上一个节点的时间差）
        let duration = '-';
        if (i > 0 && props.renderMessages[i - 1].extraInfo?.created && message.extraInfo?.created) {
            const prevMessage = props.renderMessages[i - 1];
            duration = (message.extraInfo.created - prevMessage.extraInfo.created) + ' ms';
        }

        // 处理用户消息
        if (message.role === 'user') {
            const usage = message.extraInfo.usage;

            // 计算 token 信息
            const inputTokens = '-';
            const outputTokens = '-';
            const totalTokens = '-';
            const cacheHitTokens = '-';
            const cacheHitRate = '-';

            cumulativeTokens += 0;

            const renderContent = message.content.length > 50 ? message.content.substring(0, 50) + '...' : message.content;

            data.push({
                index: data.length + 1,
                type: t('user-input'),
                typeIndex: 0,
                content: message.content,
                toolNames: [renderContent],
                inputTokens,
                outputTokens,
                totalTokens,
                cacheHitRate,
                cumulativeTokens,
                duration: '-', // 用户输入没有耗时
                status: message.extraInfo.state === 'success' ? t('success') : t('failed'),
                statusType: message.extraInfo.state === 'success' ? 'success' : 'danger',
                rawMessage: message
            });
        }
        // 处理 assistant 消息（内容或工具调用）
        else if (message.role === 'assistant/content') {
            const usage = message.extraInfo.usage;

            // 计算 token 信息
            const inputTokens = usage?.prompt_tokens || 0;
            const outputTokens = usage?.completion_tokens || 0;
            const totalTokens = usage?.total_tokens || 0;
            const cacheHitTokens = usage?.prompt_tokens_details?.cached_tokens || 0;
            const cacheHitRate = inputTokens > 0 ? Math.round((cacheHitTokens / inputTokens) * 100) : 0;

            cumulativeTokens += totalTokens;
            const renderContent = message.content.length > 50 ? message.content.substring(0, 50) + '...' : message.content;

            data.push({
                index: data.length + 1,
                type: t('assistant-output'),
                typeIndex: 1,
                content: message.content,
                toolNames: [renderContent],
                inputTokens,
                outputTokens,
                totalTokens,
                cacheHitRate: cacheHitRate + '%',
                cumulativeTokens,
                duration,
                status: message.extraInfo.state === 'success' ? t('success') : t('failed'),
                statusType: message.extraInfo.state === 'success' ? 'success' : 'danger',
                rawMessage: message
            });
        }
        // 处理 assistant 工具调用消息
        else if (message.role === 'assistant/tool_calls' && 'tool_calls' in message) {
            const toolMessage = message as IToolRenderMessage;
            const usage = toolMessage.extraInfo.usage;

            // 计算 token 信息
            const inputTokens = usage?.prompt_tokens || 0;
            const outputTokens = usage?.completion_tokens || 0;
            const totalTokens = usage?.total_tokens || 0;
            const cacheHitTokens = usage?.prompt_tokens_details?.cached_tokens || 0;
            const cacheHitRate = inputTokens > 0 ? Math.round((cacheHitTokens / inputTokens) * 100) : 0;

            cumulativeTokens += totalTokens;

            // 将所有工具调用作为一个整体处理
            const toolNames = toolMessage.tool_calls.map(toolCall => toolCall.function?.name || '');

            const typeName = toolNames.length > 1 ?
                t('tool-call') + ` (${toolNames.length})` :
                t('tool-call');

            data.push({
                index: data.length + 1,
                type: typeName,
                typeIndex: 2,
                toolNames,
                toolCalls: toolMessage.tool_calls, // 所有工具调用
                toolResults: toolMessage.toolResults || [],
                inputTokens,
                outputTokens,
                totalTokens,
                cacheHitRate: cacheHitRate + '%',
                cumulativeTokens,
                duration,
                status: toolMessage.extraInfo.state === 'success' ? t('success') : t('failed'),
                statusType: toolMessage.extraInfo.state === 'success' ? 'success' : 'danger',
                rawMessage: toolMessage
            });
        }
    }

    return data;
});

// 对话框相关
const dialogVisible = ref(false);
const selectedRow = ref<any>(null);

// 处理行点击事件
const handleRowClick = (row: any) => {
    selectedRow.value = row;
    dialogVisible.value = true;
};

// 处理对话框关闭事件
const handleDialogClose = () => {
    dialogVisible.value = false;
    selectedRow.value = null;
};
</script>

<style scoped>
.trace-table-container {
    padding: 16px;
    height: 100%;
}

.column-selector {
    margin-bottom: 16px;
    text-align: left;
}

.column-selector-content {
    max-height: 300px;
}

.column-selector-title {
    font-weight: bold;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--el-border-color);
}

.trace-table-row {
    cursor: pointer;
}

.content-pre,
.result-pre {
    white-space: pre-wrap;
    word-break: break-all;
    margin: 0;
    padding: 8px;
    background-color: var(--el-fill-color-light);
    border-radius: 4px;
    max-height: 200px;
    overflow-y: auto;
}

.arguments-pre {
    white-space: pre-wrap;
    word-break: break-all;
    margin: 0;
    padding: 0 8px;
    background-color: var(--el-fill-color-light);
    border-radius: 4px;
    max-height: 200px;
    overflow-y: hidden;
}

.dialog-footer {
    text-align: right;
}

.tool-call-item,
.tool-result-item {
    margin-bottom: 10px;
}

.tool-call-item:last-child,
.tool-result-item:last-child {
    margin-bottom: 0;
}

.tool-names-container {
    display: flex;
    gap: 4px;
}
</style>