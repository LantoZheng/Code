import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';


suite('连接管理测试', () => {
  vscode.window.showInformationMessage('开始测试连接管理');

  let inputBoxStub: sinon.SinonStub;
  let quickPickStub: sinon.SinonStub;

  setup(async () => {
    // mock选择连接类型
    quickPickStub = sinon.stub(vscode.window, 'showQuickPick');
    // mock 连接地址和认证输入框
    inputBoxStub = sinon.stub(vscode.window, 'showInputBox');
    await vscode.commands.executeCommand('workbench.view.extension.openmcp-sidebar');
    deleteAllConnection();

  });

  teardown(() => {
    sinon.restore();
  });

  const deleteAllConnection = async () => {
    //在开始之前删除所有链接
  }
  test('新建STDIO连接', async function () {
    this.timeout(15000);
    quickPickStub.onFirstCall().resolves('STDIO');
    inputBoxStub.onFirstCall().resolves('echo'); // command
    inputBoxStub.onSecondCall().resolves(''); // cwd

    await vscode.commands.executeCommand('openmcp.sidebar.installed-connection.addConnection');
  
  });

  test('新建SSE连接', async function () {
    quickPickStub.onFirstCall().resolves('SSE');
    inputBoxStub.onFirstCall().resolves('http://localhost/sse'); // command
    inputBoxStub.onSecondCall().resolves(''); // cwd

    await vscode.commands.executeCommand('openmcp.sidebar.installed-connection.addConnection');


  });

  test('新建StreamableHttp连接', async function () {
    quickPickStub.onFirstCall().resolves('STREAMABLE_HTTP');
    inputBoxStub.onFirstCall().resolves('http://localhost/mcp'); // command
    inputBoxStub.onSecondCall().resolves(''); // cwd
    await vscode.commands.executeCommand('openmcp.sidebar.installed-connection.addConnection');

  });

  test('等待以便观察窗口', async function () {
    this.timeout(15000);
    await new Promise(resolve => setTimeout(resolve, 10000));
  });


});