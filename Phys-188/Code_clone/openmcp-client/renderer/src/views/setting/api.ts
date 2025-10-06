import type { ChatStorage } from '@/components/main-panel/chat/chat-box/chat';
import { TaskLoop } from '@/components/main-panel/chat/core/task-loop';
import { llmManager } from './llm';
import { reactive, ref } from 'vue';
import { makeUsageStatistic } from '@/components/main-panel/chat/core/usage';

export const llmSettingRef = ref<any>(null);
type NumberLike = string | number | undefined;

export const testPrompt = ref('you\'re a smart assistant, please write an article of at least 100 words to introduce mcp');

export const simpleTestResult = reactive<{
    done: boolean,
    start: boolean,
    error: any,
    tps: NumberLike,
    outputTps: NumberLike
    queueTime: NumberLike
}>({
    done: false,
    start: false,
    error: '',
    tps: undefined,
    outputTps: undefined,
    queueTime: undefined,
});

export async function makeSimpleTalk() {
    simpleTestResult.done = false;
    simpleTestResult.start = true;
    simpleTestResult.tps = undefined;
    simpleTestResult.queueTime = undefined;

    const loop = new TaskLoop();

    const chatStorage: ChatStorage = {
        messages: [],
        settings: {
            temperature: 0.6,
            modelIndex: llmManager.currentModelIndex,
            systemPrompt: '',
            enableTools: [],
            enableWebSearch: false,
            contextLength: 5,
            enableXmlWrapper: false,
            parallelToolCalls: true
        }
    };

    loop.setMaxEpochs(1);

    let receiveTime = -1;

    loop.registerOnChunk(() => {
        if (receiveTime <= 0) {
            receiveTime = Date.now();
        }
    });

    loop.registerOnDone(() => {        
        simpleTestResult.error = '';
        simpleTestResult.done = true;
        simpleTestResult.start = false;
    });

    loop.registerOnError(error => {
        const errorReason = error.msg;
        const errorText = JSON.stringify(errorReason);

        simpleTestResult.error = errorText;
        simpleTestResult.start = false;
    });

    const startTime = Date.now();
    await loop.start(chatStorage, testPrompt.value);
    const endTime = Date.now();

    const costTime = (endTime - receiveTime) / 1000;
    simpleTestResult.queueTime = (receiveTime - startTime) / 1000;
    
    const message = chatStorage.messages[chatStorage.messages.length - 1];

    if (message?.extraInfo) {
        const usage = message.extraInfo.usage;
        if (usage?.prompt_tokens && usage.completion_tokens) {
            // const total = usage?.prompt_tokens + usage?.completion_tokens;
            const total = usage?.completion_tokens;
            simpleTestResult.tps = (total / costTime).toFixed(2);            
        }
    }
}