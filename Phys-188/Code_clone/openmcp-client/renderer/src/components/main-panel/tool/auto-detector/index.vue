<template>
    <el-dialog v-model="showDialog" width="800px" class="no-padding-dialog">
        <template #header>
            <div style="display: flex; align-items: center;">
                <span>Tool Diagram</span>
                &ensp;
                <!-- 重置按钮弹出下拉列表 -->
                <el-popover placement="bottom" width="180" trigger="click" v-model:visible="resetPopoverVisible">
                    <template #reference>
                        <el-button size="small" type="primary">
                            {{ t("preset") }}
                        </el-button>
                    </template>
                    <div style="display: flex; gap: 8px;">
                        <el-button size="small" @click="tomoPreset('serial')">
                            <span class="iconfont icon-serial"></span>
                        </el-button>
                        <el-button size="small" @click="tomoPreset('parallel')">
                            <span class="iconfont icon-parallel"></span>
                        </el-button>
                    </div>
                </el-popover>
                <!-- 原有自检程序弹出表单 -->
                <el-popover placement="top" width="350" trigger="click" v-model:visible="testFormVisible">
                    <template #reference>
                        <el-button size="small" type="primary">
                            {{ t('start-auto-detect') }}
                        </el-button>
                    </template>
                    <!-- ...原有自检表单内容... -->
                    <el-input type="textarea" v-model="testPrompt" :rows="2" style="margin-bottom: 8px;"
                        placeholder="请输入 prompt" />
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <el-switch v-model="enableXmlWrapper" style="margin-right: 8px;" />
                        <span :style="{
                            opacity: enableXmlWrapper ? 1 : 0.7,
                            color: enableXmlWrapper ? 'var(--main-color)' : undefined
                        }">XML</span>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <el-switch v-model="enableParallelTest" style="margin-right: 8px;" />
                        <span :style="{
                            opacity: enableParallelTest ? 1 : 0.7,
                            color: enableParallelTest ? 'var(--main-color)' : undefined
                        }">{{ t('parallel-test') }}</span>
                    </div>
                    <div style="text-align: right;">
                        <el-button size="small" @click="testFormVisible = false">{{ t("cancel") }}</el-button>
                        <el-button size="small" type="primary" @click="onTestConfirm">
                            {{ t("confirm") }}
                        </el-button>
                    </div>
                </el-popover>
            </div>
        </template>
        <el-scrollbar height="80vh">
            <Diagram :tab-id="props.tabId" />
        </el-scrollbar>

        <div class="caption" v-if="showCaption">
            {{ caption }}
        </div>
        <div v-else>
            <span class="caption">
                <el-tooltip placement="top" effect="light" :content="t('self-detect-caption')">
                    <span class="iconfont icon-about"></span>
                </el-tooltip>
            </span>
        </div>
    </el-dialog>
</template>

<script setup lang="ts">
import { computed, nextTick, provide, ref } from 'vue';
import Diagram from './diagram.vue';
import { makeNodeTest, topoSortParallel, type DiagramContext } from './diagram';
import { ElMessage } from 'element-plus';

import { useI18n } from 'vue-i18n';
import type { ToolStorage } from '../tools';
import { tabs } from '../../panel';

const { t } = useI18n();

const caption = ref('');
const showCaption = ref(false);

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false
    },
    tabId: {
        type: Number,
        required: true
    }
});
const emit = defineEmits(['update:modelValue']);

const showDialog = computed({
    get: () => props.modelValue,
    set: v => emit('update:modelValue', v)
});

function setCaption(text: string) {
    caption.value = text;
    if (caption.value) {
        nextTick(() => {
            showCaption.value = true;
        });
    } else {
        nextTick(() => {
            showCaption.value = false;
        });
    }
}

const context: DiagramContext = {
    preset: () => { },
    render: () => { },
    resetDataView: () => { },
    state: undefined,
    setCaption
};

provide('context', context);

const tab = tabs.content[props.tabId];
const tabStorage = tab.storage as ToolStorage;
const autoDetectDiagram = tabStorage.autoDetectDiagram;

if (autoDetectDiagram) {
    // ...
} else {
    tabStorage.autoDetectDiagram = {
        edges: [],
        views: []
    };
}

// 新增：自检参数表单相关
const testFormVisible = ref(false);
const enableXmlWrapper = ref(false);
const enableParallelTest = ref(true);
const testPrompt = ref('please call the tool {tool} to make some test');

async function onTestConfirm() {
    testFormVisible.value = false;
    const state = context.state;

    tabStorage.autoDetectDiagram!.views = [];

    // 先重制状态
    context.resetDataView();
    context.render();

    if (state) {
        const dispatches = topoSortParallel(state);

        if (enableParallelTest.value) {
            for (const nodeIds of dispatches) {

                await Promise.all(nodeIds.map(async id => {
                    const view = state.dataView.get(id);
                    if (view) {
                        await makeNodeTest(view, enableXmlWrapper.value, testPrompt.value, context);
                        tabStorage.autoDetectDiagram!.views!.push({
                            tool: view.tool,
                            status: view.status,
                            function: view.function,
                            result: view.result,
                            createAt: view.createAt,
                            finishAt: view.finishAt,
                            llmTimecost: view.llmTimecost,
                            toolcallTimecost: view.toolcallTimecost,
                        });
                        context.render();
                    }
                }));
            }
        } else {
            // 串行测试模式：按拓扑顺序逐个测试
            for (const nodeIds of dispatches) {
                for (const id of nodeIds) {
                    const view = state.dataView.get(id);
                    if (view) {
                        await makeNodeTest(view, enableXmlWrapper.value, testPrompt.value, context);
                        tabStorage.autoDetectDiagram!.views!.push({
                            tool: view.tool,
                            status: view.status,
                            function: view.function,
                            result: view.result,
                            createAt: view.createAt,
                            finishAt: view.finishAt,
                            llmTimecost: view.llmTimecost,
                            toolcallTimecost: view.toolcallTimecost,
                        });
                        context.render();
                    }
                }
            }
        }
    } else {
        ElMessage.error('error');
    }
}

const resetPopoverVisible = ref(false);

function tomoPreset(type: string) {
    resetPopoverVisible.value = false;
    context.preset?.(type);
}
</script>

<style>
.no-padding-dialog {
    margin-top: 30px !important;
    width: 90vw !important;
}

.no-padding-dialog .caption {
    position: absolute;
    right: 30px;
    bottom: 10px;
    margin: 0 auto;
    width: fit-content;
    min-height: 32px;
    background: rgba(245, 247, 250, 0.05);
    border-radius: 8px;
    box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.06);
    color: var(--main-color);
    font-size: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px 16px;
    z-index: 10;
    transition: background 0.2s;
}
</style>