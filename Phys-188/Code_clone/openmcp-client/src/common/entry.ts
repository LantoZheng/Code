import * as vscode from 'vscode';
import { registerCommands, registerTreeDataProviders } from './index.js';
import { HelpProvider } from '../sidebar/help.controller.js';
import { McpWorkspaceConnectProvider } from '../sidebar/workspace.controller.js';
import { McpInstalledConnectProvider } from '../sidebar/installed.controller.js';
import { WebviewController } from '../webview/webview.controller.js';
import { HookController } from '../hook/hook.controller.js';

export const InstallModules = [
    McpWorkspaceConnectProvider,
    McpInstalledConnectProvider,
    HelpProvider,
    WebviewController,
    HookController
];

const registerSingles = new Map<string, any>();

export function launch(context: vscode.ExtensionContext) {

    for (const [providerId, value] of registerTreeDataProviders) {
        const provider = new value.providerConstructor(context);
        
        registerSingles.set(providerId, provider);
        
        context.subscriptions.push(
            vscode.window.registerTreeDataProvider(providerId, provider)
        );
    }

    
    for (const [command, value] of registerCommands) {
        const namespace = value.target.__openmcp_namespace;
        const targetCommand = namespace ? `${namespace}.${command}` : command;

        const target = registerSingles.has(namespace) ? registerSingles.get(namespace) : value.target;
        
        context.subscriptions.push(vscode.commands.registerCommand(targetCommand, (...args: any[]) => {
            target[value.propertyKey](context,...args);
        }));
    }

}