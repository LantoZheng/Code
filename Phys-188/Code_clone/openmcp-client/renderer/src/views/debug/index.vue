<template>
	<div style="height: 100%;" id="debug-container">
		<Welcome v-show="!haveActiveTab"></Welcome>
		
		<!-- 如果存在激活标签页，则根据标签页进行渲染 -->
		<div v-show="haveActiveTab" v-if="panelLoaded" style="height: 100%;">
			<!-- vscode/trae 中，下面存在初始化问题 -->
			<component
                v-show="tab === tabs.content[tabs.activeIndex]"
                v-for="(tab, index) of tabs.content"
				:key="tab.id"
				:is="debugComponent[tab.componentIndex]"
                :tab-id="index"
			/>
		</div>
	</div>
</template>

<script setup lang="ts">
import { defineComponent, computed } from 'vue';
import Resource from '@/components/main-panel/resource/index.vue';
import Chat from '@/components/main-panel/chat/index.vue';
import Prompt from '@/components/main-panel/prompt/index.vue';
import Tool from '@/components/main-panel/tool/index.vue';

import Welcome from './welcome.vue';
import { tabs } from '@/components/main-panel/panel';
import { panelLoaded } from '@/hook/panel';

const debugComponent = [
	Resource, Prompt, Tool, Chat
]

defineComponent({ name: 'debug' });

const haveActiveTab = computed(() => {
	const activeTab = tabs.activeTab;
	if (activeTab && activeTab.componentIndex >= 0) {
		return true;
	}
	return false;
});

</script>

<style>
</style>