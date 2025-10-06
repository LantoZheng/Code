<template>
    <el-tooltip :content="t('parallel-tool-calls')" placement="top" effect="light">
        <div class="setting-button" :class="{ 'active': tabStorage.settings.parallelToolCalls }" size="small"
            @click="toggle">
            <span class="iconfont icon-parallel"></span>
        </div>
    </el-tooltip>
</template>

<script setup lang="ts">
import { inject } from 'vue';
import { useI18n } from 'vue-i18n';
import type { ChatStorage } from '../chat';

const { t } = useI18n();

const tabStorage = inject('tabStorage') as ChatStorage;

const toggle = () => {
    tabStorage.settings.parallelToolCalls = !tabStorage.settings.parallelToolCalls;
};

</script>

<style></style>