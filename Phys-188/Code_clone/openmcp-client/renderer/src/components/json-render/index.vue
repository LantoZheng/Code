<template>
    <el-scrollbar width="100%">
        <div v-html="renderJson(json)">
        </div>
    </el-scrollbar>
</template>

<script setup lang="ts">
import { defineProps, type PropType } from 'vue';
import { renderJson } from '../main-panel/chat/markdown/markdown';

const props = defineProps({
    json: {
        type: Object as PropType<any>,
        required: true
    }
});

</script>

<style>
</style>