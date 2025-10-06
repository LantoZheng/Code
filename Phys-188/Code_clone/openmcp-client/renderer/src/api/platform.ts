export type OpenMcpSupportPlatform = 'web' | 'vscode' | 'electron' | 'nodejs';

export const acquireVsCodeApi = (window as any)['acquireVsCodeApi'];
export const electronApi = (window as any)['electronApi'];
export const isNodejs = (window as any)['nodejs'];

export function getPlatform(): OpenMcpSupportPlatform {
    if (acquireVsCodeApi) {
        return 'vscode';
    } else if (electronApi) {
        return 'electron';
    } else if (isNodejs) {
        return 'nodejs';
    } else {
        return 'web';
    }
}