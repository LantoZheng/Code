<template>
    <div class="chat-toolbar">
        <el-select 
            v-model="chatMode"
            class="mode-selector"
        >
            <el-option 
                :label="t('single-chat')" 
                value="single-chat"
            />
            <el-option 
                :label="t('parallel-chat')" 
                value="parallel-chat"
            />
            <el-option 
                :label="t('tool-trace')" 
                value="tool-trace"
            />
        </el-select>

        <div v-if="chatMode === 'parallel-chat'" class="model-selector">
            <el-select 
                v-model="selectedModels"
                multiple 
                filterable
                :placeholder="t('choose-model-to-compare')"
                @change="initParallelChats"
                :filter-method="filterModels"
                :no-match-text="t('no-match-model')"
            >
                <el-option
                    v-for="model in filteredModels"
                    :key="model.id"
                    :label="model.name"
                    :value="model.id"
                />
            </el-select>
            <span v-if="parallelChats.length > 0" style="margin-left: 10px; font-size: 12px; width: 130px;">
                已选择 {{ parallelChats.length }} 个模型
            </span>
        </div>

        <!-- 单聊天模式下显示清空对话按钮 -->
        <div>
            <el-popconfirm 
                v-if="chatMode === 'single-chat'" 
                :title="t('dialog-delete-confirm')"
                @confirm="clearSingleChat"
            >
                <template #reference>
                    <el-button size="small">
                        <span class="iconfont icon-delete"></span>
                    </el-button>
                </template>
            </el-popconfirm>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// 定义组件的 props
const props = defineProps({
    chatMode: {
        type: String as () => 'single-chat' | 'parallel-chat' | 'tool-trace',
        required: true
    },
    selectedModels: {
        type: Array as () => string[],
        required: true
    },
    filteredModels: {
        type: Array as () => Array<{
            id: string;
            name: string;
            configIndex: number;
            modelName: string;
            providerName: string;
            isMultiModel: boolean;
        }>,
        required: true
    },
    parallelChats: {
        type: Array as () => Array<any>,
        required: true
    }
});

const chatMode = computed({
    get() {
        return props.chatMode;
    },
    set(value) {
        emit('update:chatMode', value);
    }
});

const selectedModels = computed({
    get() {
        return props.selectedModels;
    },
    set(value) {
        emit('update:selectedModels', value);
    }
});

// 定义组件的 emits
const emit = defineEmits<{
    (e: 'update:chatMode', value: 'single-chat' | 'parallel-chat' | 'tool-trace'): void;
    (e: 'update:selectedModels', value: string[]): void;
    (e: 'initParallelChats', value: string[]): void;
    (e: 'filterModels', query: string): void;
    (e: 'clearSingleChat'): void;
}>();

// 定义方法并转发到父组件
const changeChatMode = (value: string) => {
    emit('update:chatMode', value as 'single-chat' | 'parallel-chat' | 'tool-trace');
};

const initParallelChats = (value: string[]) => {    
    emit('initParallelChats', value);
};

const filterModels = (query: string) => {
    emit('filterModels', query);
};

const clearSingleChat = () => {
    emit('clearSingleChat');
};
</script>

<style scoped>
.chat-toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background-color: var(--sidebar);
    border-radius: 0.8em 0.8em 0 0;
    border-bottom: 1px solid var(--background);
}

.model-selector {
    display: flex;
    align-items: center;
    gap: 10px;
}

.mode-selector {
    width: 200px;
}
</style>