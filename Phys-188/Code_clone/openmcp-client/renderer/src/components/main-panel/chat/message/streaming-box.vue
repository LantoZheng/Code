<template>
    <div class="message-avatar streaming-box">
        <span class="iconfont icon-chat"></span>
    </div>
    <div class="message-content">
        <div class="message-role">
            Agent
            <span class="message-reminder">
                {{ t('generate-answer') }}
                <span class="tool-loading iconfont icon-double-loading">
                </span>
            </span>
        </div>
        <div class="message-text streaming-box">
            <span v-html="waitingMarkdownToHtml(streamingContent)"></span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import { useI18n } from 'vue-i18n';
import { markdownToHtml } from '@/components/main-panel/chat/markdown/markdown';

const { t } = useI18n();

const props = defineProps({
    streamingContent: {
        type: String,
        required: true
    },
    tabId: {
        type: Number,
        required: true
    }
});

function waitingMarkdownToHtml(content: string) {
    if (content) {
        return markdownToHtml(content);
    }
    return '<span class="typing-cursor">|</span>';
}

</script>

<style>
</style>