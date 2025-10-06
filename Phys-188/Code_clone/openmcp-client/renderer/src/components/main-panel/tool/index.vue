<template>
    <el-scrollbar height="100%">
        <AutoDetector :tab-id="props.tabId" />
        <div class="tool-module">
            <div class="left">
                <h2>
                    <span class="iconfont icon-tool"></span>
                    {{ t('tool-module') }}
                    <el-button
                        style="font-size: 12px;"
                        @click="showAutoDetector = true"
                    >
                        {{ t('tool-self-detect') }}
                    </el-button>
                </h2>
                <ToolList :tab-id="props.tabId"></ToolList>
            </div>
            <div class="right">
                <ToolExecutor :tab-id="props.tabId"></ToolExecutor>
                <ToolLogger :tab-id="props.tabId"></ToolLogger>
            </div>
        </div>
        <AutoDetector 
            v-model="showAutoDetector"
            :tab-id="props.tabId"
        />
    </el-scrollbar>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue';
import ToolList from './tool-list.vue';
import ToolExecutor from './tool-executor.vue';
import ToolLogger from './tool-logger.vue';
import AutoDetector from './auto-detector/index.vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    }
});

const showAutoDetector = ref(false);
</script>

<style scoped>
.tool-module {
    padding: 20px;
    height: 100%;
    display: flex;
    justify-content: space-around;
}

.tool-module .left {
    width: 45%;
    max-width: 410px;
}

.tool-module .right {
    width: 45%;
}
</style>