# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
npm run setup                 # Install dependencies and prepare OCR resources
```

### Development
```bash
npm run serve                 # Start all services in development mode (uses Turbo)
npm run build                 # Build all modules
npm run build:all             # Build all modules (alias)
npm run build:electron        # Build only Electron app
```

### Service Development
```bash
cd service
npm run serve                 # Start service with hot reload (nodemon + tsx)
npm run build                 # Compile TypeScript to dist/
npm run debug                 # Start with Node.js inspector
npm run typecheck             # Type checking without emit
```

### Renderer Development
```bash
cd renderer
npm run serve                 # Start Vite dev server
npm run build                 # Build for production
npm run serve:website         # Start in website mode
npm run type-check            # Vue TypeScript checking
```

### VSCode Extension
```bash
npm run vscode:prepublish     # Prepare for VSCode publishing (Rollup build)
npm run compile               # Compile TypeScript
npm run watch                 # Watch mode compilation
vsce package                  # Create VSIX package for distribution
vsce publish                  # Publish to VSCode Marketplace (requires auth)
```

### Quality Assurance
```bash
npm run lint                  # ESLint for TypeScript files
npm run pretest               # Run compile and lint
npm run test                  # Run tests
```

## Architecture Overview

### Multi-Module Structure
OpenMCP follows a **layered modular architecture** with three main deployment targets:

1. **VSCode Extension** (`src/extension.ts`) - IDE integration
2. **Service Layer** (`service/`) - Node.js backend handling MCP protocol
3. **Renderer Layer** (`renderer/`) - Vue.js frontend for UI

### Key Architectural Patterns

#### Message Bridge Communication
The system uses a **message bridge pattern** for cross-platform communication:
- **VSCode**: Uses `vscode.postMessage` API
- **Electron**: Uses IPC communication
- **Web**: Uses WebSocket connections
- **Node.js**: Uses EventEmitter for SDK mode

All communication flows through `MessageBridge` class in `renderer/src/api/message-bridge.ts`.

#### MCP Client Management
- **Connection Management**: `service/src/mcp/connect.service.ts` handles multiple MCP server connections
- **Client Pooling**: `clientMap` maintains active MCP client instances with UUID-based identification
- **Transport Abstraction**: Supports STDIO, SSE, and StreamableHTTP transports
- **Auto-reconnection**: `McpServerConnectMonitor` handles connection monitoring

#### Request/Response Flow
```
Frontend (Vue) → MessageBridge → Service Router → MCP Controllers → MCP SDK → External MCP Servers
```

### Important Service Patterns

#### Preprocessing Commands
`service/src/mcp/connect.service.ts` includes **automatic environment setup**:
- Python projects: Auto-runs `uv sync` and installs MCP CLI
- Node.js projects: Auto-runs `npm install` if node_modules missing
- Path resolution: Handles `~/` home directory expansion

#### OCR Integration
Built-in OCR using Tesseract.js:
- Images from MCP responses are automatically processed
- Base64 images saved to temp files and queued for OCR
- Results delivered via worker threads

### Frontend Architecture (Vue 3)

#### State Management
- **Panel System**: Tab-based interface in `renderer/src/components/main-panel/`
- **Reactive Connections**: MCP connection state managed reactively
- **Multi-language**: Vue i18n with support for 9 languages

#### Core Components
- **Chat Interface**: `main-panel/chat/` - LLM interaction with MCP tools
- **Tool Testing**: `main-panel/tool/` - Direct MCP tool invocation
- **Resource Browser**: `main-panel/resource/` - MCP resource exploration
- **Prompt Manager**: `main-panel/prompt/` - System prompt templates

### Build System

#### Turbo Monorepo
Uses Turbo for coordinated builds across modules:
- **Dependency ordering**: Renderer builds before Electron
- **Parallel execution**: Service and Renderer can build concurrently
- **Task caching**: Disabled for development iterations

#### Rollup Configuration
VSCode extension uses Rollup for optimal bundling:
- **ES modules**: Output as ESM format
- **External dependencies**: VSCode API marked as external
- **TypeScript**: Direct compilation without webpack

## Development Workflow

### Adding New MCP Features
1. **Service Layer**: Add controller in `service/src/mcp/`
2. **Router Registration**: Add to `ModuleControllers` in `service/src/common/router.ts`
3. **Frontend Integration**: Add API calls in `renderer/src/api/`
4. **UI Components**: Create components in `renderer/src/components/`

### Testing MCP Servers
1. **Connection**: Configure in connection panel (STDIO/SSE/HTTP)
2. **Validation**: Test tools/resources in respective panels
3. **Integration**: Verify LLM interaction in chat interface

### Packaging VSCode Extension

1. **Build Dependencies**: Run `npm run build` to build all modules
2. **Prepare Extension**: Run `npm run vscode:prepublish` to bundle extension code
3. **Create Package**: Run `vsce package` to generate `.vsix` file
4. **Install Locally**: Use `code --install-extension openmcp-x.x.x.vsix` for testing
5. **Publish**: Run `vsce publish` (requires marketplace publisher account)

### Platform-Specific Considerations

- **VSCode**: Uses webview API, limited to extension context
- **Electron**: Full desktop app capabilities, local service spawning
- **Web**: Requires external service, WebSocket limitations
- **SDK**: Embedded in other Node.js applications

## Important Files

### Configuration

- `turbo.json` - Monorepo build orchestration
- `rollup.config.js` - VSCode extension bundling
- `service/package.json` - Backend dependencies and scripts
- `renderer/package.json` - Frontend dependencies and scripts

### Core Architecture

- `src/extension.ts` - VSCode extension entry point
- `service/src/main.ts` - Service WebSocket server
- `service/src/common/router.ts` - Request routing system
- `renderer/src/api/message-bridge.ts` - Cross-platform communication
- `service/src/mcp/client.service.ts` - MCP client implementation

## Development Reminders

- **Service Startup**: 
  - 不要自行启动服务器,run serve只能由用户操作