<template>
    <div class="message-role">
        <span class="message-reminder" v-if="callingTools">
            Agent {{ t('using-tool') }}
            <span class="tool-loading iconfont icon-double-loading">
            </span>
        </span>
    </div>
    <div class="message-text tool_calls" :class="[currentMessageLevel]">
        
        <!-- 工具的消息 -->
        <div v-if="props.message.content" v-html="markdownToHtml(props.message.content)"></div>

        <!-- 工具的调用 -->
        <el-collapse v-model="activeNames" v-if="props.message.tool_calls">
            <el-collapse-item name="tool">
                <template #title>
                    <div class="tool-calls">
                        <div class="tool-call-header">
                            <span class="tool-name">
                                <span class="iconfont icon-tool"></span>

                                {{ props.message.tool_calls[0].function!.name }}
                            </span>
                            <el-button size="small" @click="createTest(props.message.tool_calls[0])">
                                <span class="iconfont icon-send"></span>
                            </el-button>
                        </div>
                    </div>
                </template>

                <div v-for="(toolResult, toolIndex) in props.message.toolResults" :key="toolIndex"
                    class="toolcall-item">

                    <div class="tool-calls" v-if="toolIndex > 0">
                        <div class="tool-call-header">
                            <span class="tool-name">
                                <span class="iconfont icon-tool"></span>

                                {{ props.message.tool_calls[toolIndex].function!.name }}
                            </span>
                            <el-button size="small" @click="createTest(props.message.tool_calls[toolIndex])">
                                <span class="iconfont icon-send"></span>
                            </el-button>
                        </div>
                    </div>

                    <div class="tool-arguments">
                        <json-render :json="parseArguments(props.message.tool_calls[toolIndex].function!.arguments)"/>
                    </div>

                    <!-- 工具调用结果 -->
                    <div v-if="toolResult.length > 0">
                        <div class="tool-call-header result">

                            <span class="tool-name" v-if="isValid(toolResult)">
                                <span :class="`iconfont icon-info`"></span>
                                {{ t("response") }}
                            </span>
                            <span class="tool-name" v-else>
                                <span :class="`iconfont icon-${currentMessageLevel}`"></span>
                                {{ isValid(toolResult) ? t("response") : t('error') }}
                                <el-button size="small" @click="gotoIssue()">
                                    {{ t('feedback') }}
                                </el-button>
                            </span>


                            <span v-if="currentMessageLevel === 'info'"
                                style="width: 200px;" class="tools-dialog-container"
                            >
                                <el-switch v-model="showJsons[toolIndex]" inline-prompt active-text="JSON"
                                    inactive-text="Text" style="margin-left: 10px; width: 200px;"
                                    :inactive-action-style="'backgroundColor: var(--sidebar)'" />
                            </span>
                        </div>

                        <div class="tool-result" v-if="isValid(toolResult)">
                            <!-- 展示 JSON -->
                            <div v-if="showJsons[toolIndex]" class="tool-result-content">
                                <json-render :json="props.message.toolResults[toolIndex]"/>
                            </div>

                            <!-- 展示富文本 -->
                            <span v-else>
                                <div v-for="(item, index) in props.message.toolResults[toolIndex]" :key="index"
                                    class="response-item">
                                    <ToolcallResultItem :item="item"
                                        @update:item="value => updateToolCallResultItem(value, toolIndex, index)"
                                        @update:ocr-done="value => collposePanel()" />
                                </div>
                            </span>
                        </div>
                        <div v-else class="tool-result">
                            <div class="tool-result-content" v-for="(error, index) of collectErrors(toolResult)"
                                :key="index">
                                {{ error }}
                            </div>
                        </div>
                    </div>
                    <div v-else style="width: 90%">
                        <div class="tool-call-header result">
                            <span class="tool-name">
                                <span :class="`iconfont icon-waiting`"></span>
                                {{ t('waiting-mcp-server') }}
                            </span>
                        </div>
                        <div class="tool-result-content">
                            <div class="progress">
                                <el-progress :percentage="100" :format="() => ''" :indeterminate="true" text-inside />
                            </div>
                        </div>
                    </div>

                    <MessageMeta v-if="toolIndex === props.message.toolResults.length - 1" :message="message" />

                </div>
            </el-collapse-item>
        </el-collapse>
    
    </div>
</template>

<script setup lang="ts">
import { defineProps, ref, watch, type PropType, computed, defineEmits } from 'vue';
import { useI18n } from 'vue-i18n';

import MessageMeta from './message-meta.vue';
import { markdownToHtml } from '@/components/main-panel/chat/markdown/markdown';
import { createTest } from '@/views/setting/llm';
import { type IToolRenderMessage, MessageState } from '../chat-box/chat';
import type { ToolCallContent } from '@/hook/type';

import ToolcallResultItem from './toolcall-result-item.vue';
import JsonRender from '@/components/json-render/index.vue';


const { t } = useI18n();
const props = defineProps({
    message: {
        type: Object as PropType<IToolRenderMessage>,
        required: true
    },
    tabId: {
        type: Number,
        required: true
    }
});

const hasOcr = computed(() => {
    if (props.message.role === 'assistant/tool_calls') {
        for (const toolResult of props.message.toolResults) {
            for (const item of toolResult) {
                const metaInfo = item._meta || {};
                const { ocr = false } = metaInfo;
                if (ocr) {
                    return true;
                }
            }
        }
    }

    return false;
});


const callingTools = computed(() => {
    const emptyToolResult = props.message.toolResults.find(item => item.length === 0);    

    if (emptyToolResult) {
        return true;
    }

    return false;
});

const showJsons = ref<boolean[]>([]);
props.message.toolResults.forEach(() => {
    showJsons.value.push(false);
});

const activeNames = ref<string[]>(callingTools.value ? ['tool']: []);

watch(
    () => props.message,
    (value, _) => {
        if (hasOcr.value) {
            return;
        }

        if (value) {
            collposePanel();
        }
    }
);

function collposePanel() {
    setTimeout(() => {
        activeNames.value = [''];
    }, 1000);
}


function gotoIssue() {
    window.open('https://github.com/LSTM-Kirigaya/openmcp-client/issues', '_blank');
}


function isValid(toolResult: ToolCallContent[]) {
    try {
        const item = toolResult[0];
        if (item.type === 'error') {
            return false;
        }
        return true;
    } catch {
        return false;
    }
}


const currentMessageLevel = computed(() => {

    // 此时正在等待 mcp server 给出回应
    for (const toolResult of props.message.toolResults) {
        if (toolResult.length === 0) {
            return 'info';
        }

        if (!isValid(toolResult)) {
            return 'error';
        }
    }

    if (props.message.extraInfo.state !== MessageState.Success) {
        return 'warning';
    }

    return 'info';
});


function collectErrors(toolResult: ToolCallContent[]) {
    const errorMessages = [];
    try {
        const errorResults = toolResult.filter(item => item.type === 'error');
        console.log(errorResults);

        for (const errorResult of errorResults) {
            errorMessages.push(errorResult.text);
        }
        return errorMessages;
    } catch {
        return errorMessages;
    }
}

const emits = defineEmits(['update:tool-result']);

function updateToolCallResultItem(value: any, toolIndex: number, index: number) {
    emits('update:tool-result', value, toolIndex, index);
}

function parseArguments(args: string | undefined): object {
    try {
        return JSON.parse(args || '{}');
    } catch {
        return { rawArgs: args || '' };
    }
}

</script>

<style>
.message-text.tool_calls {
    border: 1px solid var(--main-color);
    border-radius: .5em;
    padding: 3px 10px;
}

.tool-result-content .progress {
    border-radius: .5em;
    background-color: var(--el-fill-color-light) !important;
    padding: 20px 10px;
    width: 50%;
}

.message-text.tool_calls.warning {
    border: 1px solid var(--el-color-warning);
}

.message-text.tool_calls.warning .tool-name {
    color: var(--el-color-warning);
}

.message-text.tool_calls.warning .tool-result {
    background-color: rgba(230, 162, 60, 0.5);
}

.message-text.tool_calls.error {
    border: 1px solid var(--el-color-error);
}

.message-text.tool_calls.error .tool-name {
    color: var(--el-color-error);
}

.message-text.tool_calls.error .tool-result {
    background-color: rgba(245, 108, 108, 0.5);
}


.message-text .el-collapse-item__header {
    display: flex;
    align-items: center;
    height: fit-content;
}

.message-text .el-collapse-item__content {
    padding-bottom: 5px;
}

.toolcall-item .tool-calls {
    margin-top: 22px;
}

.tool-call-item {
    margin-bottom: 10px;
}

.tool-call-header {
    display: flex;
    align-items: center;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}

.tool-call-header.result {
    margin-top: 10px;
}

.tool-name {
    font-weight: bold;
    color: var(--el-color-primary);
    margin-right: 8px;
    margin-bottom: 0;
    display: flex;
    align-items: center;
    height: 26px;
    display: flex;
    align-items: center;
}

.tool-name .iconfont {
    margin-right: 5px;
}

.tool-type {
    font-size: 0.8em;
    color: var(--el-text-color-secondary);
    background-color: var(--el-fill-color-light);
    padding: 2px 6px;
    display: flex;
    align-items: center;
    border-radius: 4px;
    margin-right: 10px;
    height: 22px;
}

.response-item {
    margin-bottom: 10px;
}

.tool-arguments {
    margin: 0;
    padding: 8px;
    background-color: var(--el-fill-color-light);
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9em;
}

.tool-result {
    padding: 8px;
    background-color: var(--el-fill-color-light);
    border-radius: 4px;
}

.tool-text {
    white-space: pre-wrap;
    line-height: 1.6;
}

.tool-other {
    font-family: monospace;
    font-size: 0.9em;
    color: var(--el-text-color-secondary);
    margin-top: 4px;
}
</style>