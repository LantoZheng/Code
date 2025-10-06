import * as assert from 'assert';
import * as vscode from 'vscode';

suite('测试基础插件激活和命令注册', () => {
	vscode.window.showInformationMessage('开始测试基础插件激活和命令注册');
	setup(async () => {
		await vscode.commands.executeCommand('workbench.view.extension.openmcp-sidebar');
	});
	test('测试的测试', () => {
		assert.strictEqual([1, 2, 3].indexOf(5), -1);
		assert.strictEqual([1, 2, 3].indexOf(0), -1);
	});

	test('插件存在测试', async () => {
		const ext = vscode.extensions.getExtension('kirigaya.openmcp');
		assert.ok(ext, '插件未找到');
	});

	test('插件激活测试', async () => {
		const ext = vscode.extensions.getExtension('kirigaya.openmcp');
		await ext?.activate();
		assert.ok(ext?.isActive, '插件未激活');
	});

	test('命令 openmcp.showOpenMCP 注册测试', async () => {
		const commands = await vscode.commands.getCommands(true);
		assert.ok(commands.includes('openmcp.showOpenMCP'), '命令未注册');
	});

	// 
});