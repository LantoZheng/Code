<template>
    <div>
        <h3>{{ currentResource?.name }}</h3>
    </div>
    <div class="resource-reader-container">
        <el-form :model="tabStorage.formData" :rules="formRules" ref="formRef" label-position="top">
            <el-form-item v-for="param in currentResource?.params" :key="param" :label="param"
                :prop="param">
                <el-input v-model="tabStorage.formData[param]"
                    :placeholder="t('enter') + ' ' + param"
                    @keydown.enter.prevent="handleSubmit"
                />
            </el-form-item>

            <el-form-item v-if="tabStorage.currentType === 'template'">
                <el-button type="primary" :loading="loading" @click="handleSubmit">
                    {{ t('read-resource') }}
                </el-button>
                <el-button @click="resetForm">
                    {{ t('reset') }}
                </el-button>
            </el-form-item>
            <el-form-item v-else>
                <el-button @click="handleSubmit">
                    {{ t("refresh") }}
                </el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup lang="ts">
import { defineComponent, defineProps, watch, ref, computed, reactive, defineEmits } from 'vue';
import { useI18n } from 'vue-i18n';
import type { FormInstance, FormRules } from 'element-plus';
import { tabs } from '../panel';
import { parseResourceTemplate, type ResourceStorage } from './resources';
import type{ ResourcesReadResponse } from '@/hook/type';
import { getDefaultValue, normaliseJavascriptType } from '@/hook/mcp';
import { mcpClientAdapter } from '@/views/connect/core';

defineComponent({ name: 'resource-reader' });

const { t } = useI18n();

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    },
    currentResourceName: {
        type: String,
        required: false
    }
});

const emits = defineEmits(['resource-get-response']);

let tabStorage: ResourceStorage;

if (props.tabId >= 0) {
    const tab = tabs.content[props.tabId];
    tabStorage = tab.storage as ResourceStorage;
} else {
    tabStorage = reactive({
        activeNames: [0],
		templateActiveNames: [0],
        currentType: 'resource',
        currentResourceName: props.currentResourceName || '',
        formData: {},
        lastResourceReadResponse: undefined
    });
}

if (!tabStorage.formData) {
    tabStorage.formData = {};
}

// 表单相关状态
const formRef = ref<FormInstance>();
const loading = ref(false);
const responseData = ref<ResourcesReadResponse>();

// 当前 resource 的模板参数
const currentResource = computed(() => {

    for (const client of mcpClientAdapter.clients) {
        const resource = client.resources?.get(tabStorage.currentResourceName);
        if (resource) {
            return {
                name: resource.name,
                template: resource,
                params: [],
                // resources 用不到 fill 函数
                fill: () => ''
            };
        }

        const resourceTemplate = client.resourceTemplates?.get(tabStorage.currentResourceName);
        if (resourceTemplate) {
            const { params, fill } = parseResourceTemplate(resourceTemplate.uriTemplate);
            return {
                name: resourceTemplate.name,
                template: resourceTemplate,
                params,
                fill
            };
        }
    }
});

// 表单验证规则
const formRules = computed<FormRules>(() => {
    const rules: FormRules = {}
    currentResource.value?.params.forEach(param => {
        rules[param] = [
            {
                message: `${param} ` + t('is-required'),
                trigger: 'blur'
            }
        ]
    });

    return rules;
});

// 初始化表单数据
const initFormData = () => {
    if (!currentResource.value?.params) {
        return;
    }

    const newSchemaDataForm: Record<string, number | boolean | string> = {};
    currentResource.value.params.forEach(param => {
        newSchemaDataForm[param] = '';
        if (tabStorage.formData[param] !== undefined) {
            newSchemaDataForm[param] = tabStorage.formData[param];
        }
    });

    tabStorage.formData = newSchemaDataForm;
}

// 重置表单
const resetForm = () => {
    formRef.value?.resetFields();
    responseData.value = undefined;
}

function getUri() {
    if (tabStorage.currentType === 'template') {
        const fillFn = currentResource.value?.fill || ((str: any) => str);
        const uri = fillFn(tabStorage.formData);
        return uri;
    }
    
    for (const client of mcpClientAdapter.clients) {
        const resource = client.resources?.get(tabStorage.currentResourceName);
        if (resource) {
            return resource.uri;
        }
    }
}

// 提交表单
async function handleSubmit() {
    const uri = getUri();
    const res = await mcpClientAdapter.readResource(uri);
    tabStorage.lastResourceReadResponse = res;
    emits('resource-get-response', res);
}

if (props.tabId >= 0) {
    watch(() => tabStorage.currentResourceName, () => {
        initFormData();
        resetForm();
    }, { immediate: true });
}

</script>

<style>
.resource-reader-container {
    background-color: var(--background);
    padding: 10px 12px;
    border-radius: .5em;
    margin-bottom: 15px;
}
</style>