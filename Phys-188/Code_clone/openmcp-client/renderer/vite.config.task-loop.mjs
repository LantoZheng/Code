import { defineConfig, normalizePath } from 'vite';
import { resolve } from 'path';
import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
    define: {
        'window': {
            'nodejs': true,
            'navigator': {
                'userAgent': 2
            },
            'performance': {
                'now': () => performance.now()
            },
            'Date': {
                'now': () => Date.now()
            }
        },
    },
    plugins: [
        viteStaticCopy({
            targets: [
                {
                    src: normalizePath(resolve(__dirname, '../resources/openmcp-sdk-release/*')),
                    dest: normalizePath(resolve(__dirname, '../openmcp-sdk'))
                }
            ]
        })
    ],
    build: {
        target: 'node18',
        lib: {
            entry: resolve(__dirname, '..', 'renderer/src/components/main-panel/chat/core/task-loop.ts'),
            name: 'TaskLoop',
            fileName: (format) => `task-loop.js`,
            formats: ['es']
        },
        outDir: resolve(__dirname, '..', 'openmcp-sdk'),
        emptyOutDir: false,
        rollupOptions: {
            external: [
                'vue',
                'chalk',
                'element-plus',
            ],
            output: {
                globals: {
                    vue: 'vue',
                    chalk: 'chalk',
                    'element-plus': './tools.js'
                },
                esModule: true
            }
        },
        minify: false,
        sourcemap: false
    },
    resolve: {
        alias: {
            '@': resolve(__dirname, '..', 'renderer/src'),
        }
    }
});