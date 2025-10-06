<template>
	<div class="connection-option">
		<span>{{ t('connection-method') }}</span>
		<span style="width: 200px;">
			<el-select name="language-setting" class="language-setting" v-model="client.connectionArgs.connectionType">
				<el-option v-for="option in connectionSelectDataViewOption" :value="option.value" :label="option.label"
					:key="option.label"></el-option>
			</el-select>
		</span>
	</div>
</template>

<script setup lang="ts">
import { computed, defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';
import { connectionSelectDataViewOption, mcpClientAdapter } from './core';

defineComponent({ name: 'connection-method' });
const props = defineProps({
	index: {
		type: Number,
		required: true
	}
});

const client = computed(() => mcpClientAdapter.clients[props.index]);

const { t } = useI18n();

</script>

<style></style>