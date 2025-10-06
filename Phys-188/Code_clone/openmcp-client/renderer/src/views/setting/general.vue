<template>
	<div class="setting-section">
		<h2>{{ t('general-setting') }}</h2>
		<div class="setting-option">
			<span>
				<span class="iconfont icon-i18n"></span>
				<span class="option-title">{{ t('language-setting') }}</span>
			</span>
			<div style="width: 100px;">
				<el-select name="language-setting" class="language-setting" v-model="locale" @change="onlanguagechange">
					<el-option v-for="option in languageSetting.options" :value="option.value" :label="option.text"
						:key="option.value">
					</el-option>
				</el-select>
			</div>
		</div>

		<div class="setting-option">
			<span>
				<span class="iconfont icon-timeout"></span>
				<span class="option-title">{{ t('mcp-server-timeout') }} (sec)</span>
			</span>
			<div style="width: 200px;">
				<el-slider
					v-model="mcpSetting.timeout"
					:min="10" :max="10000" :step="1"
					@change="safeSaveSetting" />
			</div>
		</div>

		<div class="setting-option">
			<span>
				<span class="iconfont icon-proxy"></span>
				<span class="option-title">{{ t('proxy-server') }}</span>
			</span>
			<div style="width: 200px;">
				<el-input
					v-model="mcpSetting.proxyServer"
					:placeholder="'http://localhost:7890'"
					@input="safeSaveSetting"
				/>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { languageSetting } from './language';
import { useI18n } from 'vue-i18n';
import { mcpSetting } from '@/hook/mcp';
import { debounce } from 'lodash';
import { saveSetting } from '@/hook/setting';

defineComponent({ name: 'appearance' });

const { t, locale } = useI18n();

function onlanguagechange() {	
	saveSetting();
}

const safeSaveSetting = debounce(() => {
	saveSetting();
}, 10);

onMounted(() => {
    locale.value = mcpSetting.language;
});

</script>

<style></style>