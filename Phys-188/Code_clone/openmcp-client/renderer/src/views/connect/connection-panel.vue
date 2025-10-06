<template>
	<el-scrollbar height="98%">
		<div class="connection-container" @dragover.prevent="handleDragOver" @drop.prevent="handleDrop">
			<div v-if="isDraging" class="drag-mask">
				<span class="iconfont icon-connect"></span>
				<span>{{ t('drag-to-fill-connect-parameters') }}</span>
			</div>
			<div class="connect-panel-container left" :ref="el => client.connectionSettingRef = el">
				<ConnectionMethod :index="props.index" />
				<ConnectionArgs :index="props.index" />
				<ConnectionEnvironment :index="props.index" />

				<div class="connect-action">
					<el-button
                        type="primary"
                        size="large"
                        :loading="isLoading"
						@click="connect()"
                    >
						<span class="iconfont icon-connect" v-if="!isLoading"></span>
						{{ t('connect.appearance.connect') }}
					</el-button>

                    <el-button
                        type="danger"
                        size="large"
                        :loading="isDisconnecting"
                        :disabled="!client.connectionResult.success"
						@click="disconnect()"
                    >
						<span class="iconfont icon-disconnect" v-if="!isDisconnecting"></span>
						{{ t('connect.appearance.disconnect') }}
					</el-button>
				</div>
			</div>

			<div class="connect-panel-container right" :ref="el => client.connectionLogRef = el">
				<ConnectionLog :index="props.index" />
			</div>
		</div>
	</el-scrollbar>
</template>

<script setup lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { useI18n } from 'vue-i18n';

import ConnectionMethod from './connection-method.vue';
import ConnectionArgs from './connection-args.vue';
import ConnectionEnvironment from './connection-environment.vue';
import ConnectionLog from './connection-log.vue';

import { getPlatform } from '@/api/platform';
import { mcpClientAdapter } from './core';

defineComponent({ name: 'connection-panel' });

const props = defineProps({
	index: {
		type: Number,
		required: true
	}

});

const client = computed(() => mcpClientAdapter.clients[props.index]);

const { t } = useI18n();

const isLoading = ref(false);
const isDisconnecting = ref(false);

async function connect() {
	isLoading.value = true;

	const ok = await client.value.connect();

	if (ok) {
		mcpClientAdapter.saveLaunchSignature();
	}

	isLoading.value = false;
}

// 添加断开连接功能
async function disconnect() {
	isDisconnecting.value = true;
	
	try {
		await client.value.disconnect();
	} catch (error) {
		console.error('Disconnect error:', error);
	} finally {
		isDisconnecting.value = false;
	}
}

const isDraging = ref(false);
let dragHandler: NodeJS.Timeout;

function handleDragOver(event: DragEvent) {
	event.preventDefault();
	clearTimeout(dragHandler);
	isDraging.value = true;

	dragHandler = setTimeout(() => {
		isDraging.value = false;
	}, 100);
}


function getLaunchCommand(fileName: string) {
	const ext = fileName.split('.').pop()?.toLowerCase();
	switch (ext) {
		case 'py':
			return `mcp run ${fileName}`;
		
		case 'js':
			return `node ${fileName}`;

		default:
			return fileName;
	}
}

function handleDrop(event: DragEvent) {
	event.preventDefault();

	const dragedFilePath = event.dataTransfer?.getData('text/plain') || '';
	if (dragedFilePath) {
		const path = dragedFilePath.replace(/\\/g, '/');
		const coms = path.split('/');
		const fileName = coms[coms.length - 1];
		const cwd = coms.slice(0, coms.length - 1).join('/');

		const command = getLaunchCommand(fileName);
		client.value.connectionArgs.connectionType = 'STDIO';
		client.value.connectionArgs.commandString = command;		
		client.value.connectionArgs.cwd = cwd;
	}

	isDraging.value = false;

	// const files = event.dataTransfer?.files;
	// if (files && files.length > 0) {
	// 	for (let i = 0; i < files.length; i++) {
	// 		console.log('拖拽的文件:', files[i]);
	// 	}
	// }
}

</script>

<style>
.connection-container {
	display: flex;
	max-height: 85vh;
}


.connect-panel-container.left {
	display: flex;
	flex-direction: column;
	width: 45%;
	max-width: 500px;
	min-width: 350px;
	padding: 5px 20px;
}

.connect-panel-container.right {
	display: flex;
	flex-direction: column;
	width: 55%;
	min-width: 450px;
	padding: 5px 20px;
}


.connection-option {
	display: flex;
	flex-direction: column;
	background-color: var(--background);
	padding: 10px;
	margin-bottom: 20px;
	border-radius: .5em;
	border: 1px solid var(--background);
}

.connection-option>span:first-child {
	margin-bottom: 5px;
}

.input-env-container {
	display: flex;
	margin-bottom: 10px;
}

.display-env {
	padding-top: 10px;
	padding-bottom: 10px;
}

.input-env-container>span {
	width: 150px;
	margin-right: 10px;
	display: flex;
	height: 30px;
	align-items: center;
}

.input-env-container .iconfont {
	font-size: 20px;
	border-radius: 99em;
	color: var(--foreground);
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: var(--animation-3s);
	user-select: none;
}

.input-env-container .iconfont:hover {
	color: var(--main-color);
	transition: var(--animation-3s);
}

.connect-action {
	padding: 10px;
}

.drag-mask {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.5);
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	color: white;
	font-size: 18px;
	z-index: 9999;
}

.drag-mask .iconfont {
	font-size: 80px;
	margin-bottom: 20px;
}
</style>