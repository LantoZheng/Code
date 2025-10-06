import { Prism } from './prism';
import I18n from '@/i18n';

const { t } = I18n.global;

// 定义 escapeHtml 函数
function escapeHtml(unsafe: string) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

interface HighlightOption {
    needTools?: boolean
}

// 导出默认的 highlight 函数
export default function highlight(option: HighlightOption = {}) {
    const {
        needTools = true
    } = option;

    return (str: string, lang: string) => {

        if (needTools) {
            // 创建代码块容器
            let container = `<div class="openmcp-code-block">`;

            // 添加复制按钮（右上角）
            container += `
        <div class="code-header">
        <div class="code-language">${lang || ''}</div>
        <button class="copy-button" onclick="copyCode(this)">${t("copy")}</button>
        </div>
        `;

            if (lang && Prism.languages[lang]) {
                // 使用 Prism 高亮代码
                const highlightedCode = Prism.highlight(str, Prism.languages[lang], lang);
                // 添加代码区域
                container += `<pre class="language-${lang}"><code class="language-${lang}">${highlightedCode}</code></pre>`;
            } else {
                // 普通代码块
                container += `<pre class="language-none"><code>${escapeHtml(str)}</code></pre>`;
            }

            container += `</div>`;
            return container;
        } else {
            return Prism.highlight(str, Prism.languages[lang], lang);
        }
    }
}


// 全局复制函数
(window as any).copyCode = function (button: HTMLElement) {
    const codeBlock = button.closest('.openmcp-code-block');
    if (!codeBlock) return;
    const codeElement = codeBlock.querySelector('code');
    const code = codeElement?.textContent || '';

    //  支持 nodejs 下运行
    const thisWindow = window as any;
    if (!thisWindow || !thisWindow.navigator || !thisWindow.navigator.clipboard) {
        return;
    }

    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.textContent;
        button.textContent = t('copied');
        setTimeout(() => {
            button.textContent = originalText;
        }, 500);
    }).catch((error) => {
        console.error('复制失败:', error);
        button.textContent = t('fail-to-copy');
    });
};