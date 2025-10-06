<template>
    <el-tooltip placement="top" effect="light">
        <template #content>
            <div class="resource-chat-item-tooltip">
                <div v-for="(item, index) of toolRenderItems" :key="index">
                    <div v-if="item.mimeType === 'text/plain'">
                        {{ item.text }}
                    </div>

                    <div v-else-if="item.mimeType === 'image/jpeg' || item.mimeType === 'image/png'">
                        <img :src="item.imageUrl" alt="screenshot" />
                        <span>{{ item.text }}</span>
                    </div>

                    <div v-else>

                    </div>
                </div>
            </div>
        </template>

        <span class="chat-prompt-item" contenteditable="false">
            <span class="iconfont icon-file"></span>
            <span class="real-text">{{ resourceText }}</span>
            <el-progress v-if="!finishProcess" class="progress" style="width: 100px;" :percentage="progress"
                color="var(--main-color)"></el-progress>
        </span>
    </el-tooltip>
</template>

<script setup lang="ts">
import { useMessageBridge } from '@/api/message-bridge';
import type { ResourcesReadResponse } from '@/hook/type';
import { getImageBlobUrlByBase64 } from '@/hook/util';
import { computed, defineProps, type PropType, ref } from 'vue';

const props = defineProps({
    contents: {
        type: Array as PropType<ResourcesReadResponse['contents']>,
        required: true
    }
});


// mcp 协议中，表示图像两种方法
// 1. 将图像实现处理成文本
// 2. 将图像做成  { image_url: "https://tos.com/xxx.jpeg" }，然后上传这段表达的序列化文本

const toolRenderItems = ref<{
    mimeType: string;
    text: string;
    [key: string]: any;
}[]>([]);

const resourceText = computed(() => {    
    const texts = [];
    for (const item of toolRenderItems.value) {
        if (item.mimeType === 'text/plain') {
            texts.push(item.text);
        } else if (item.mimeType === 'image/jpeg' || item.mimeType === 'image/png') {
            texts.push(item.text || '');
        }
    }

    return texts.join('');
});

const bridge = useMessageBridge();
const progress = ref(0);
const progressText = ref('OCR');
const finishProcess = ref(true);

props.contents.forEach((content) => {
    console.log(content);

    if (content.mimeType === 'text/plain') {
        toolRenderItems.value.push({
            mimeType: content.mimeType,
            text: content.text
        });
    }

    if (content.mimeType === 'image/jpeg' || content.mimeType === 'image/png') {
        finishProcess.value = false;

        const blobUrl = getImageBlobUrlByBase64(content.blob!, content.mimeType);

        toolRenderItems.value.push({
            mimeType: content.mimeType,
            imageUrl: blobUrl,
            text: ''
        });

        const renderItem = toolRenderItems.value.at(-1)!;

        const makeRequest = async () => {
            const res = await bridge.commandRequest('ocr/start-ocr', {
                base64String: content.blob,
                mimeType: content.mimeType
            });

            if (res.code === 200) {
                const filename = res.msg.filename;
                const workerId = res.msg.workerId;

                const cancel = bridge.addCommandListener('ocr/worker/log', data => {

                    finishProcess.value = false;
                    const { id, progress: p = 1.0, status = 'finish' } = data;
                    if (id === workerId) {
                        progressText.value = status;
                        progress.value = Math.min(Math.ceil(Math.max(p * 100, 0)), 100);
                    }
                }, { once: false });

                bridge.addCommandListener('ocr/worker/done', data => {
                    if (data.id !== workerId) {
                        return;
                    }

                    progress.value = 1;
                    finishProcess.value = true;
                    toolRenderItems.value[0].text = data.text;

                    cancel();
                }, { once: true });
            }
        }

        makeRequest();
    }
});

</script>

<style>
.resource-chat-item-tooltip {
    min-height: 100px;
    max-width: 420px;
    display: flex;
    flex-direction: column;
}

.resource-chat-item-tooltip img {
    max-width: 420px;
}


.chat-resource-item {
    max-width: 80px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: inline-flex;
    border-radius: .3em;
    align-items: center;
    padding: 0 4px;
    background-color: #373839;
    border: 1px solid var(--foreground);
    font-size: 12px;
    margin-left: 3px;
    margin-right: 3px;
}

.chat-resource-item .iconfont {
    margin-right: 4px;
}
</style>