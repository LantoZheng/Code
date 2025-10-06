import { reactive } from 'vue';
import { createTab, tabs } from '@/components/main-panel/panel';
import type { ToolStorage } from '@/components/main-panel/tool/tools';
import type { ToolCall } from '@/components/main-panel/chat/chat-box/chat';

import I18n from '@/i18n';
const { t } = I18n.global;

export const llms = reactive<BasicLlmDescription[]>([]);

export const llmManager = reactive({
	currentModelIndex: 0,
});

export interface BasicLlmDescription {
	id: string,
	name: string,
	baseUrl: string,
	models: string[],
	isOpenAICompatible: boolean,
	description: string,
	website: string,
	userToken: string,
	userModel: string,
	isDynamic?: boolean,
	modelsEndpoint?: string,
	supportsPricing?: boolean,
	[key: string]: any
}

export function createTest(call: ToolCall) {
	const tab = createTab('tool', 0);
	tab.componentIndex = 2;
	tab.icon = 'icon-tool';
	tab.name = t("tools");
	
	const storage: ToolStorage = {
		activeNames: [0],
		currentToolName: call.function!.name!,
		formData: JSON.parse(call.function!.arguments!)
	};

	tab.storage = storage;
	tabs.content.push(tab);
	tabs.activeIndex = tabs.content.length - 1;
}