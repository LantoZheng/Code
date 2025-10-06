<template>
    <div class="message-role">Agent</div>
    <div class="message-text">
        <div v-if="message.content" v-html="markdownToHtml(messageContent)"></div>
    </div>
    <MessageMeta :message="props.message" />
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue';
import { markdownToHtml } from '@/components/main-panel/chat/markdown/markdown';

import MessageMeta from './message-meta.vue';

const props = defineProps({
    message: {
        type: Object,
        required: true
    },
    tabId: {
        type: Number,
        required: true
    }
});

const messageContent = computed(() => {
    if (typeof props.message.content === 'undefined') {
        return 'undefined';
    }
    if (typeof props.message.content === 'object') {
        return JSON.stringify(props.message.content, null, 2);
    }
    return props.message.content.toString();
});


</script>

<style>
</style>