// esbuild.config.js
const { build } = require('esbuild');

build({
  entryPoints: ['src/extension.ts'],
  bundle: true,
  platform: 'node',
  format: 'cjs',
  outfile: 'dist/extension.cjs.js',
  sourcemap: true,
  external: ['vscode'], 
  target: ['node22'],   
  loader: {
    '.json': 'json'
  },
  define: { 'import.meta.url': '_importMetaUrl' },
  banner: {
    js: "const _importMetaUrl=require('url').pathToFileURL(__filename)",
  },
}).catch(() => process.exit(1));