<template>
<footer class="chat-footer">
    <div class="input-area">
        <div class="input-wrapper">

            <KRichTextarea
                :ref="el => editorRef = el"
                :tabId="tabId"
                v-model="userInput"
                :placeholder="t('enter-message-dot')"
                :customClass="'chat-input'"
                @press-enter="handleSend()"
            />

            <el-button type="primary" @click="isLoading ? handleAbort() : handleSend()" class="send-button">
                <span v-if="!isLoading" class="iconfont icon-send"></span>
                <span v-else class="iconfont icon-stop"></span>
            </el-button>
        </div>
    </div>
</footer>
</template>

<script setup lang="ts">
import { provide, onMounted, onUnmounted, ref, defineEmits, defineProps, type PropType, inject, type Ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

import KRichTextarea from './rich-textarea.vue';
import { tabs } from '../../panel';
import type { ChatMessage, ChatStorage, ToolCall, RichTextItem } from './chat';
import { MessageState } from './chat';

import { TaskLoop } from '../core/task-loop';
import { llmManager, llms } from '@/views/setting/llm';
import { ElMessage } from 'element-plus';

const { t } = useI18n();

const props = defineProps({
    tabId: {
        type: Number,
        required: true
    }
});

const emits = defineEmits(['update:scrollToBottom']);
const editorRef = ref<any>(null);

const tab = tabs.content[props.tabId];
const tabStorage = tab.storage as ChatStorage;

// 创建 messages
if (!tabStorage.messages) {
    tabStorage.messages = [] as ChatMessage[];
}

const userInput = ref<string>('');

let loop: TaskLoop | undefined = undefined;

const isLoading = inject('isLoading') as Ref<boolean>;
const autoScroll = inject('autoScroll') as Ref<boolean>;
const streamingContent = inject('streamingContent') as Ref<string>;
const streamingToolCalls = inject('streamingToolCalls') as Ref<ToolCall[]>;
const scrollToBottom = inject('scrollToBottom') as () => Promise<void>;
const updateScrollHeight = inject('updateScrollHeight') as () => void;
const chatContext = inject('chatContext') as any;

// 并行模式相关
const chatMode = inject('chatMode') as Ref<string>;
const parallelChats = inject('parallelChats') as Ref<any[]>;
const updateChatRenderMessages = inject('updateChatRenderMessages') as (chat: any, streamingToolCalls?: ToolCall[]) => Promise<void>;

chatContext.handleSend = handleSend;

function clearErrorMessage(errorMessage: string) {
    try {
        const errorObject = JSON.parse(errorMessage);
        if (errorObject.error) {
            return errorObject.error;
        }
        if (errorObject.message) {
            return errorObject.message;
        }
        if (errorObject.msg) {
            return errorObject.msg;
        }
    } catch (error) {
        return errorMessage;
    }
}

function handleSend(newMessage?: string) {
    
    const userMessage = newMessage || userInput.value;


    if (!userMessage || isLoading.value) {
        return;
    }

    // 清空文本
    userInput.value = '';
    const editor = editorRef.value.editor;
    if (editor) {
        editor.innerHTML = '';
    }

    if (chatMode.value === 'parallel-chat' && parallelChats.value.length > 0) {
        // 并行模式：同时发送到多个模型
        handleParallelSend(userMessage);
    } else {
        // 单聊天模式：发送到当前模型
        handleSingleSend(userMessage);
    }
}

function handleSingleSend(userMessage: string) {
    isLoading.value = true;
    autoScroll.value = true;
    
    loop = new TaskLoop();
    loop.bindStreaming(streamingContent, streamingToolCalls);

    loop.registerOnError((error) => {
        const errorMessage = clearErrorMessage(error.msg);
        ElMessage.error(errorMessage);
        
        if (error.state === MessageState.ReceiveChunkError) {
            tabStorage.messages.push({
                role: 'assistant',
                content: errorMessage,
                extraInfo: {
                    created: Date.now(),
                    state: error.state,
                    serverName: llms[llmManager.currentModelIndex].id || 'unknown',
                    enableXmlWrapper: false
                }
            });
        }
    });

    loop.registerOnChunk(() => {
        scrollToBottom();
    });

    loop.registerOnDone(() => {
        scrollToBottom();
    });

    loop.registerOnEpoch(() => {
        isLoading.value = true;
        scrollToBottom();
    });

    loop.start(tabStorage, userMessage).then(() => {
        isLoading.value = false;
    });
}

function handleParallelSend(userMessage: string) {
    isLoading.value = true;
    
    // 为每个并行聊天实例启动独立的对话
    const parallelPromises = parallelChats.value.map(async (chat, index) => {
        
        // 添加用户消息到这个聊天实例
        chat.messages.push({
            role: 'user',
            content: userMessage,
            extraInfo: {
                created: Date.now(),
                state: MessageState.Success,
                serverName: chat.modelId,
                enableXmlWrapper: tabStorage.settings.enableXmlWrapper
            }
        });

        // 设置这个聊天实例为加载中
        chat.isLoading = true;
        chat.streamingContent = '';

        // 立即更新渲染消息以显示用户输入
        await updateChatRenderMessages(chat);

        // 创建独立的TaskLoop实例，避免状态共享
        const chatLoop = new TaskLoop({
            maxEpochs: tabStorage.settings.contextLength || 5,
            verbose: 0
        });
        
        const targetModelIndex = chat.llmIndex;
        
        try {
            // 为这个聊天实例创建完全独立的存储，包含独立的模型配置
            const chatStorage = {
                messages: [...chat.messages], // 深拷贝消息
                settings: {
                    ...tabStorage.settings,
                    // 强制设置当前模型索引，避免全局状态冲突
                    currentModelIndex: targetModelIndex,
                    // 关闭并行工具调用，避免索引冲突
                    parallelToolCalls: false
                }
            };
            
            // 动态注入模型索引到 chatLoop 的上下文中
            (chatLoop as any)._targetModelIndex = targetModelIndex;
            
            // 绑定流式输出到这个聊天实例
            const chatStreamingContent = ref('');
            const chatStreamingToolCalls = ref<ToolCall[]>([]);
            chatLoop.bindStreaming(chatStreamingContent, chatStreamingToolCalls);

            // 监听流式内容变化
            const stopWatchStreaming = watch(chatStreamingContent, (newContent) => {
                console.log(`[DEBUG] 模型 ${chat.modelId} 流式内容更新:`, newContent.slice(0, 50) + '...');
                chat.streamingContent = newContent;
            });

            // 防抖更新函数
            let updateTimer: NodeJS.Timeout | null = null;
            const debouncedUpdate = (newToolCalls: ToolCall[]) => {
                if (updateTimer) {
                    clearTimeout(updateTimer);
                }
                updateTimer = setTimeout(async () => {
                    await updateChatRenderMessages(chat, newToolCalls);
                    updateTimer = null;
                }, 50);
            };

            // 监听流式工具调用变化
            const stopWatchToolCalls = watch(chatStreamingToolCalls, (newToolCalls) => {
                console.log(`[DEBUG] 模型 ${chat.modelId} 工具调用更新:`, newToolCalls.length, '个工具调用');
                debouncedUpdate(newToolCalls);
            }, { deep: true });

            chatLoop.registerOnError((error) => {
                console.log(`[DEBUG] 模型 ${chat.modelId} 出错:`, error.msg);
                const errorMessage = clearErrorMessage(error.msg);
                
                chat.messages.push({
                    role: 'assistant',
                    content: errorMessage,
                    extraInfo: {
                        created: Date.now(),
                        state: error.state,
                        serverName: chat.modelId,
                        enableXmlWrapper: false
                    }
                });

                chat.isLoading = false;
                
                updateChatRenderMessages(chat);
            });

            chatLoop.registerOnDone(() => {
                chat.isLoading = false;
                chat.streamingContent = '';
                stopWatchStreaming();
                stopWatchToolCalls();
                if (updateTimer) {
                    clearTimeout(updateTimer);
                    updateTimer = null;
                }
            });

            // 临时保存和恢复模型索引，确保TaskLoop使用正确的模型
            const savedModelIndex = llmManager.currentModelIndex;
            if (targetModelIndex >= 0 && targetModelIndex < llms.length) {
                console.log(`[DEBUG] 模型 ${chat.modelId} 切换模型: ${savedModelIndex} -> ${targetModelIndex}`);
                llmManager.currentModelIndex = targetModelIndex;
            }
            
            console.log(`[DEBUG] 模型 ${chat.modelId} 开始TaskLoop执行，当前全局模型索引: ${llmManager.currentModelIndex}`);
            await chatLoop.start(chatStorage, '__SKIP_USER_MESSAGE__');
            console.log(`[DEBUG] 模型 ${chat.modelId} TaskLoop执行完成`);
            
            // 立即恢复模型索引
            if (savedModelIndex !== llmManager.currentModelIndex) {
                console.log(`[DEBUG] 模型 ${chat.modelId} 恢复模型: ${llmManager.currentModelIndex} -> ${savedModelIndex}`);
                llmManager.currentModelIndex = savedModelIndex;
            }
            
            // 更新存储中的消息
            chat.messages = chatStorage.messages;
            
            // 重新计算渲染消息
            await updateChatRenderMessages(chat);
            
        } catch (error) {
            console.error(`并行聊天 ${chat.modelId} 出错:`, error);
            chat.isLoading = false;
            chat.streamingContent = '';
        }
    });

    // 等待所有并行请求完成
    Promise.all(parallelPromises).then(() => {
        isLoading.value = false;
        
        // 更新存储
        tabStorage.parallelChats = parallelChats.value.map(chat => ({
            modelId: chat.modelId,
            messages: chat.messages
        }));
    });
}

function handleAbort() {
    if (loop) {
        loop.abort();
        isLoading.value = false;
        ElMessage.info('请求已中止');
    }
}


onMounted(() => {
    updateScrollHeight();
    window.addEventListener('resize', updateScrollHeight);
    scrollToBottom();
});

onUnmounted(() => {
    window.removeEventListener('resize', updateScrollHeight);
});


</script>

<style>
.chat-footer {
    padding: 16px;
    border-top: 1px solid var(--el-border-color);
    flex-shrink: 0;
    position: absolute;
    height: fit-content !important;
    bottom: 0;
    width: 100%;
}

.input-area {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
}

.input-wrapper {
    position: relative;
}

.chat-input {
    padding-right: 80px;
}

.chat-input textarea {
    border-radius: .5em;
}

.send-button {
    position: absolute !important;
    right: 8px !important;
    bottom: 8px !important;
    height: auto;
    padding: 8px 12px;
    font-size: 20px;
    border-radius: 1.2em !important;
}

:deep(.chat-settings) {
    position: absolute;
    left: 0;
    bottom: 0px;
    z-index: 1;
}

.typing-cursor {
    animation: blink 1s infinite;
}

@keyframes blink {
    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0;
    }
}
</style>