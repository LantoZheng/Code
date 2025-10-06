<template>
    <!-- 下侧的设置按钮 -->
    <Setting :tabId="tabId" v-model="modelValue" />

    <!-- 编辑区 -->
    <div class="k-rich-textarea">
        <div
            :ref="el => editor = el"
            contenteditable="true"
            class="rich-editor"
            :placeholder="placeholder"
            @input="handleInput"
            @paste="handlePaste"
            @keydown.backspace="handleBackspace"
            @keydown.enter="handleKeydown"
            @compositionstart="handleCompositionStart"
            @compositionend="handleCompositionEnd"
        ></div>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, computed, provide } from 'vue';

import Setting from './options/setting.vue';

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    },
    modelValue: {
        type: String,
        required: true
    },
    placeholder: {
        type: String,
        default: '输入消息...'
    },
    customClass: {
        type: String,
        default: ''
    }
});

const modelValue = computed({
    get() {
        return props.modelValue;
    },
    set(value: string) {
        emit('update:modelValue', value);
    }
})

const emit = defineEmits(['update:modelValue', 'pressEnter']);

const editor = ref<any>(null);

provide('editorContext', {
    editor,
});

function handleBackspace(event: KeyboardEvent) {
    // 自定义 Backspace 行为
    const editorElement = editor.value;
    if (!(editorElement instanceof HTMLDivElement)) {
        return;
    }

    const selection = window.getSelection();
    if (!selection || !selection.rangeCount) {
        return;
    }

    const range = selection.getRangeAt(0);
    const startContainer = range.startContainer;

    // 如果光标在 rich-item 元素中，阻止默认行为并删除整个元素
    if (startContainer.parentElement?.classList.contains('rich-item')) {
        event.preventDefault();
        startContainer.parentElement.remove();
    }
}

function handleInput(event: Event) {
    const editorElement = editor.value;
    if (!(editorElement instanceof HTMLDivElement)) {
        return;
    }
    const fragments: string[] = [];

    editorElement.childNodes.forEach(node => {
        if (node.nodeType === Node.TEXT_NODE) {

            fragments.push(node.textContent || '');
        } else {
            const element = node as HTMLElement;

            const collection = element.getElementsByClassName('real-text');
            const fragmentText = extractTextFromCollection(collection);
            
            fragments.push(fragmentText || '');
        }
    });

    emit('update:modelValue', fragments.join(' '));
}

function extractTextFromCollection(collection: HTMLCollection) {
    const texts = [];
    for (let i = 0; i < collection.length; i++) {        
        texts.push(collection[i].textContent); // 或 .innerText
    }

    return texts.join('');
}

const isComposing = ref(false);

defineExpose({
    editor,
    handleBackspace,
    handleInput,
});

function handleKeydown(event: KeyboardEvent) {
    
    if (event.key === 'Enter' && !event.shiftKey && !isComposing.value) {
        event.preventDefault();
        const editorElement = editor.value;
        if (!(editorElement instanceof HTMLDivElement)) {
            return;
        }

        // 清空
        editorElement.innerHTML = '';

        emit('pressEnter', event);

    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {

        const editorElement = editor.value;
        if (!(editorElement instanceof HTMLDivElement)) {
            return;
        }

        const selection = window.getSelection();
        if (!selection || !selection.rangeCount) {
            return;
        }

        const range = selection.getRangeAt(0);
        const startContainer = range.startContainer;

        if (event.key === 'ArrowLeft') {
            // 检查左侧节点
            const previousSibling = startContainer.previousSibling;
            if (previousSibling && previousSibling.nodeType !== Node.TEXT_NODE) {
                event.preventDefault();
                range.setStartBefore(previousSibling);
                range.collapse(true);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        } else if (event.key === 'ArrowRight') {
            // 检查右侧节点
            const nextSibling = startContainer.nextSibling;
            if (nextSibling && nextSibling.nodeType !== Node.TEXT_NODE) {
                event.preventDefault();
                range.setStartAfter(nextSibling);
                range.collapse(true);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        }
    }
}

function handlePaste(event: ClipboardEvent) {
    event.preventDefault(); // 阻止默认粘贴行为
    const clipboardData = event.clipboardData;
    if (clipboardData) {
        const pastedText = clipboardData.getData('text/plain');
        const editorElement = editor.value;
        if (editorElement instanceof HTMLDivElement) {
            const selection = window.getSelection();
            if (selection && selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                range.deleteContents();
                const textNode = document?.createTextNode(pastedText);
                range.insertNode(textNode);
                range.setStartAfter(textNode);
                range.collapse(true);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        }
    }

    if (editor.value) {
        editor.value.dispatchEvent(new Event('input'));
    }
}

function handleCompositionStart() {
    isComposing.value = true;
}

function handleCompositionEnd() {
    isComposing.value = false;
}

</script>

<style>
.k-rich-textarea {
    border: 1px solid var(--main-color);
    background-color: var(--el-input-bg-color, var(--el-fill-color-blank));
    background-image: none;
    border-radius: .5em;
    box-shadow: 0 0 0 1px var(--el-input-border-color, var(--el-border-color)) inset;
    box-sizing: border-box;
    color: var(--el-input-text-color, var(--el-text-color-regular));
    padding: 10px 10px;
    display: inline-block;
    font-size: var(--el-font-size-base);
    position: relative;
    vertical-align: bottom;
    width: 100%;
    min-height: 50px;
    transition: var(--el-transition-box-shadow);
}

.rich-editor {
    min-height: 100px;
    outline: none;
    white-space: pre-wrap;
}

.rich-editor:empty::before {
    content: attr(placeholder);
    color: #C0C4CC;
}

.rich-item {
    padding: 2px 4px;
    border-radius: 4px;
    margin: 0 2px;
}

.rich-item-prompt {
    background-color: #e8f0fe;
    color: #1a73e8;
}

.rich-item-resource {
    background-color: #f1f3f4;
    color: #202124;
}


.chat-resource-item {
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    background-color: #373839;
    font-size: 12px;
}

.chat-resource-item .iconfont {
    margin-right: 4px;
}

</style>