<template>
    <div class="extra-info warning" v-if="isGoogle">
        当前模型组协议兼容性较差，特别是 gemini-2.0-flash 模型的函数调用能力不稳定；如果想要稳定使用 gemini 的服务，请尽可能使用最新的模型或者使用 newApi 进行协议转接。
    </div>
    <div class="connect-test" v-if="simpleTestResult.done || simpleTestResult.error">
        <div class="test-result">
            <div class="result-item" v-if="simpleTestResult.done">
                <span class="iconfont icon-dui"></span>
                <span>{{ " okey dockey :D" }}</span>
                    <span v-if="simpleTestResult.queueTime" class="queue-time">
                        {{ t('queue-time') }}: {{ simpleTestResult.queueTime }} s
                    </span>
                <span v-if="simpleTestResult.tps" class="tps">{{ simpleTestResult.tps }} token/s</span>
                <span v-else class="tps">{{ t("server-not-support-statistic") }}</span>
            </div>
            <div class="result-item error" v-if="simpleTestResult.error">
                <span class="iconfont icon-cuo"></span>
                <span>{{ ' ' + simpleTestResult.error }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { simpleTestResult } from './api';
import { llmManager, llms } from './llm';
import { computed } from '@vue/reactivity';

const { t } = useI18n();

const isGoogle = computed(() => {
    const model = llms[llmManager.currentModelIndex];
    return model.userModel?.startsWith('gemini') || model.baseUrl.includes('googleapis');
});

console.log(llms[llmManager.currentModelIndex]);


</script>

<style scoped>
.connect-test {
    margin-top: 20px;
    padding: 12px;
    border-radius: 4px;
    background-color: var(--el-bg-color);
}

.test-result {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.result-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--el-color-success);
    padding: 6px 12px;
    border-radius: 4px;
}

.connect-test .tps {
    margin-left: 5px;
    color: var(--foreground);
    background-color: var(--el-fill-color-light);
    padding: 2px 6px;
    border-radius: 4px;
}

.result-item.error {
    color: var(--el-color-danger);
}

.result-item .iconfont {
    font-size: 16px;
}

.extra-info.warning {
    background-color: rgba(230, 162, 60, 0.5);
    padding: 10px;
    border-radius: 4px;
    margin-top: 15px;
    margin-bottom: 10px;
}

.queue-time {
    margin-left: 8px;
    color: var(--foreground);
    background-color: var(--el-fill-color-light);
    padding: 2px 6px;
    border-radius: 4px;
}
</style>