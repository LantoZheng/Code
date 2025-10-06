<template>
    <el-tooltip :content="t('prompts')" placement="top" effect="light">
        <div class="setting-button" @click="showChoosePrompt = true; saveCursorPosition();">
            <span class="iconfont icon-chat"></span>
        </div>
    </el-tooltip>

    <!-- 上下文长度设置 - 改为滑块形式 -->
    <el-dialog v-model="showChoosePrompt" :title="t('prompts')" width="400px">

        <div class="prompt-template-container-scrollbar" v-if="!selectPrompt">
            <PromptTemplates :tab-id="-1" @prompt-selected="prompt => selectPrompt = prompt" />
        </div>
        <div v-else>
            <PromptReader :tab-id="-1" :current-prompt-name="selectPrompt!.name"
                @prompt-get-response="msg => whenGetPromptResponse(msg)" />
        </div>

        <template #footer>
            <el-button v-if="selectPrompt" @click="selectPrompt = undefined;">{{ t('return') }}</el-button>
            <el-button @click="showChoosePrompt = false; selectPrompt = undefined;">{{ t("cancel") }}</el-button>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { createApp, inject, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import type { ChatStorage, EditorContext } from '../chat';
import type { PromptsGetResponse, PromptTemplate } from '@/hook/type';

import PromptTemplates from '@/components/main-panel/prompt/prompt-templates.vue';
import PromptReader from '@/components/main-panel/prompt/prompt-reader.vue';
import { ElMessage, ElTooltip } from 'element-plus';

import PromptChatItem from '../prompt-chat-item.vue';

const { t } = useI18n();

const tabStorage = inject('tabStorage') as ChatStorage;
let selectPrompt = ref<PromptTemplate | undefined>(undefined);
const showChoosePrompt = ref(false);

const editorContext = inject('editorContext') as EditorContext;
let savedSelection: Range | null = null;

function saveCursorPosition() {
    const editor = editorContext.editor.value;
    if (editor) {
        const selection = window.getSelection();
        if (selection && selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            // 检查 selection 是否在 editor 内部
            if (editor.contains(range.startContainer) && editor.contains(range.endContainer)) {
                savedSelection = range;
            } else {
                savedSelection = null;
            }
        }
    }
}

async function whenGetPromptResponse(msg: PromptsGetResponse) {
    try {
        const content = msg.messages[0].content;
        selectPrompt.value = undefined;
        const editor = editorContext.editor.value;

        if (!content || !editor) {
            return;
        }

        const container = document?.createElement('div');
        const promptChatItem = createApp(PromptChatItem, {
            messages: msg.messages
        });
        promptChatItem.use(ElTooltip);
        promptChatItem.mount(container);

        const firstElement = container.firstElementChild!;

        if (savedSelection) {
            
            savedSelection.deleteContents();
            savedSelection.insertNode(firstElement);            
        } else {
            editor.appendChild(firstElement);
        }

        // 设置光标到插入元素的后方
        const newRange = document?.createRange();
        newRange.setStartAfter(firstElement);
        newRange.collapse(true);
        const selection = window.getSelection();

        selection?.removeAllRanges();
        selection?.addRange(newRange);

        editor.dispatchEvent(new Event('input'));
        editor.focus();

        showChoosePrompt.value = false;
    } catch (error) {
        ElMessage.error((error as Error).message);
    }
}

</script>

<style>
.icon-length {
    font-size: 16px;
}
</style>