<template>
	<el-collapse :expand-icon-position="'left'" v-model="tabStorage.activeNames">
		<el-collapse-item v-for="(client, index) in mcpClientAdapter.clients" :name="index" :class="[]">

			<!-- header -->
			<template #title>
				<h3 class="resource-template">
					<span>resources/list</span>
					<span class="iconfont icon-restart" @click.stop="reloadResources(client, { first: false })"></span>
				</h3>
			</template>

			<!-- body -->
			<div class="resource-template-container-scrollbar">
				<el-scrollbar height="fit-content" v-if="(client.resources?.size || 0) > 0">
					<div class="resource-template-container">
						<div class="item"
							:class="{ 'active': props.tabId >= 0 && tabStorage.currentType === 'resource' && tabStorage.currentResourceName === resource.name }"
							v-for="resource of client.resources?.values()" :key="resource.uri"
							@click="handleClick(resource)">
							<span class="resource-title">{{ resource.name }}</span>
							<span class="resource-description">{{ resource.mimeType }}</span>
						</div>
					</div>
				</el-scrollbar>
				<div v-else style="padding: 10px;">
					<div class="empty-description">
						<span class="iconfont icon-empty" style="font-size: 22px; opacity: 0.4; margin-right: 6px;"></span>
						<span style="opacity: 0.6;">No resources found.</span>
					</div>
				</div>
			</div>
		</el-collapse-item>
	</el-collapse>
</template>

<script setup lang="ts">
import type { Resources } from '@/hook/type';
import { onMounted, defineProps, defineEmits, reactive, type Reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import type { ResourceStorage } from './resources';
import { tabs } from '../panel';
import { ElMessage } from 'element-plus';
import { McpClient, mcpClientAdapter } from '@/views/connect/core';

const { t } = useI18n();

const props = defineProps({
	tabId: {
		type: Number,
		required: true
	}
});

const emits = defineEmits(['resource-selected']);

let tabStorage: ResourceStorage;

if (props.tabId >= 0) {
	const tab = tabs.content[props.tabId];
	tabStorage = tab.storage as ResourceStorage;
} else {
	tabStorage = reactive({
		activeNames: [0],
		templateActiveNames: [0],
		currentType: 'resource',
		currentResourceName: '',
		formData: {},
		lastResourceReadResponse: undefined
	});
}

async function reloadResources(client: Reactive<McpClient>, option: { first: boolean }) {
	await client.getResources({ cache: false });

	if (!option.first) {
		ElMessage({
			message: t('finish-refresh'),
			type: 'success',
			duration: 3000,
			showClose: true,
		});
	}
}

async function handleClick(resource: Resources) {
	tabStorage.currentType = 'resource';
	tabStorage.currentResourceName = resource.name;
	tabStorage.lastResourceReadResponse = undefined;
	emits('resource-selected', resource);

	// 更新资源
	if (props.tabId >= 0) {
		const res = await mcpClientAdapter.readResource(resource.uri);
		tabStorage.lastResourceReadResponse = res;
	}
}

onMounted(async () => {
	if (tabStorage.currentResourceName === undefined && tabStorage.currentType === 'resource') {
		const masterNode = mcpClientAdapter.masterNode;
		const resource = masterNode.resources?.values().next();
		tabStorage.currentResourceName = resource?.value?.name || '';
	}
});

</script>

<style>
h3.resource-template {
	display: flex;
	align-items: center;
}

h3.resource-template .iconfont.icon-restart {
	margin-left: 10px;
	cursor: pointer;
}

h3.resource-template .iconfont.icon-restart:hover {
	color: var(--main-color);
}

.resource-template-container-scrollbar {
	background-color: var(--background);
	margin-bottom: 10px;
	border-radius: .5em;
}

.resource-template-container {
	height: fit-content;
	display: flex;
	flex-direction: column;
	padding: 10px;
}

.resource-template-function-container {
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.resource-template-function-container button {
	width: 175px;
}

.resource-template-container > .item {
	margin: 3px;
	padding: 5px 10px;
	border-radius: .3em;
	user-select: none;
	cursor: pointer;
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	transition: var(--animation-3s);
}

.resource-template-container > .item:hover {
	background-color: var(--main-light-color);
	transition: var(--animation-3s);
}

.resource-template-container > .item.active {
	background-color: var(--main-light-color);
	transition: var(--animation-3s);
}

.resource-template-container > .item:active {
    transform: scale(0.95);
    transition: var(--animation-3s);
}

.resource-title {
	font-weight: bold;
	max-width: 250px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.resource-description {
	opacity: 0.6;
	font-size: 12.5px;
	max-width: 250px;
	/* Remove ellipsis and allow full text wrap */
	overflow: visible;
	text-overflow: unset;
	white-space: normal;
	word-break: break-all;
}

.empty-description {
	display: flex;
	align-items: center;
	justify-content: center;
	color: var(--el-text-color-placeholder, #bbb);
	font-size: 15px;
	min-height: 40px;
}
</style>