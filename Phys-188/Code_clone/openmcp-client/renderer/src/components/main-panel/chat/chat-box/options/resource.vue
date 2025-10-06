<template>
    <el-tooltip :content="t('resources')" placement="top" effect="light">
        <div class="setting-button" @click="showChooseResource = true; saveCursorPosition();">
            <span class="iconfont icon-file"></span>
        </div>
    </el-tooltip>

    <el-dialog v-model="showChooseResource" :title="t('resources')" width="400px">
        <div class="resource-template-container-scrollbar" v-if="!selectResource">
            <ResourceList :tab-id="-1" @resource-selected="resource => handleResourceSelected(resource)" />
        </div>
        <div v-else>
            <ResourceReader :tab-id="-1" :current-resource-name="selectResource!.name"
                @resource-get-response="msg => whenGetResourceResponse(msg)" />
        </div>

        <template #footer>
            <el-button v-if="selectResource" @click="selectResource = undefined;">{{ t('return') }}</el-button>
            <el-button @click="showChooseResource = false; selectResource = undefined;">{{ t("cancel") }}</el-button>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { createApp, inject, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import type { ChatStorage, EditorContext } from '../chat';
import type { Resources, ResourcesReadResponse, ResourceTemplate } from '@/hook/type';

import ResourceList from '@/components/main-panel/resource/resource-list.vue';
import ResourceReader from '@/components/main-panel/resource/resouce-reader.vue';
import { ElMessage, ElTooltip, ElProgress, ElPopover } from 'element-plus';

import ResourceChatItem from '../resource-chat-item.vue';
import { mcpClientAdapter } from '@/views/connect/core';

const { t } = useI18n();

const tabStorage = inject('tabStorage') as ChatStorage;
let selectResource = ref<ResourceTemplate | undefined>(undefined);
const showChooseResource = ref(false);

const editorContext = inject('editorContext') as EditorContext;
let savedSelection: Range | null = null;

function saveCursorPosition() {
    const editor = editorContext.editor.value;
    if (editor) {
        const selection = window.getSelection();
        if (selection && selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            if (editor.contains(range.startContainer) && editor.contains(range.endContainer)) {
                savedSelection = range;
            } else {
                savedSelection = null;
            }
        }
    }
}

async function handleResourceSelected(resource: Resources) {
    selectResource.value = undefined;
    const msg = await mcpClientAdapter.readResource(resource.uri);
    
    if (msg) {
        await whenGetResourceResponse(msg as ResourcesReadResponse);
    }
}

async function whenGetResourceResponse(msg: ResourcesReadResponse) {
    if (!msg) {
        return;
    }

    try {
        console.log(msg);

        selectResource.value = undefined;
        const editor = editorContext.editor.value;

        if (msg.contents.length === 0 || !editor) {
            return;
        }

        const container = document?.createElement('div');
        const resourceChatItem = createApp(ResourceChatItem, {
            contents: msg.contents
        });
        resourceChatItem
            .use(ElTooltip)
            .use(ElProgress)
            .use(ElPopover)
        resourceChatItem.mount(container);

        const firstElement = container.firstElementChild!;

        if (savedSelection) {
            savedSelection.deleteContents();
            savedSelection.insertNode(firstElement);
        } else {
            editor.appendChild(firstElement);
        }

        const newRange = document?.createRange();
        newRange.setStartAfter(firstElement);
        newRange.collapse(true);
        const selection = window.getSelection();

        selection?.removeAllRanges();
        selection?.addRange(newRange);

        editor.dispatchEvent(new Event('input'));
        editor.focus();

        showChooseResource.value = false;
    } catch (error) {
        ElMessage.error((error as Error).message);
    }
}
</script>

<style>
.icon-length {
    font-size: 16px;
}

.el-dialog .el-collapse-item__header {
    background-color: transparent !important;
}

.el-dialog .el-collapse-item__wrap {
    background-color: transparent !important;
}

</style>