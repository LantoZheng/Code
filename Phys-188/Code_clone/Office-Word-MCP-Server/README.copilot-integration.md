## Office-Word-MCP-Server — VS Code / OpenMCP 集成（快速指南）

本文件描述如何：
- 构建并安装 OpenMCP VS Code 插件（作为 MCP 客户端桥接）
- 生成 VS Code / OpenMCP 的辅助配置文件（不会自动改写用户设置）
- 启动 `word-document-server`（streamable-http）并做端到端验证

安全原则
- 所有对用户配置的修改都在写入前进行备份。
- 本说明提供手动及自动两种路径；自动写入 `settings.json` 需用户显式同意。

目录
- 插件源码（示例）: `/Users/zhengxiaoyang/Code/openmcp-client`
- 本仓库脚本: `/Users/zhengxiaoyang/Code/Office-Word-MCP-Server/setup_mcp.py`

一、构建并安装 OpenMCP 插件（生成 VSIX）

1. 克隆（已完成示例）

  git clone https://github.com/LSTM-Kirigaya/openmcp-client.git

2. 在 `openmcp-client` 目录安装依赖并构建插件（项目使用 yarn）

```bash
cd /Users/zhengxiaoyang/Code/openmcp-client
npm ci
# 如果没有 yarn： npm install -g yarn
npm run build:plugin
# 成功后会在仓库根生成 openmcp-<version>.vsix
```

3. 用 VS Code 的 CLI 安装 VSIX（macOS 示例）

```bash
# 如果 code 不在 PATH，可用完整路径：
/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code --install-extension \
  /Users/zhengxiaoyang/Code/openmcp-client/openmcp-0.1.13.vsix --force

# 验证已安装：
/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code --list-extensions --show-versions | grep openmcp
```

二、生成 VS Code / OpenMCP 辅助文件（不会自动修改 settings.json）

本仓库的 `setup_mcp.py` 增加了一个安全 helper：`generate_vscode_copilot_files(...)`，会创建两份文件：

- `vscode_mcp.json` — 原始 MCP 配置文件（可被 OpenMCP 或 mcp-use 读取）
- `vscode_settings_snippet.txt` — 手动导入到 VS Code settings 的说明片段

交互式运行（示例）：

```bash
cd /Users/zhengxiaoyang/Code/Office-Word-MCP-Server
python3 setup_mcp.py
# 按提示选择 transport（stdio / streamable-http / sse）并选择生成 VS Code helper
```

或者直接使用已生成的文件（示例路径）：

- `/Users/zhengxiaoyang/Code/Office-Word-MCP-Server/vscode_mcp.json`
- `/Users/zhengxiaoyang/Code/Office-Word-MCP-Server/vscode_settings_snippet.txt`

三、（可选）把配置写入 VS Code 用户设置（已备份）

注意：自动写入会先备份 `settings.json`，如不信任请手动合并 `vscode_settings_snippet.txt` 中的片段。

示例（macOS 用户设置文件位置）

`~/Library/Application Support/Code/User/settings.json`

备份示例命令（脚本化）：

```bash
cp "${HOME}/Library/Application Support/Code/User/settings.json" \
  "${HOME}/Library/Application Support/Code/User/settings.json.openmcp_backup_$(date -u +%Y%m%dT%H%M%S)"
```

示例合并片段（仅示范，建议手动编辑）：

```json
"openmcp.client": {
  "mcpConfig": { /* paste contents of vscode_mcp.json here */ }
}
```

四、启动 `word-document-server`（示例：streamable-http）

建议把 server 以 streamable-http 启动以便 OpenMCP 或本地客户端通过 HTTP/SSE 连接。

```bash
cd /Users/zhengxiaoyang/Code/Office-Word-MCP-Server
export MCP_TRANSPORT=streamable-http
export MCP_HOST=127.0.0.1
export MCP_PORT=8931
export MCP_PATH=/mcp
# 使用本地仓库脚本启动
/opt/homebrew/Caskroom/miniconda/base/bin/python word_mcp_server.py &>/tmp/word_mcp_server.log &
# 记录 PID 并查看日志
echo $!  # 子进程 PID
tail -f /tmp/word_mcp_server.log
```

五、端到端验证（使用 mcp_use 客户端）

下面的示例使用与 server 相同的 Python 环境（如果你用 conda，请用 conda run 前缀）。此示例会：
- 连接到 `http://127.0.0.1:8931/mcp`
- 调用 `list_tools` 列出服务器提供的工具
- 调用 `create_document` 与 `get_document_info` 做一次创建验证

安装 mcp_use（示例，使用系统/conda 的 Python）：

```bash
conda run -p /opt/homebrew/Caskroom/miniconda/base --no-capture-output python -m pip install --user mcp_use
```

调用示例（可以直接粘到终端执行）：

```bash
conda run -p /opt/homebrew/Caskroom/miniconda/base --no-capture-output python - <<'PY'
import asyncio
from mcp_use import MCPClient

async def main():
    config = {"mcpServers": {"word": {"url": "http://127.0.0.1:8931/mcp"}}}
    client = MCPClient.from_dict(config)
    await client.create_all_sessions()
    session = client.get_session('word')
    tools = await session.list_tools()
    print('Got', len(tools), 'tools')
    # 调用 create_document 示例
    res = await session.call_tool('create_document', {'filename':'/tmp/test_mcp_created.docx','title':'MCP Test','author':'You'})
    print('create_document ->', res.content[0].text if res.content else res)
    await client.close_all_sessions()

asyncio.run(main())
PY
```

六、停止 & 清理

停止后台 server（示例）：

```bash
# 假设你在启动时通过 $! 得到 PID
kill <PID>
# 或通过查找并杀掉 python 进程
pkill -f word_mcp_server.py
```

七、故障排查要点
- 如果 `code` 命令未找到：在 VS Code 中打开 Command Palette，运行 `Shell Command: Install 'code' command in PATH` 或直接使用应用包内的 `bin/code` 路径。
- 如果构建提示 `yarn`：用 `npm install -g yarn` 安装，或用 `yarn` 代替 `npm` 执行脚本。
- 若 Python 包安装出现 conda 基环境冲突：使用 `conda run -p <env> --no-capture-output python -m pip install --user ...` 来避免改写 conda 基环境核心包。
- 若 OpenMCP 扩展有自定义设置位置：优先使用扩展的 UI（OpenMCP 侧栏）来导入 `vscode_mcp.json`，而不是直接编辑 settings.json。
- 若 `microsoft/markitdown` 服务器在启动日志中报错 `unrecognized arguments: markitdown-mcp==0.0.1a4`：
  更新你的 MCP 配置，使其使用 `uvx --from markitdown-mcp==0.0.1a4 markitdown-mcp --stdio`（参见本仓库最新的 `mcp-config.json` / `vscode_mcp.json` 示例），不要把版本号当成 CLI 参数传给 `markitdown-mcp` 本身。
- 若 `WolframAlphaServer` 报缺少凭据：先在终端导出 `WOLFRAM_API_KEY=<你的 Wolfram|Alpha AppID>`，或直接在配置文件中把占位符 `<insert-your-appid>` 换成真实 AppID。本仓库内置了 `wolframalpha_mcp_server.py`（基于 FastMCP 与 Wolfram|Alpha HTTP API），直接运行 `python /path/to/Office-Word-MCP-Server/wolframalpha_mcp_server.py` 即可启动；若依赖缺失，请在同一 Python 环境中安装 `fastmcp` 与 `httpx`。

八、可选的自动化改进（建议）
- 把 `setup_mcp.py` 中的 `generate_vscode_copilot_files()` 与一个 `--apply-to-vscode` 选项结合，但必须在写入前明确备份与用户确认。
- 将 OpenMCP VSIX 与本仓库建立一个 `tools/` 子目录并编写一个 `make` 或 `scripts/install_openmcp.sh` 来自动化构建与安装步骤（可选）。

九、联系与后续
如需我代你：
- 1) 把 VSIX 安装到你的 VS Code（我已成功在当前机器上安装），或
- 2) 在 OpenMCP UI 中帮你加载并演示一次工具调用（我可继续远端执行或给出屏幕操作步骤）。

—— 结束 ——
