<template>
    <el-scrollbar height="100%">
        <div class="prompt-module">
            <div class="left">
                <h2>
                    <span class="iconfont icon-chat"></span>
                    {{ t('prompt-module') }}
                </h2>

                <PromptTemplates :tab-id="props.tabId"></PromptTemplates>

            </div>
            <div class="right">
                <PromptReader :tab-id="props.tabId"></PromptReader>

                <PromptLogger :tab-id="props.tabId"></PromptLogger>
            </div>
        </div>
    </el-scrollbar>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import PromptTemplates from './prompt-templates.vue';
import PromptReader from './prompt-reader.vue';
import PromptLogger from './prompt-logger.vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    }
});

</script>

<style scoped>
.prompt-module {
    padding: 20px;
    height: 100%;
    display: flex;
    justify-content: space-around;
}

.prompt-module .left {
    width: 45%;
    max-width: 410px;
}

.prompt-module .right {
    width: 45%;
}
</style>