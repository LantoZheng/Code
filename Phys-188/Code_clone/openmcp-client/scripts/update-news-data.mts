import { readFileSync, writeFileSync } from 'fs';
import fetch from 'node-fetch';
import path from 'path';
import { OpenAI } from 'openai';
import chalk from 'chalk';

const client = new OpenAI({
	baseURL: 'https://api.deepseek.com',
	apiKey: process.env.DEEPSEEK_API_TOKEN,
});

async function fetchContributorsFromRepo(owner: string, repo: string) {
    let page = 1;
    const per_page = 100;
    let contributors: any[] = [];

    while (true) {
        const res = await fetch(
            `https://api.github.com/repos/${owner}/${repo}/contributors?per_page=${per_page}&page=${page}`,
            {
                headers: {
                    'User-Agent': 'openmcp-client-script'
                }
            }
        );
        if (!res.ok) {
            throw new Error(`GitHub API error: ${res.status} ${res.statusText}`);
        }
        const data = await res.json();
        if (data.length === 0) break;
        contributors = contributors.concat(data);
        page++;
    }

    return contributors;
}

async function fetchAndMergeContributors() {
    const repos = [
        { owner: 'LSTM-Kirigaya', repo: 'openmcp-client' },
        { owner: 'LSTM-Kirigaya', repo: 'openmcp-document' }
    ];

    const allContributors: Record<string, { username: string, avatarUrl: string, homeUrl: string, contributions: number }> = {};

    for (const { owner, repo } of repos) {
        const contributors = await fetchContributorsFromRepo(owner, repo);
        for (const c of contributors) {
            const username = c.login;
            if (!allContributors[username]) {
                allContributors[username] = {
                    username,
                    avatarUrl: c.avatar_url,
                    homeUrl: c.html_url,
                    contributions: c.contributions
                };
            } else {
                allContributors[username].contributions += c.contributions;
            }
        }
    }

    // 按贡献次数排序
    const result = Object.values(allContributors)
        .sort((a, b) => b.contributions - a.contributions)
        .map(({ contributions, ...rest }) => rest); // 去掉contributions字段

    return result;
}

const PRJ_PATH = path.join(path.dirname(import.meta.dirname));

async function getVersionAndContent() {
    const changelog = readFileSync( path.join(PRJ_PATH, 'CHANGELOG.md'), { encoding: 'utf-8' });
    const newContent = changelog.split('## [main]')[1];
    const version = newContent.split('\n')[0].trim();

    // 提取 main 版本下的 markdown 列表内容
    const contentLines = newContent.split('\n').slice(1);
    const content = contentLines
        .filter(line => line.trim().startsWith('- ') || line.trim().startsWith('* '))
        .map(line => line.replace(/^[-*]\s*/, '').trim())
        .join('\n');

    // 让大模型翻译并输出 json
    const prompt = `
Translate the following markdown list to English and return a JSON array of strings (do not include any markdown or extra text, only valid JSON array):

${content}
`;

    const completion = await client.chat.completions.create({
        model: 'deepseek-chat',
        messages: [
            { role: 'system', content: 'You are a helpful assistant for translation and JSON formatting.' },
            { role: 'user', content: prompt }
        ],
        temperature: 0.2,
        max_tokens: 1024
    });

    // 解析大模型返回的 JSON
    let changelogs: string[] = [];
    try {
		const choices = completion.choices;
		if (!choices || choices.length === 0 || !choices[0].message || !choices[0].message.content) {
			throw new Error('Invalid response from LLM');
		}
        const text = choices[0].message.content.trim();
		// 按行过滤：只保留非 ``` 开头的行
		const clearText = text.split('\n').filter(line => !line.startsWith('```')).join('\n')
        changelogs = JSON.parse(clearText);
    } catch (e) {
        throw new Error('Failed to parse LLM output as JSON: ' + e);
    }

    return { version, changelogs };
}

console.log(chalk.green('Starting to update contributors...'));
const contributors = await fetchAndMergeContributors();
const { version, changelogs } = await getVersionAndContent();
const newsData = {
	version,
	changelogs,
	contributors
};
const newsDataPath = path.join(PRJ_PATH, 'news', 'src', 'data.json');
writeFileSync(newsDataPath, JSON.stringify(newsData, null, 2), { encoding: 'utf-8' });
console.log('News data updated successfully:', newsDataPath);

import { execSync } from 'child_process';

// ...前面的代码...

// 写入 news/src/data.json
writeFileSync(newsDataPath, JSON.stringify(newsData, null, 2), { encoding: 'utf-8' });
console.log('News data updated successfully:', newsDataPath);

// 1. 进入 news 目录并编译
const newsDir = path.join(PRJ_PATH, 'news');
console.log('Building news SPA...');
execSync('npm run build', { cwd: newsDir, stdio: 'inherit' });

// 2. 拷贝编译产物到 resources/changelog
const buildOutputDir = path.join(newsDir, 'dist');
const targetDir = path.join(PRJ_PATH, 'resources', 'changelog');

// 简单递归复制函数
import { existsSync, mkdirSync, readdirSync, statSync, copyFileSync } from 'fs';

function copyDir(src: string, dest: string) {
    if (!existsSync(dest)) mkdirSync(dest, { recursive: true });
    for (const file of readdirSync(src)) {
        const srcFile = path.join(src, file);
        const destFile = path.join(dest, file);
		if (file.endsWith('.css')) {
			continue;
		}
        if (statSync(srcFile).isDirectory()) {
            copyDir(srcFile, destFile);
        } else {
            copyFileSync(srcFile, destFile);
        }
    }
}

copyDir(buildOutputDir, targetDir);
console.log('Build output copied to:', targetDir);