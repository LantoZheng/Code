<template>
    <div class="message-role"></div>
    <div class="message-text">
        <div v-if="!isEditing" class="message-content">
            <span>
                {{ props.message.content.trim() }}
            </span>
        </div>
        
        <KCuteTextarea v-else
            v-model="userInput"
            :placeholder="t('enter-message-dot')"
            @press-enter="handleKeydown"
        />
        <div class="message-actions" v-if="!isEditing">
            <el-button @click="copy">
                <span class="iconfont icon-copy"></span>
            </el-button>
            <el-button @click="reload">
                <span class="iconfont icon-restart"></span>
            </el-button>
            <el-button @click="toggleEdit">
                <span class="iconfont icon-edit2"></span>
            </el-button>
        </div>
        <div class="message-actions" v-else>
            <el-button @click="toggleEdit">
                {{ '取消' }}
            </el-button>
            <el-button @click="handleKeydown" type="primary">
                {{ '发送' }}
            </el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, ref, type PropType, inject, watch, type Ref } from 'vue';
import { tabs } from '../../panel';
import type { ChatStorage, IRenderMessage } from '../chat-box/chat';
import { MessageState } from '../chat-box/chat';

import KCuteTextarea from '@/components/k-cute-textarea/index.vue';
import { ElMessage } from 'element-plus';

import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps({
    message: {
        type: Object as PropType<IRenderMessage>,
        required: true
    },
    tabId: {
        type: Number,
        required: true
    }
});

const tab = tabs.content[props.tabId];
const tabStorage = tab.storage as ChatStorage;
const isEditing = ref(false);
const userInput = ref('');

const chatContext = inject('chatContext') as any;

// 在setup顶层获取并行模式相关的注入值
const chatMode = inject('chatMode') as Ref<string>;
const parallelChats = inject('parallelChats') as Ref<any[]>;
const updateChatRenderMessages = inject('updateChatRenderMessages') as any;

const toggleEdit = () => {
    isEditing.value = !isEditing.value;
    if (isEditing.value) {
        userInput.value = props.message.content;
    }
};

const handleKeydown = (event: KeyboardEvent) => {
    console.log(chatContext);
    
    if (chatMode.value === 'parallel-chat' && parallelChats?.value?.length > 0) {
        // 并行模式：只编辑当前消息所属的聊天实例
        const messageServerName = props.message.extraInfo.serverName;
        
        // 找到对应的聊天实例
        const targetChat = parallelChats.value.find((chat: any) => chat.modelId === messageServerName);
        
        if (targetChat) {
            const index = targetChat.messages.findIndex((msg: any) => msg.extraInfo === props.message.extraInfo);
            if (index !== -1) {
                // 把 index 之后的全部删除（包括 index）
                targetChat.messages.splice(index);
                
                // 重新计算渲染消息
                if (updateChatRenderMessages) {
                    updateChatRenderMessages(targetChat);
                }
            }
            
            // 更新存储
            if (tabStorage.parallelChats) {
                tabStorage.parallelChats = parallelChats.value.map((chat: any) => ({
                    modelId: chat.modelId,
                    messages: chat.messages
                }));
            }
            
            // 只对这个特定的聊天实例重新发送消息
            retrySingleChat(targetChat, userInput.value);
            isEditing.value = false;
        }
    } else {
        // 单聊天模式：清理主消息列表
        const index = tabStorage.messages.findIndex(msg => msg.extraInfo === props.message.extraInfo);
        if (index !== -1) {
            // 把 index 之后的全部删除（包括 index）
            tabStorage.messages.splice(index);
        }
        
        if (chatContext.handleSend) {
            chatContext.handleSend(userInput.value);
            isEditing.value = false;
        }
    }
};

const copy = async () => {
    try {        
        await navigator.clipboard.writeText(props.message.content.trim());
        ElMessage.success('内容已复制到剪贴板');
    } catch (err) {
        console.error('无法复制内容: ', err);
        ElMessage.error('复制失败，请手动复制');
    }
};

// 单个聊天实例重试函数
const retrySingleChat = async (chat: any, userMessage: string) => {
    console.log('开始单实例重试，聊天实例:', chat.modelId);
    console.log('重试消息:', userMessage);
    
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

    console.log('设置聊天实例为加载中:', chat.modelId);

    // 立即更新渲染消息以显示用户输入
    if (updateChatRenderMessages) {
        await updateChatRenderMessages(chat);
    }

    // 导入需要的依赖
    const { TaskLoop } = await import('../core/task-loop');
    const { llmManager, llms } = await import('@/views/setting/llm');
    
    // 创建独立的TaskLoop
    const chatLoop = new TaskLoop();
    
    // 为这个聊天实例创建临时存储
    const chatStorage = {
        messages: chat.messages,
        settings: { ...tabStorage.settings }
    };
    
    // 临时改变当前模型为这个聊天实例的模型
    const originalModelIndex = llmManager.currentModelIndex;
    const targetModelIndex = parseInt(chat.modelId);
    
    if (!isNaN(targetModelIndex) && targetModelIndex >= 0 && targetModelIndex < llms.length) {
        llmManager.currentModelIndex = targetModelIndex;
    }

    // 绑定流式输出到这个聊天实例
    const chatStreamingContent = ref('');
    const chatStreamingToolCalls = ref([]);
    chatLoop.bindStreaming(chatStreamingContent, chatStreamingToolCalls);

    // 监听流式内容变化
    const stopWatchStreaming = watch(chatStreamingContent, (newContent) => {
        chat.streamingContent = newContent;
    });

    chatLoop.registerOnError((error: any) => {
        chat.messages.push({
            role: 'assistant',
            content: error.msg,
            extraInfo: {
                created: Date.now(),
                state: error.state,
                serverName: chat.modelId,
                enableXmlWrapper: false
            }
        });
        
        // 重新计算渲染消息
        updateChatRenderMessages(chat);
    });

    chatLoop.registerOnDone(() => {
        chat.isLoading = false;
        chat.streamingContent = '';
        stopWatchStreaming();
    });

    try {
        // 使用特殊标记来表示不需要添加用户消息，因为我们已经手动添加了
        await chatLoop.start(chatStorage, '__SKIP_USER_MESSAGE__');
        
        // 恢复原始模型
        llmManager.currentModelIndex = originalModelIndex;
        
        // 更新存储中的消息
        chat.messages = chatStorage.messages;
        
        // 重新计算渲染消息
        await updateChatRenderMessages(chat);
        
    } catch (error) {
        console.error(`重试聊天 ${chat.modelId} 出错:`, error);
        chat.isLoading = false;
        chat.streamingContent = '';
        stopWatchStreaming();
        llmManager.currentModelIndex = originalModelIndex;
    }
};

const reload = async () => {
    console.log('重试按钮被点击');
    console.log('并行模式:', chatMode.value);
    console.log('并行聊天数量:', parallelChats?.value?.length);
    console.log('消息信息:', props.message);
    
    if (chatMode.value === 'parallel-chat' && parallelChats?.value?.length > 0) {
        // 并行模式：只重试当前消息所属的聊天实例
        const messageServerName = props.message.extraInfo.serverName;
        console.log('消息所属服务器:', messageServerName);
        console.log('可用的聊天实例:', parallelChats.value.map((chat: any) => chat.modelId));
        
        // 找到对应的聊天实例
        const targetChat = parallelChats.value.find((chat: any) => chat.modelId === messageServerName);
        
        console.log('找到的目标聊天实例:', targetChat);
        
        if (targetChat) {
            const index = targetChat.messages.findIndex((msg: any) => msg.extraInfo === props.message.extraInfo);
            console.log('消息在目标聊天实例中的索引:', index);
            
            if (index !== -1) {
                // 把 index 之后的全部删除（包括 index）
                targetChat.messages.splice(index);
                
                // 重新计算渲染消息
                if (updateChatRenderMessages) {
                    await updateChatRenderMessages(targetChat);
                }
            }
            
            // 更新存储
            if (tabStorage.parallelChats) {
                tabStorage.parallelChats = parallelChats.value.map((chat: any) => ({
                    modelId: chat.modelId,
                    messages: chat.messages
                }));
            }
            
            console.log('调用单实例重试');
            // 只对这个特定的聊天实例重新发送消息
            retrySingleChat(targetChat, props.message.content);
        } else {
            console.log('未找到目标聊天实例，不执行重试');
            console.error('无法找到匹配的聊天实例进行重试');
            ElMessage.error('无法找到对应的聊天实例进行重试');
        }
    } else {
        console.log('单聊天模式，使用原有逻辑');
        // 单聊天模式：清理主消息列表
        const index = tabStorage.messages.findIndex(msg => msg.extraInfo === props.message.extraInfo);
        if (index !== -1) {
            // 把 index 之后的全部删除（包括 index）
            tabStorage.messages.splice(index);
        }
        
        if (chatContext.handleSend) {
            chatContext.handleSend(props.message.content);
        }
    }
};

</script>

<style>

.message-text {
    position: relative;
}

.message-text:hover .message-actions {
    opacity: 1;
}

.message-actions {
    opacity: 0;
    transition: var(--animation-3s);
    position: absolute;
    bottom: -34px;
    right: 0;    
}

.message-actions .el-button {
    border-radius: .5em;
    padding: 5px 8px;
}

.message-actions .el-button:hover {
    background-color: var(--main-light-color);
}

.message-actions .el-button+.el-button {
    margin-left: 10px;
}

.user .message-content {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
}

.user .message-content > span {
    max-width: calc(100% - 48px);
    border-radius: .9em;
    background-color: var(--main-light-color);
    padding: 10px 15px;
    box-sizing: border-box;
    white-space: pre-wrap;
    word-break: break-word;
    text-align: left;
}

</style>