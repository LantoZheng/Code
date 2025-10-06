<div align="center">

<img src="./icons/openmcp-sdk.svg" height="200px"/>

<h3>openmcp-sdk: Deployment Framework for OpenMCP</h3>
<h4>Lightning-fast deployment of your agent from lab to production</h4>

<a href="https://openmcp.kirigaya.cn/sdk-tutorial/" target="_blank" style="display: inline-block; padding: 8px 16px; background-color: #7D3FF8; color: white; border-radius: .5em; text-decoration: none;">🫱 OpenMCP SDK 官方文档</a>


<a href="https://qm.qq.com/cgi-bin/qm/qr?k=C6ZUTZvfqWoI12lWe7L93cWa1hUsuVT0&jump_from=webapi&authKey=McW6B1ogTPjPDrCyGttS890tMZGQ1KB3QLuG4aqVNRaYp4vlTSgf2c6dMcNjMuBD" target="_blank" style="display: inline-block; padding: 8px 16px; background-color: #CB81DA; color: white; border-radius: .5em; text-decoration: none;">QQ Discussion Group</a><a href="https://discord.gg/af5cfB9a" target="_blank" style="display: inline-block; padding: 8px 16px; background-color: rgb(84, 176, 84); color: white; border-radius: .5em; text-decoration: none; margin-left: 5px;">Discord Channel</a>

</div>

## Installation

```bash
npm install openmcp-sdk
```

> Currently, openmcp-sdk only supports ESM-style imports.

## Usage

Filename: `main.ts`

```typescript
import { OmAgent } from 'openmcp-sdk/service/sdk';

// create Agent
const agent = new OmAgent();
    
// Load configuration, which can be automatically generated after debugging with openmcp client
agent.loadMcpConfig('./mcpconfig.json');

// Read the debugged prompt
const prompt = await agent.getPrompt('hacknews', { topn: '5' });    

// Execute the task
const res = await agent.ainvoke({ messages: prompt });

console.log('⚙️ Agent Response', res);
```

`mcpconfig.json` can be generated from [openmcp client](https://github.com/LSTM-Kirigaya/openmcp-client) directly, you don't have to write it by yourself. Here is the example:

```json
{
    "version": "1.0.0",
    "namespace": "openmcp",
    "mcpServers": {
        "my-browser": {
            "command": "mcp",
            "args": [
                "run",
                "~/projects/openmcp-tutorial/crawl4ai-mcp/main.py"
            ],
            "description": "A MCP for long-term memory support",
            "prompts": [
                "hacknews"
            ]
        }
    },
    "defaultLLM": {
        "baseURL": "https://api.deepseek.com",
        "apiToken": "sk-xxxxxxxxxxxxxx",
        "model": "deepseek-chat"
    }
}
```

Run your agent and get example output:

```
[2025/6/20 20:47:31] 🚀 [crawl4ai-mcp] 1.9.1 connected
[2025/6/20 20:47:35] 🤖 Agent wants to use these tools get_web_markdown
[2025/6/20 20:47:35] 🔧 using tool get_web_markdown
[2025/6/20 20:47:39] ✓  use tools success
[2025/6/20 20:47:46] 🤖 Agent wants to use these tools get_web_markdown, get_web_markdown, get_web_markdown
[2025/6/20 20:47:46] 🔧 using tool get_web_markdown
[2025/6/20 20:47:48] ✓  use tools success
[2025/6/20 20:47:48] 🔧 using tool get_web_markdown
[2025/6/20 20:47:54] ✓  use tools success
[2025/6/20 20:47:54] 🔧 using tool get_web_markdown
[2025/6/20 20:47:57] ✓  use tools success

⚙️ Agent Response
⌨️ Today's Tech Article Roundup

📌 How to Detect or Observe Passing Gravitational Waves?
Summary: This article explores the physics of gravitational waves, explaining their effects on space-time and how humans might perceive or observe this cosmic phenomenon.
Author: ynoxinul
Posted: 2 hours ago
Link: https://physics.stackexchange.com/questions/338912/how-would-a-passing-gravitational-wave-look-or-feel

📌 Learn Makefile Tutorial
Summary: A comprehensive Makefile tutorial for beginners and advanced users, covering basic syntax, variables, automatic rules, and advanced features to help developers manage project builds efficiently.
Author: dsego
Posted: 4 hours ago
Link: https://makefiletutorial.com/

📌 Hurl: Run and Test HTTP Requests in Plain Text
Summary: Hurl is a command-line tool that allows defining and executing HTTP requests in plain text format, ideal for data fetching and HTTP session testing. It supports chained requests, value capture, and response queries, making it perfect for testing REST, SOAP, and GraphQL APIs.
Author: flykespice
Posted: 8 hours ago
Link: https://github.com/Orange-OpenSource/hurl
```

For more details, see the official documentation: [https://openmcp.kirigaya.cn/sdk-tutorial/](https://openmcp.kirigaya.cn/sdk-tutorial/)  

Star our project: [https://github.com/LSTM-Kirigaya/openmcp-client](https://github.com/LSTM-Kirigaya/openmcp-client)  
