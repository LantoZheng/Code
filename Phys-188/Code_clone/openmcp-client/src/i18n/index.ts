import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

const defaultBundle: Record<string, string> = {}

export function getDefaultLanguage() {
    const lang = vscode.env.language || 'en';
    if (lang === 'zh-cn') {
        return 'zh';
    }
    return lang;
}

export function initialiseI18n(context: vscode.ExtensionContext) {
    if (vscode.l10n.bundle === undefined) {
        // 获取用户的语言设置
        const userLanguage = vscode.env.language;
        
        // 尝试加载用户语言对应的语言包
        let bundlePath = context.asAbsolutePath(`l10n/bundle.l10n.${userLanguage}.json`);
        
        // 如果用户语言的语言包不存在，回退到英语
        if (!fs.existsSync(bundlePath)) {
            bundlePath = context.asAbsolutePath('l10n/bundle.l10n.en.json');
        }
        
        try {
            const bundle = JSON.parse(fs.readFileSync(bundlePath, { encoding: 'utf-8' })) as Record<string, string>;
            Object.assign(defaultBundle, bundle);
        } catch (error) {
            console.error('Failed to load i18n bundle:', error);
            // 如果加载失败，尝试加载英语包作为最后的回退
            try {
                const fallbackPath = context.asAbsolutePath('l10n/bundle.l10n.en.json');
                const fallbackBundle = JSON.parse(fs.readFileSync(fallbackPath, { encoding: 'utf-8' })) as Record<string, string>;
                Object.assign(defaultBundle, fallbackBundle);
            } catch (fallbackError) {
                console.error('Failed to load fallback i18n bundle:', fallbackError);
            }
        }
    }
}

export function t(message: string, ...args: string[]): string {
    if (vscode.l10n.bundle === undefined) {
        // 使用自定义的语言包
        let translateMessage = defaultBundle[message] || message;
        
        // 替换占位符 {0}, {1}, {2} 等
        for (let i = 0; i < args.length; i++) {
            translateMessage = translateMessage.replace(`{${i}}`, args[i]);
        }
        
        return translateMessage;
    } else {
        // 使用 VS Code 的 l10n API
        return vscode.l10n.t(message, ...args);
    }
}

/**
 * 获取当前使用的语言
 */
export function getCurrentLanguage(): string {
    return vscode.env.language;
}

/**
 * 获取已加载的翻译键列表，用于调试
 */
export function getAvailableKeys(): string[] {
    if (vscode.l10n.bundle === undefined) {
        return Object.keys(defaultBundle);
    }
    return [];
}

/**
 * 检查是否有特定键的翻译
 */
export function hasTranslation(key: string): boolean {
    if (vscode.l10n.bundle === undefined) {
        return key in defaultBundle;
    }
    // VS Code 的 l10n API 没有直接的方法检查，我们尝试翻译并比较
    const translated = vscode.l10n.t(key);
    return translated !== key;
}