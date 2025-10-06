import MarkdownIt from 'markdown-it';
import MarkdownKatex from './markdown-katex';
import MarkdownHighlight from './markdown-highlight';

const md = new MarkdownIt({
    highlight: MarkdownHighlight({ needTools: true }),
});

md.use(MarkdownKatex, {
    delimiters: [
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false },
        { left: '$$', right: '$$', display: false },
    ],
});

export const markdownToHtml = (markdown: string) => {
    return md.render(markdown);
};

const pureHighLightMd = new MarkdownIt({
    highlight: MarkdownHighlight({ needTools: false }),
});

export const copyToClipboard = (text: string) => {
    //  支持 nodejs 下运行
    const thisWindow = window as any;
    if (!thisWindow || !thisWindow.navigator || !thisWindow.navigator.clipboard) {
        return;
    }
    
    return navigator.clipboard.writeText(text);
};

const tryParseJson = (text: string) => {
    try {
        return JSON.parse(text);
    } catch (error) {
        return text;
    }
}


const prettifyObj = (obj: object | string) => {
    const rawObj = typeof obj === 'string' ? tryParseJson(obj) : obj;
    return JSON.stringify(rawObj, null, 2);
}

export const renderJson = (obj: object | string | undefined) => {
    if (!obj) {
        return '<span>Invalid JSON</span>';
    }

    const jsonString = prettifyObj(obj);
    const md = "```json\n" + jsonString + "\n```";
    const html = pureHighLightMd.render(md);
    return html;
}