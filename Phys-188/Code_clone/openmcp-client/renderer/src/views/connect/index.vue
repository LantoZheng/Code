<template>
	<div class="connection-container-wrapper">
		<div class="server-list"
			:ref="el => mcpServerAddRef = el"
		>
			<el-segmented 
				v-model="mcpClientAdapter.currentClientIndex" 
				:options="serverOptions"
				style="background-color: var(--background);"
			>
				<template #default="scope"
					@click="selectServer(scope.item.index)"
				>
					<div class="server-item" :class="{ 'active': mcpClientAdapter.currentClientIndex === scope.index }">
						<span class="connect-status">
							<span v-if="scope.item.client.connectionResult.success"
								class="success"
							>
								<span class="iconfont icon-dui"></span>
								<span class="name">{{ scope.item.client.connectionResult.name }}</span>
							</span>
							<span v-else>
								<span class="server-name" style="margin-right: 60px;">
									<span class="iconfont icon-blank"></span>
								</span>
								<span class="iconfont icon-cuo"></span>
							</span>
						</span>
						<span
							v-if="scope.item.index > 0"
							class="delete-btn" @click.stop="deleteServer(scope.item.index)">
							<span class="iconfont icon-delete"></span>
						</span>
					</div>
				</template>
			</el-segmented>
			<div class="add-server" @click="addServer">
				<span class="iconfont icon-add"></span>
			</div>
		</div>
		<div class="panel-container" v-if="mcpClientAdapter.clients.length > 0">
			<ConnectionPanel :index="mcpClientAdapter.currentClientIndex" />
		</div>
		<div class="empty-state" v-else>
			<span class="iconfont icon-openmcp"></span>
			<span class="empty-text">{{ t('no-connect-right-now') }}</span>
		</div>
	</div>
</template>

<script setup lang="ts">
import { defineComponent, computed, reactive } from 'vue';
import { useI18n } from 'vue-i18n';
import ConnectionPanel from './connection-panel.vue';
import { McpClient, mcpClientAdapter } from './core';
import { ElMessage } from 'element-plus';
import { mcpServerAddRef } from '.';

defineComponent({ name: 'connection' });

const { t } = useI18n();

function selectServer(index: number) {
	mcpClientAdapter.currentClientIndex = index;
}

function addServer() {
	// const client = reactive(new McpClient());
	const client = new McpClient();
	mcpClientAdapter.clients.push(client);
	mcpClientAdapter.currentClientIndex = mcpClientAdapter.clients.length - 1;
	mcpClientAdapter.clients.at(-1)!.handleEnvSwitch(true);
}


const serverOptions = computed(() => {
    return mcpClientAdapter.clients.map((client, index) => ({
        value: index,
        label: `Server ${index + 1}`,
        client,
        index
    }));
});


function deleteServer(index: number) {
    if (mcpClientAdapter.clients.length <= 1) {
        ElMessage.warning(t('at-least-one-server'));
        return;
    }
    mcpClientAdapter.clients.splice(index, 1);
    if (mcpClientAdapter.currentClientIndex >= mcpClientAdapter.clients.length) {
        mcpClientAdapter.currentClientIndex = mcpClientAdapter.clients.length - 1;
    }
	mcpClientAdapter.saveLaunchSignature();
}
</script>

<style>
.connection-container-wrapper {
	display: flex;
	flex-direction: column;
	height: 100%;
}

.server-list {
	display: flex;
	align-items: center;
	width: 150px;
	border-right: 1px solid var(--border-color);
	padding: 0 25px;
}

.server-name {
	font-size: 12px;
}

.server-item {
	cursor: pointer;
	border-radius: 4px;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.server-item.active {
	background-color: var(--main-color);
	color: white;
}

.server-item .name {
	width: 100px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	margin-left: 5px;
}

.server-item .success {
	display: flex;
	align-items: center;
}

.server-status {
	font-size: 12px;
}

.server-status.connected {
	color: green;
}

.server-status.disconnected {
	color: red;
}

.add-server {
	padding: 10px;
	text-align: center;
	cursor: pointer;
	border-radius: 4px;
	border: 1px dashed var(--border-color);
}

.add-server:hover {
	background-color: var(--background);
}

.panel-container {
	flex: 1;
	padding: 5px;
}

.delete-btn {
    margin-left: 10px;
    cursor: pointer;
    color: var(--error-color);
}
.delete-btn:hover {
    opacity: 0.8;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--text-secondary);
}

.empty-state .iconfont {
    font-size: 128px;
    margin-bottom: 16px;
}

.empty-text {
    font-size: 18px;
    color: var(--text-secondary);
}
</style>