<template>
    <div class="k-input-object">
        <div :ref="el => editorContainer = el"
            class="k-input-object__editor"
        ></div>
        <div v-if="errorMessage" class="k-input-object__error">
            {{ errorMessage }}
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, type PropType, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { EditorView, basicSetup } from 'codemirror';
import type { Completion, CompletionContext } from "@codemirror/autocomplete"
import { jsonLanguage } from "@codemirror/lang-json"

import { json } from '@codemirror/lang-json'
import { oneDark } from '@codemirror/theme-one-dark'
import { debounce } from 'lodash'
import { patchEditors } from './patch';
import { getPlatform } from '@/api/platform';

const props = defineProps({
    modelValue: {
        type: Object,
        default: () => ({})
    },
    placeholder: {
        type: String,
        default: '请输入 JSON 对象'
    },
    debounceTime: {
        type: Number,
        default: 500
    },
    schema: {
        type: Object as PropType<{
            type?: string;
            properties?: Record<string, {
                type: string;
                description?: string;
                default?: any;
                enum?: any[];
            }>;
            required?: string[];
        }>,
        default: () => ({})
    }
})

const emit = defineEmits(['update:modelValue', 'parse-error']);
const { t } = useI18n();

const editorContainer = ref<any>(null);
const editorView = ref<EditorView | null>(null);
const isInvalid = ref(false);
const errorMessage = ref('');

const inputValue = ref<string>(JSON.stringify(props.modelValue, null, 2));

// 防抖处理输入
const debouncedParse = debounce((value: string) => {
    if (value.trim() === '') {
        errorMessage.value = '';
        isInvalid.value = false;
        emit('update:modelValue', undefined);
        return;
    }
    try {
        const parsed = JSON.parse(value);
        isInvalid.value = false;
        errorMessage.value = '';
        emit('update:modelValue', parsed);
    } catch (error) {
        isInvalid.value = true;
        errorMessage.value = t('error-parse-json') + (error as Error).message;
        emit('parse-error', error);
    }
}, props.debounceTime);

// 添加自动补全函数
function getJsonCompletion(schema: any) {
    return (context: CompletionContext) => {
        // 检查当前输入是否是标点符号
        const charBefore = context.state.sliceDoc(context.pos - 1, context.pos)
        if (/[,.{}[\]:]/.test(charBefore)) return null

        const word = context.matchBefore(/\w*/)
        if (!word) return null

        // 检查当前是否在字符串内
        const state = context.state
        const pos = context.pos
        const line = state.doc.lineAt(pos)
        const textBefore = line.text.slice(0, pos - line.from)

        // 如果前面有奇数个双引号，说明在字符串内，不触发补全
        const quoteCount = (textBefore.match(/"/g) || []).length
        if (quoteCount % 2 !== 0) return null

        const completions: Completion[] = []

        // 处理对象属性补全
        if (schema.properties) {
            Object.entries(schema.properties).forEach(([key, value]) => {
                completions.push({
                    label: key,
                    type: "property",
                    apply: `"${key}": ${getDefaultValue(value as any)}`
                })
            })
        }

        return {
            from: word.from,
            options: completions,
            validFor: /^\w*$/
        }
    }
}

// 获取默认值函数
function getDefaultValue(property: any): string {
    if (property.default !== undefined) {
        return JSON.stringify(property.default)
    }
    switch (property.type) {
        case 'string': return '""'
        case 'number': return '0'
        case 'boolean': return 'false'
        case 'object': return '{}'
        case 'array': return '[]'
        default: return 'null'
    }
}

watch(
    () => props.modelValue,
    (newVal) => {
        // 当前编辑器内容
        const currentContent = editorView.value?.state.doc.toString() ?? '';
        const newContent = JSON.stringify(newVal ?? {}, null, 2);

        if (currentContent !== newContent && editorView.value) {
            editorView.value.dispatch({
                changes: {
                    from: 0,
                    to: editorView.value.state.doc.length,
                    insert: newContent
                }
            });
        }
    },
    { deep: true }

);

const platform = getPlatform();

onMounted(() => {
    if (editorContainer.value) {
        const extensions = [
            basicSetup,
            json(),
            oneDark,
            EditorView.updateListener.of(update => {
                if (update.docChanged) {
                    const value = update.state.doc.toString()
                    debouncedParse(value)
                }
            })
        ];

        // 如果schema不为空，添加自动补全
        if (Object.keys(props.schema).length > 0) {
            extensions.push(
                jsonLanguage.data.of({
                    autocomplete: getJsonCompletion(props.schema)
                })
            )
        }

        editorView.value = new EditorView({
            doc: JSON.stringify(props.modelValue, null, 2),
            extensions,
            parent: editorContainer.value
        });

        if (platform === 'vscode') {
            const editableElement = editorContainer.value.querySelector('[contenteditable="true"]');
            patchEditors.add(editableElement);
        }
    }
})


onUnmounted(() => {
    if (platform === 'vscode') {
         const editableElement = editorContainer.value.querySelector('[contenteditable="true"]');
        patchEditors.delete(editableElement);   
    }
})

</script>

<style scoped>
.k-input-object {
    width: 100%;
    background-color: var(--background);
    border-radius: .5em;
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
}

.k-input-object__textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid var(--el-border-color-light);
    border-radius: 4px;
    font-family: monospace;
    resize: vertical;
    transition: border-color 0.2s;
    background-color: var(--el-bg-color-overlay);
    color: var(--el-text-color-primary);
}

.k-input-object__textarea:focus {
    outline: none;
    border-color: var(--main-color);
}

.k-input-object__textarea.is-invalid {
    border-color: var(--el-color-error);
}

.k-input-object__error {
    color: var(--el-color-error);
    font-size: 12px;
    margin-top: 4px;
}

.k-input-object__editor {
    width: 100%;
    border: 1px solid var(--el-border-color-light);
    border-radius: 4px;
    overflow: hidden;
    background-color: var(--el-bg-color-overlay);
}

.k-input-object__editor.is-invalid {
    border-color: var(--el-color-error);
}

.k-input-object__error {
    color: var(--el-color-error);
    font-size: 12px;
    margin-top: 4px;
}
</style>