import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
	plugins: [
		vue(),
		vueDevTools(),
	],
	resolve: {
		alias: {
			'@': fileURLToPath(new URL('./src', import.meta.url))
		},
	},
	base: mode === 'website' ? '/mcp/' : '/',
	build: {
		cssCodeSplit: false, // 禁用 CSS 代码分割
		rollupOptions: {
			output: {
				inlineDynamicImports: true, // 将动态导入的内容内联
				manualChunks: undefined, // 禁用手动分块
			},
		},
	},
}))
