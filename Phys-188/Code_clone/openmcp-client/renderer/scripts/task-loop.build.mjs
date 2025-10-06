import * as fs from 'node:fs';

const targetFile = './openmcp-sdk/task-loop.js';

if (fs.existsSync(targetFile)) {
    let content = fs.readFileSync(targetFile, 'utf-8');
    
    // Replace element-plus with ./tools.js
    content = content.replace(/'element-plus'/g, "'./tools.mjs'");
    content = content.replace(/"element-plus"/g, "\"./tools.mjs\"");

    // content = content.replace(/const chalk = require\("chalk"\);/g, 'const chalk = require("chalk").default;');
    
    // Replace define_window_default$number.performance with performance
    content = content.replace(/define_window_default\$\d+\.performance/g, 'performance');
    
    fs.writeFileSync(targetFile, content);
    console.log('\x1b[32m✓ File processing completed\x1b[0m');  // Green color
} else {
    console.log('Target file does not exist:', targetFile);
}