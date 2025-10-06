<template>
    <div>
        <h3>{{ currentPrompt?.name }}</h3>
    </div>
    <div class="prompt-reader-container">
        <el-form :model="tabStorage.formData" :rules="formRules" ref="formRef" label-position="top">
            <el-form-item v-for="param in currentPrompt?.arguments" :key="param.name"
                :label="param.name" :prop="param.name">
                <el-input v-model="tabStorage.formData[param.name]"
                    :placeholder="t('enter') +' ' + param.name"
                    @keydown.enter.prevent="handleSubmit"
                />
            </el-form-item>

            <el-form-item>
                <el-button type="primary" :loading="loading" @click="handleSubmit">
                    {{ t('read-prompt') }}
                </el-button>
                <el-button @click="resetForm">
                    {{ t('reset') }}
                </el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { defineComponent, defineProps, defineEmits, watch, ref, computed, reactive, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import type { FormInstance, FormRules } from 'element-plus';
import { tabs } from '../panel';
import type { PromptStorage } from './prompts';
import type { PromptsGetResponse } from '@/hook/type';
import { mcpClientAdapter } from '@/views/connect/core';

defineComponent({ name: 'prompt-reader' });

const { t } = useI18n();

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    },
    currentPromptName: {
        type: String,
        required: false
    }
});

const emits = defineEmits(['prompt-get-response']);

let tabStorage: PromptStorage;

if (props.tabId >= 0) {
    tabStorage = tabs.content[props.tabId].storage as PromptStorage;
} else {
    tabStorage = reactive({
        activeNames: [0],
        currentPromptName: props.currentPromptName || '',
        formData: {},
        lastPromptGetResponse: undefined
    });
}

if (!tabStorage.formData) {
    tabStorage.formData = {};
}

const formRef = ref<FormInstance>();
const loading = ref(false);
const responseData = ref<PromptsGetResponse>();

const currentPrompt = computed(() => {

    for (const client of mcpClientAdapter.clients) {
        const prompt = client.promptTemplates?.get(tabStorage.currentPromptName);
        if (prompt) {
            return prompt;
        }
    }
});

const formRules = computed<FormRules>(() => {
    const rules: FormRules = {}
    currentPrompt.value?.arguments.forEach(param => {
        rules[param.name] = [
            {
                message: `${param.name} ` + t('is-required'),
                trigger: 'blur'
            }
        ]
    });

    return rules;
});

const initFormData = () => {
    if (!currentPrompt.value?.arguments) return;
    const newSchemaDataForm: Record<string, number | boolean | string> = {};    

    currentPrompt.value.arguments.forEach(param => {
        newSchemaDataForm[param.name] = '';
        if (tabStorage.formData[param.name] !== undefined) {
            newSchemaDataForm[param.name] = tabStorage.formData[param.name];
        }
    });

    tabStorage.formData = newSchemaDataForm;
}

const resetForm = () => {
    formRef.value?.resetFields();
    responseData.value = undefined;
}

async function handleSubmit() {

    const res = await mcpClientAdapter.readPromptTemplate(
        currentPrompt.value?.name || '',
        JSON.parse(JSON.stringify(tabStorage.formData))
    );

    tabStorage.lastPromptGetResponse = res;
    emits('prompt-get-response', res);
}

if (props.tabId >= 0) {
    watch(() => tabStorage.currentPromptName, () => {
        initFormData();
        resetForm();
    }, { immediate: true });
}

onMounted(() => {
    initFormData();
});

</script>

<style>
.prompt-reader-container {
    background-color: var(--background);
    padding: 10px 12px;
    border-radius: .5em;
    margin-bottom: 15px;
}
</style>