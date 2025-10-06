<template>
    <el-tooltip :content="t('choose-model')" placement="top" effect="light">
        <div class="setting-button" @click="showModelDialog = true">
            <span class="iconfont icon-model">
                {{ currentServerName }}/{{ currentModelName }}
            </span>
        </div>
    </el-tooltip>

    <!-- 模型选择对话框 -->
    <el-dialog v-model="showModelDialog" :title="t('choose-model')" width="400px">
        <!-- 搜索框 -->
        <el-input 
            v-model="searchText" 
            :placeholder="t('search-model')" 
            clearable
            style="margin-bottom: 15px;"
        >
            <template #prefix>
                <span class="iconfont icon-search"></span>
            </template>
        </el-input>
        
        <!-- 模型列表 -->
        <el-radio-group v-model="selectedModelIndex" @change="onRadioGroupChange">
            <div class="model-list">
                <el-radio 
                    v-for="(model, index) in filteredModels" 
                    :key="index" 
                    :value="index"
                    class="model-item"
                >
                    {{ model }}
                </el-radio>
            </div>
        </el-radio-group>
        <template #footer>
            <el-button @click="showModelDialog = false">{{ t("cancel") }}</el-button>
            <el-button type="primary" @click="confirmModelChange">{{ t("confirm") }}</el-button>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { saveSetting } from '@/hook/setting';
import { llmManager, llms } from '@/views/setting/llm';
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const showModelDialog = ref(false);
const searchText = ref('');
const currentModel = llms[llmManager.currentModelIndex].userModel;
const selectedModelIndex = ref(llms[llmManager.currentModelIndex].models.indexOf(currentModel));

const currentServerName = computed(() => {
	const currentLlm = llms[llmManager.currentModelIndex];
	if (currentLlm) {
		return currentLlm.name;
	}
	return '';
});

const currentModelName = computed(() => {
	const currentLlm = llms[llmManager.currentModelIndex];
	if (currentLlm) {
		return currentLlm.models[selectedModelIndex.value];
	}
	return '';
});

const availableModels = computed(() => {
	return llms[llmManager.currentModelIndex].models;
});

const filteredModels = computed(() => {
    if (!searchText.value) {
        return availableModels.value;
    }
    
    const searchTerm = searchText.value.toLowerCase().trim();
    return availableModels.value.filter(model => 
        model.toLowerCase().startsWith(searchTerm)
    );
});

const confirmModelChange = () => {
	showModelDialog.value = false;
};

const onRadioGroupChange = () => {
	const currentModel = llms[llmManager.currentModelIndex].models[selectedModelIndex.value];
	llms[llmManager.currentModelIndex].userModel = currentModel;
	saveSetting();
};

</script>

<style>
.setting-button:hover {
    background: var(--main-light-color, #f0f8ff);
    box-shadow: 0 2px 8px 0 rgba(64,158,255,0.08);
    border-color: var(--el-color-primary-light-7, #c6e2ff);
}

.setting-button:active {
    transform: scale(0.95);
}

.model-list {
    max-height: 300px;
    width: 100%;
}

.model-item {
    display: flex;
    align-items: center;
    width: 100%;
    margin-bottom: 10px;
    padding: 8px 12px;
    border-radius: 4px;
}

.model-item:hover {
    background-color: var(--el-fill-color-light);
}
</style>