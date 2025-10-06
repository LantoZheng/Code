<template>
    <div class="connection-option">
        <div class="env-switch">
            <span>{{ t('env-var') }}</span>

            <el-switch v-model="envEnabled" @change="(enable: boolean) => client.handleEnvSwitch(enable)" inline-prompt
                :active-text="t('preset')" :inactive-text="t('preset')"></el-switch>
        </div>
        <div class="input-env">
            <span class="input-env-container">
                <span>
                    <el-input v-model="client.connectionEnvironment.newKey" @keyup.enter="addEnvVar"></el-input>
                </span>
                <span>
                    <el-input v-model="client.connectionEnvironment.newValue" @keyup.enter="addEnvVar"></el-input>
                </span>
                <span>
                    <div @click="addEnvVar">
                        <span class="iconfont icon-add"></span>
                    </div>
                </span>
            </span>
        </div>
        <el-scrollbar height="200px" width="350px" class="display-env-container">
            <div class="display-env">
                <div class="input-env-container" v-for="option of client.connectionEnvironment.data" :key="option.key">
                    <span> <el-input v-model="option.key"></el-input></span>
                    <span> <el-input v-model="option.value" show-password></el-input></span>
                    <span @click="deleteEnvVar(option)">
                        <span class="iconfont icon-delete"></span>
                    </span>
                </div>
            </div>
        </el-scrollbar>
    </div>
</template>


<script setup lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { mcpClientAdapter } from './core';
import type { EnvItem } from './type';

defineComponent({ name: 'env-var' });
const props = defineProps({
    index: {
        type: Number,
        required: true
    }
});

const client = computed(() => mcpClientAdapter.clients[props.index]);

const { t } = useI18n();

/**
 * @description 添加环境变量
 */
function addEnvVar() {
    // 检查是否存在一样的 key
    const currentKey = client.value.connectionEnvironment.newKey;
    const currentValue = client.value.connectionEnvironment.newValue;

    if (currentKey.length === 0 || currentValue.length === 0) {
        return;
    }

    const sameNameItems = client.value.connectionEnvironment.data.filter(item => item.key === currentKey);

    if (sameNameItems.length > 0) {
        const conflictItem = sameNameItems[0];
        conflictItem.value = currentValue;
    } else {
        client.value.connectionEnvironment.data.push({
            key: currentKey, value: currentValue
        });
        client.value.connectionEnvironment.newKey = '';
        client.value.connectionEnvironment.newValue = '';
    }
}

watch(
    () => client.value.connectionEnvironment.data,
    () => {
        mcpClientAdapter.saveLaunchSignature();
    },
    { deep: true }
);

/**
 * @description 删除环境变量
 */
function deleteEnvVar(option: EnvItem) {
    const currentKey = option.key;
    const reserveItems = client.value.connectionEnvironment.data.filter(item => item.key !== currentKey);
    client.value.connectionEnvironment.data = reserveItems;
}

const envEnabled = ref(true);

</script>

<style>
.env-switch {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.env-switch .el-switch .el-switch__action {
    background-color: var(--main-color);
}

.env-switch .el-switch.is-checked .el-switch__action {
    background-color: var(--sidebar);
}

.env-switch .el-switch__core {
    border: 1px solid var(--main-color) !important;
}
</style>