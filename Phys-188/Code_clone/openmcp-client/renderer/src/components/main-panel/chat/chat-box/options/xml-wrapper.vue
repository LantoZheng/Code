<template>
    <el-tooltip :content="t('enable-xml-wrapper')" placement="top" effect="light">
        <div class="setting-button" :class="{ 'active': tabStorage.settings.enableXmlWrapper }" size="small"
            @click="toggle">
            <span class="iconfont icon-suffix-xml"></span>
        </div>
    </el-tooltip>
</template>

<script setup lang="ts">
import { defineComponent, inject } from 'vue';
import type { ChatStorage } from '../chat';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const tabStorage = inject('tabStorage') as ChatStorage;

const toggle = () => {    
    tabStorage.settings.enableXmlWrapper = !tabStorage.settings.enableXmlWrapper;
};

</script>

<style></style>