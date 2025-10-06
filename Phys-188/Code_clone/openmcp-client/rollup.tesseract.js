import path from 'path';
import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import { babel } from '@rollup/plugin-babel';
import json from '@rollup/plugin-json'; // ✅ 新增
import copy from 'rollup-plugin-copy';

export default {
  input: './node_modules/tesseract.js/src/worker-script/node/index.js',
  output: {
    file: path.resolve(__dirname, '..', 'resources', 'ocr', 'worker.js'),
    format: 'cjs',
    exports: 'auto'
  },
  plugins: [
    json(), // ✅ 插入 JSON 插件
    nodeResolve({
      browser: false,
      preferBuiltins: true
    }),
    commonjs(),
    babel({
      babelHelpers: 'bundled',
      exclude: 'node_modules/**',
      presets: ['@babel/preset-env']
    }),
    copy({
      targets: [
        {
          src: path.resolve(__dirname, '..', 'node_modules', 'tesseract.js-core', 'tesseract*'),
          dest: path.resolve(__dirname, '..', 'resources', 'ocr')
        }
      ]
    })
  ],
  external: ['bufferutil', 'utf-8-validate']
};
