<template>
    <div class="tool-logger">
        <span>
            <span>{{ t('response') }}</span>
            <span style="width: 200px; display: flex;">
				<el-segmented v-model="renderMode.current" :options="renderMode.data" size="default"
					style="margin: 10px; background-color: var(--background); font-size: 12px;">
					<template #default="scope">
						{{ scope.item.label }}
					</template>
				</el-segmented>
            </span>
        </span>
        <el-scrollbar height="500px">
            <div class="output-content" contenteditable="false">

                <!-- TODO: 更加稳定，现在通过下面这个来判断上一次执行结果是否成功 -->
                <div v-if="typeof tabStorage.lastToolCallResponse === 'string'" class="error-tool-call">
                    <span>
                        {{ tabStorage.lastToolCallResponse }}
                    </span>
                </div>

                <div v-else>
                    <!-- 展示原本的信息 -->
                    <template v-if="renderMode.current === 'plaintext'">
                        <div
                            v-for="(c, idx) in (tabStorage.lastToolCallResponse?.content || [])"
                            :key="idx"
                            class="tool-call-block"
                        >
                            <pre class="tool-call-text">{{ c.text }}</pre>
                        </div>
                    </template>

                    <template v-else-if="renderMode.current === 'markdown'">
                        <div class="markdown" v-html="resultMarkdown"></div>
                    </template>

                    <!-- 展示 json -->
                    <template v-else-if="renderMode.current === 'json'">
                        <json-render :json="tabStorage.lastToolCallResponse"/>
                    </template>
                </div>

            </div>
        </el-scrollbar>
    </div>
</template>

<script setup lang="ts">
import { defineComponent, defineProps, computed, ref, reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import { tabs } from '../panel';
import type { ToolStorage } from './tools';
import JsonRender from '@/components/json-render/index.vue';
import { markdownToHtml } from '../chat/markdown/markdown';

defineComponent({ name: 'tool-logger' });
const { t } = useI18n();

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    }
});

const tab = tabs.content[props.tabId];
const tabStorage = tab.storage as ToolStorage;

const resultMarkdown = computed(() => {
    const lastToolCallResponse = tabStorage.lastToolCallResponse;
    if (!lastToolCallResponse) {
        return '';
    }
    if (typeof lastToolCallResponse === 'string') {
        return markdownToHtml(lastToolCallResponse.toString());
    }
    
    const rawText = (lastToolCallResponse.content || []).map(c => c.text).join('\n\n');
    const html = markdownToHtml(rawText);
    return html;
})

const renderMode = reactive({
	current: 'plaintext',
	data: [
		{
			value: 'plaintext',
			label: 'plaintext'
		},
		{
			value: 'markdown',
			label: 'markdown',
		},
		{
			value: 'json',
            label: 'json'
		}
	]
});

</script>

<style>
.tool-logger {
    border-radius: .5em;
    background-color: var(--background);
    padding: 10px;
}

.tool-logger .el-switch__core {
    border: 1px solid var(--main-color) !important;
    width: 60px !important;
}

.tool-logger .el-switch .el-switch__action {
    background-color: var(--main-color);
}

.tool-logger .el-switch.is-checked .el-switch__action {
    background-color: var(--sidebar);
}

.tool-logger>span:first-child {
    margin-bottom: 5px;
    display: flex;
    align-items: center;
}

.tool-logger .output-content {
    border-radius: .5em;
    padding: 15px;
    min-height: 450px;
    height: fit-content;
    font-family: var(--code-font-family);
    background-color: var(--sidebar);
}

.error-tool-call {
    background-color: rgba(245, 108, 108, 0.5);
    padding: 5px 9px;
    border-radius: .5em;
}

.tool-call-block {
    margin-bottom: 12px;
    padding: 10px 12px;
    background: rgba(0,0,0,0.04);
    border-radius: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.tool-call-text {
    font-family: var(--code-font-family, monospace);
    font-size: 15px;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 0;
    color: var(--el-text-color-primary, #222);
}
</style>