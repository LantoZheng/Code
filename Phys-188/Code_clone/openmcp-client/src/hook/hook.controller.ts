import { RegisterCommand } from "../common/index.js";
import * as vscode from 'vscode';
import * as path from 'path';
import Tesseract from 'tesseract.js';
import { revealOpenMcpNewsWebviewPanel } from "../webview/webview.service.js";

export class HookController {

    @RegisterCommand('openmcp.hook.test-ocr')
    async testOcr(context: vscode.ExtensionContext) {
        try {
            const testImage = path.join(context.extensionPath, 'icons/openmcp.resource.png');

            console.log('test ocr begin');

            const cachePath = context.extensionPath;
            const workerPath = path.join(cachePath, 'resources', 'ocr', 'worker.js');
            const corePath = path.join(cachePath, 'resources', 'ocr');
            const langPath = path.join(cachePath,'resources', 'ocr');

            console.log('workerPath', workerPath);
            console.log('corePath', corePath);
            console.log('cachePath', context.extensionPath);
            
            const { data: { text } } = await Tesseract.recognize(
                testImage,
                'eng+chi_sim',
                {
                    logger: (m) => console.log(m),
                    langPath,
                    gzip: false,
                    workerPath,
                    corePath 
                }
            );
    
            console.log('ocr result: ' + text);
        } catch (error) {
            vscode.window.showErrorMessage(error as string);
        }
    }

    @RegisterCommand('openmcp.hook.test-news')
    async testNews(context: vscode.ExtensionContext) {
        revealOpenMcpNewsWebviewPanel(context);
    }
}