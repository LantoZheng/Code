<template>
	<div v-if="!isConnecting" class="connected-status-container" id="connected-status-container"
		@click.stop="toggleConnectionPanel()" :class="{ 'connected': client.connectionResult.success }">
		<span class="mcp-server-info">
			<el-tooltip class="extra-connect-container" effect="light" placement="right"
				:content="mcpClientAdapter.masterNode.connectionResult.name + ' / ' + mcpClientAdapter.masterNode.connectionResult.version"
            >
				<span class="name">{{ displayServerName }}</span>
			</el-tooltip>
		</span>
		<span class="connect-status">
			<span v-if="client.connectionResult.success">
				<span class="iconfont icon-connect"></span>
				<span class="iconfont icon-dui"></span>
			</span>
			<span v-else>
				<span class="iconfont icon-connect"></span>
				<span class="iconfont icon-cuo"></span>
			</span>
		</span>
	</div>
	<div v-else class="connected-status-container">
		<span class="mcp-server-info">
			<el-tooltip class="extra-connect-container" effect="light" placement="right"
				:content="'loading ...'"
            >
				<span class="name">
					{{ t("loading") }}
				</span>
			</el-tooltip>
		</span>
		<span class="connect-status">
			<span style="display: flex;">
				<span class="iconfont icon-connect"></span>
				<div class="custom-loading">
					<svg class="circular" viewBox="-10, -10, 50, 50">
						<path class="path" d="
            M 30 15
            L 28 17
            M 25.61 25.61
            A 15 15, 0, 0, 1, 15 30
            A 15 15, 0, 1, 1, 27.99 7.5
            L 15 15
          " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0); stroke: var(--main-color);" />
					</svg>
				</div>
			</span>
		</span>
	</div>
</template>

<script setup lang="ts">
import { defineComponent, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { Connection } from './sidebar';
import { mcpClientAdapter } from '@/views/connect/core';
import { isConnecting } from './connected';

defineComponent({ name: 'connected' });

const { t } = useI18n();
const client = computed(() => mcpClientAdapter.masterNode);


const displayServerName = computed(() => {
	const name = client.value.connectionResult.name;
	if (name.length <= 3) return name;

	// 处理中文混合名称
	const chineseMatch = name.match(/[\u4e00-\u9fa5]/g);
	if (chineseMatch && chineseMatch.length >= 2) {
		return chineseMatch.slice(0, 3).join('');
	}

	// 处理各种命名格式
	const words = name
		.replace(/([a-z])([A-Z])/g, '$1 $2')  // 驼峰分割
		.split(/[\s\-_]+/)  // 分割空格、连字符和下划线
		.filter(word => word.length > 0);

	if (words.length === 1 && words[0].length > 3) {
		return words[0].substring(0, 3).toUpperCase();
	}

	return words
		.map(word => word[0].toUpperCase())
		.slice(0, 3)
		.join('');
});


function toggleConnectionPanel() {
	Connection.showPanel = true;
}

</script>

<style>
.connected .status-circle {
	background-color: var(--el-color-success) !important;
}

.connected .connect-status {
	border: 1px solid var(--el-color-success) !important;
	color: var(--el-color-success) !important;
}

.disconnected-color {
	background-color: var(--main-color);
}

.status-circle {
	height: 12px;
	width: 12px;
	border-radius: 99%;
	background-color: var(--main-color);
	box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
}

.extra-connect-container {
	user-select: none;
}

.connected-status-container {
	user-select: none;
	display: flex;
	align-items: center;
	width: auto;
	padding: 8px 0;
	flex-direction: column;
	border-radius: 6px;
	transition: background-color 0.3s ease;
}

.connected-status-container .connect-status {
	display: flex;
	align-items: center;
	justify-content: space-between;
	margin-top: 10px;
	border-radius: .5em;
	padding: 5px 10px;
	width: 30px;
	border: 1px solid var(--main-color);
	color: var(--main-color);
}

.connected-status-container:hover {
	background-color: var(--sidebar-hover);
}


.status-string {
	color: var(--foreground);
	transition: var(--animation-3s);
	font-size: 13px;
	font-weight: 500;
	white-space: nowrap;
	margin-top: 4px;
}

.mcp-server-info {
	display: flex;
	flex-direction: column;
}

.mcp-server-info .name {
	font-size: 14px;
	font-weight: 600;
	width: 30px;
	display: flex;
	align-items: center;
	justify-content: center;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
	background-color: #f39a6d;
	padding: 5px 12px;
	border-radius: .5em;
	color: #1e1e1e;
}

.mcp-server-info .version {
	font-size: 12px;
	font-weight: 400;
}

.custom-loading .circular {
	margin-right: 6px;
	width: 18px;
	height: 18px;
	animation: loading-rotate 2s linear infinite;
}

.custom-loading .circular .path {
	animation: loading-dash 1.5s ease-in-out infinite;
	stroke-dasharray: 90, 150;
	stroke-dashoffset: 0;
	stroke-width: 2;
	stroke: var(--el-button-text-color);
	stroke-linecap: round;
}
</style>