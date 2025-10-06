<template>
	<div class="connection-log">
		<div class="header">
			<span>{{ t('log') }}</span>
			<span class="iconfont icon-delete" @click="clearLogs"></span>
		</div>
		<el-scrollbar height="90%">
			<div class="output-content">
				<el-collapse :expand-icon-position="'left'">
					<el-collapse-item v-for="(log, index) in logString" :name="index" :class="['item', log.type]">
						<template #title>
							<div class="tool-calls">
								<div class="tool-call-header">
									<span>{{ log.title }}</span>
								</div>
							</div>
						</template>

						<div class="logger-inner">
							{{ log.message || '' }}
						</div>
					</el-collapse-item>
				</el-collapse>
			</div>
		</el-scrollbar>
	</div>
</template>

<script setup lang="ts">
import { computed, defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';
import { mcpClientAdapter } from './core';

defineComponent({ name: 'connection-log' });
const props = defineProps({
	index: {
		type: Number,
		required: true
	}
});

const logString = computed(() => {
	return mcpClientAdapter.clients[props.index].connectionResult.logString;
});

const { t } = useI18n();

function clearLogs() {
    mcpClientAdapter.clients[props.index].connectionResult.logString = [];
}
</script>

<style>

.connection-log {
	height: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    background-color: var(--el-bg-color);
    border-radius: 4px;
    margin-bottom: 16px;
}

.connection-log .el-scrollbar__view {
	height: 100%;
}

.connection-log .output-content {
	border-radius: .5em;
	padding: 12px 16px;
	min-height: 300px;
	height: fit-content;
	font-family: var(--code-font-family);
	white-space: pre-wrap;
	word-break: break-all;
	user-select: text;
	cursor: text;
	font-size: 14px;
	line-height: 1.6;
	background-color: rgba(var(--sidebar), 0.3);
	height: 95%;
}

.output-content .item {
	margin-bottom: 12px;
	padding: 0px 9px;
	border-radius: .5em;
}

.output-content .info {
	background-color: rgba(103, 194, 58, 0.5);
}

.output-content .error {
	background-color: rgba(245, 108, 108, 0.5);
}

.output-content .warning {
	background-color: rgba(230, 162, 60, 0.5);
}

.log-icon {
	display: inline-block;
	width: 8px;
	height: 8px;
	border-radius: 50%;
	margin-right: 8px;
	vertical-align: middle;
}

.log-icon.info {
	background-color: rgba(103, 194, 58, 0.3);
}

.log-icon.error {
	background-color: rgba(245, 108, 108, 0.3);
}

.log-icon.warning {
	background-color: rgba(230, 162, 60, 0.3);
}

.log-message {
	display: inline-block;
	vertical-align: middle;
}

.output-content .el-collapse-item__header,
.output-content .el-collapse-item__wrap {
	background-color: unset !important;
	border-bottom: unset !important;
}

.output-content .el-collapse-item__content {
	padding-bottom: unset;
}

.logger-inner {
	padding: 10px;
}

.header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
}

.header .icon-delete {
	margin-left: 10px;
	cursor: pointer;
}

.header .icon-delete:hover {
	color: var(--el-color-error);
}

</style>