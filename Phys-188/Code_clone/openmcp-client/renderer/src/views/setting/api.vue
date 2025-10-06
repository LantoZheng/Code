<template>
	<div class="setting-section"
		:ref="el => llmSettingRef = el"
	>
		<h2 class="api-title">
			{{ "API" }}
		</h2>
		<div class="setting-option">
			<span>
				<span class="iconfont icon-company"></span>
				<span class="option-title">{{ t('server-provider') }}</span>
			</span>
			<div style="width: 160px;">
				<el-select name="language-setting" class="language-setting" v-model="llmManager.currentModelIndex"
					@change="onmodelchange">

					<el-option v-for="(option, index) in llms" :value="index" :label="option.name" :key="index">
						<div class="llm-option">
							<span>{{ option.name }}</span>
							<el-dropdown trigger="hover" @command="handleCommand">
								<span>
									<span class="iconfont icon-more"></span>
								</span>
								<template #dropdown>
									<el-dropdown-menu>
										<el-dropdown-item :command="{type: 'edit', index}">
											<span class="iconfont icon-edit">&emsp;{{ t('edit') }}</span>
										</el-dropdown-item>
										<el-dropdown-item :command="{type: 'delete', index}" divided>
											<span class="iconfont icon-delete">&emsp;{{ t('delete') }}</span>
										</el-dropdown-item>
									</el-dropdown-menu>
								</template>
							</el-dropdown>
						</div>
					</el-option>
				</el-select>
			</div>
		</div>

		<!-- TODO: 根据不同模型展示不同的接入点 -->
		<div v-if="false">

		</div>
		<div v-else>
			<ConnectInterfaceOpenai />
		</div>

		<br>

		<div class="setting-save-container">
			<el-button
				id="add-new-server-button"
				type="success"
				@click="addNewServer"
			>
				{{ t("add-new-server") }}
			</el-button>

			<el-button
				id="add-new-server-button"
				type="success"
				@click="updateModels"
				:loading="updateModelLoading"
			>
				{{ t('update-model-list') }}
			</el-button>

			<!-- 新增：测试 prompt 下拉输入 -->
			<el-popover
				placement="top"
				width="400"
				trigger="click"
				v-model:visible="testPromptPopoverVisible"
			>
				<template #reference>
                    <el-button
                        type="primary"
                        id="test-llm-button"
                        :loading="simpleTestResult.start"
                    >
                        <span v-show="!simpleTestResult.start" class="iconfont icon-test"></span>
                        {{ t('test') }}
                    </el-button>
				</template>
				<div style="margin-bottom: 8px; font-weight: bold;">
                        {{ t('prompts') }}
				</div>
				<el-input
					type="textarea"
					v-model="testPrompt"
					:rows="3"
					:placeholder="t('test-prompt-placeholder') || '输入测试内容...'"
					style="margin-bottom: 8px;"
					clearable
				/>
				<div style="text-align: right;">
					<el-button size="small" @click="testPromptPopoverVisible = false">{{ t('cancel') }}</el-button>
					<el-button size="small" type="primary" @click="testPromptPopoverVisible = false; makeSimpleTalk()">{{ t('confirm') }}</el-button>
				</div>
			</el-popover>

			<el-button
				type="primary"
				id="save-llm-button"
				@click="saveLlmSetting"
			>
				<span class="iconfont icon-save"></span>
				{{ t('save') }}
			</el-button>
		</div>


		<!-- 测试连通性的地方 -->
		<ConnectTest />

		<!-- 当前页面的聊天框 -->
		<el-dialog v-model="dialogVisible" width="50%" class="api-man-dialog">
			
			<br>

			<el-form :model="newProviderForm" label-width="auto">
				<el-form-item :label="t('server-provider')">
					<el-input v-model="newProviderForm.provider" />
				</el-form-item>
				<el-form-item :label="t('model')">
					<el-input-tag
						v-model="newProviderForm.models"
						placeholder="gpt-3.5-turbo"
					/>
				</el-form-item>
				<el-form-item :label="t('api-root-url')">
					<el-input v-model="newProviderForm.baseUrl" placeholder="https://" />
				</el-form-item>
				<el-form-item :label="t('api-token')">
					<el-input v-model="newProviderForm.userToken" show-password />
				</el-form-item>
			</el-form>
			<template #footer>
				<el-button @click="dialogVisible = false">{{ t("cancel") }}</el-button>
				<el-button type="primary" @click="dialogConfirm">{{ t("confirm") }}</el-button>
			</template>
		</el-dialog>
	</div>
</template>

<script setup lang="ts">
import { defineComponent, ref } from 'vue';
import { llmManager, llms } from './llm';
import { useI18n } from 'vue-i18n';
import { saveSetting } from '@/hook/setting';
import { ElMessage, ElMessageBox } from 'element-plus';
import { pinkLog } from './util';

import ConnectInterfaceOpenai from './connect-interface-openai.vue';
import ConnectTest from './connect-test.vue';
import { llmSettingRef, makeSimpleTalk, simpleTestResult, testPrompt } from './api';
import { useMessageBridge } from '@/api/message-bridge';
import { mcpSetting } from '@/hook/mcp';

defineComponent({ name: 'api' });
const { t } = useI18n();

function saveLlmSetting() {
	saveSetting(() => {
		ElMessage({
			message: t('success-save'),
			type: 'success'
		});
	});
}

const currentDialogMode = ref('');
const dialogVisible = ref(false);
const testPromptPopoverVisible = ref(false);

function addNewServer() {
	newProviderForm.value = {
        provider: '',
        models: [],
        baseUrl: '',
        userToken: ''
    };

	currentDialogMode.value = 'add';
	dialogVisible.value = true;
}

function editModel(index: number) {
	currentDialogMode.value = 'edit';
	editingIndex.value = index;

	const formData = JSON.parse(JSON.stringify(llms[index]));
	newProviderForm.value = {
		provider: formData.name,
		models: formData.models,
		baseUrl: formData.baseUrl,
		userToken: formData.userToken
	};

	dialogVisible.value = true;
}



const newProviderForm = ref<{
	provider: string;
	models: string[];
	baseUrl: string;
	userToken: string;
}>({
	provider: '',
	models: [],
	baseUrl: '',
	userToken: ''
});

const editingIndex = ref(-1);


function dialogConfirm() {
	if (currentDialogMode.value === 'add') {
		addNewProvider();
	} else if (currentDialogMode.value === 'edit') {
		updateProvider();
	}
}

function addNewProvider() {
	const formData = JSON.parse(JSON.stringify(newProviderForm.value));

	llms.push({
		id: formData.provider,
		name: formData.provider,
		models: formData.models,
		userModel: formData.models[0],
		baseUrl: formData.baseUrl,
		userToken: formData.userToken,
		isOpenAICompatible: true,
		description: "User Defined Server",
		website: "",
	});	

	dialogVisible.value = false;
	newProviderForm.value = {
		provider: '',
		models: [],
		baseUrl: '',
		userToken: ''
	};
}


const updateModelLoading = ref(false);

async function updateModels() {
	updateModelLoading.value = true;

	const llm = llms[llmManager.currentModelIndex];
	const apiKey = llm.userToken;
	const baseURL = llm.baseUrl;
    const proxyServer = mcpSetting.proxyServer;

	const bridge = useMessageBridge();
	
	// 检查是否为动态模型加载（如OpenRouter）
	let result;
	if (llm.isDynamic && llm.id === 'openrouter') {
		result = await bridge.commandRequest('llm/models/openrouter', {});
	} else {
		result = await bridge.commandRequest('llm/models', {
			apiKey,
			baseURL,
			proxyServer
		});
	}

	const { code, msg } = result;
	const isGemini = baseURL.includes('googleapis');
	const isOpenRouter = llm.id === 'openrouter';

	if (code === 200 && Array.isArray(msg)) {
		const models = msg
			.filter(item => item.object === 'model')
			.map(item => {
				let modelName = item.id as string;
				if (isGemini && modelName.includes('/')) {
					modelName = modelName.split('/')[1];
				}
				return modelName;
			});
		
		llm.models = models;
		
		// 如果是OpenRouter且尚未设置默认模型，设置一个推荐的模型
		if (isOpenRouter && !llm.userModel && models.length > 0) {
			// 寻找GPT-4或类似的推荐模型
			const recommendedModel = models.find(model => 
				model.includes('gpt-4') || 
				model.includes('claude') || 
				model.includes('gemini')
			) || models[0];
			llm.userModel = recommendedModel;
		}
		
		saveLlmSetting();
		
		if (isOpenRouter) {
			ElMessage.success(`已更新 ${models.length} 个 OpenRouter 模型`);
		} else {
			ElMessage.success('模型列表更新成功');
		}
	} else {
		ElMessage.error('模型列表更新失败: ' + msg);
	}
	updateModelLoading.value = false;
}

function updateProvider() {
	if (editingIndex.value < 0) {
		return;
	}

    const formData = JSON.parse(JSON.stringify(newProviderForm.value));
	
    llms[editingIndex.value] = {
        ...llms[editingIndex.value],
		id: formData.provider,
        name: formData.provider,
        models: formData.models,
        userModel: formData.models[0] || '',
        baseUrl: formData.baseUrl,
        userToken: formData.userToken
    };

	console.log(llms[editingIndex.value]);
	
    newProviderForm.value = {
        provider: '',
        models: [],
        baseUrl: '',
        userToken: ''
    };

	dialogVisible.value = false;
	saveLlmSetting();
}

function onmodelchange() {
	pinkLog('切换模型到：' + llms[llmManager.currentModelIndex].id);
	saveLlmSetting();
}

function deleteModel(index: number) {
    if (llms.length <= 1) {
        ElMessage.warning(t('reserve-one-last-model'));
        return;
    }
    
    ElMessageBox.confirm(
        t('confirm-delete-model'),
        'warning',
        {
            confirmButtonText: t('confirm'),
            cancelButtonText: t('cancel'),
            type: 'warning',
        }
    ).then(() => {
        llms.splice(index, 1);
        
        if (llmManager.currentModelIndex === index) {
            llmManager.currentModelIndex = 0;
        } else if (llmManager.currentModelIndex > index) {
            llmManager.currentModelIndex --;
        }

		saveLlmSetting();
    }).catch(() => {
        // 用户取消删除
    });
}

function handleCommand(command: {type: string, index: number}) {
    if (command.type === 'edit') {
        editModel(command.index);
    } else if (command.type === 'delete') {
        deleteModel(command.index);
    }
}
</script>

<style>

.api-man-dialog {
	min-width: 500px;
	max-width: 800px;
	padding: 20px;
}

.api-man-dialog .el-tag {
	background-color: var(--main-light-color) !important;
}

.setting-save-container {
	margin: 5px;
}

.setting-save-container .iconfont {
	margin-right: 5px;
	font-weight: 700;
}

.api-title {
	display: flex;
	align-items: center;
}


.api-title .iconfont {
	font-weight: 300;
	font-size: 18px;
	margin-left: 10px;
	cursor: pointer;
	transition: var(--animation-3s);
}

.api-title .iconfont:hover {
	color: var(--main-color);
}

.llm-option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
	--el-color-primary: white;
}

.delete-icon {
    color: var(--el-color-danger);
    cursor: pointer;
    margin-left: 10px;
}

.delete-icon:hover {
    opacity: 0.8;
}
</style>