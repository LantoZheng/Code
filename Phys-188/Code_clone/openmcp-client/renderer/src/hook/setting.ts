import { useMessageBridge } from "@/api/message-bridge";
import { llmManager, llms } from "@/views/setting/llm";
import { pinkLog } from "@/views/setting/util";
import I18n from '@/i18n/index';
import { userHasReadGuide } from "@/components/guide/tour";
import { mcpSetting } from "./mcp";

export async function loadSetting() {
    const bridge = useMessageBridge();

    const data = await bridge.commandRequest('setting/load');
    if (data.code !== 200) {
        pinkLog('配置加载失败');
        console.log(data.msg);

    } else {
        const persistConfig = data.msg;
        pinkLog('配置加载成功');        

        llmManager.currentModelIndex = persistConfig.MODEL_INDEX || 0;
        I18n.global.locale.value = persistConfig.LANG || 'zh';
        mcpSetting.language = persistConfig.LANG || 'zh';
        mcpSetting.timeout = persistConfig.MCP_TIMEOUT_SEC || 60;
        mcpSetting.proxyServer = persistConfig.PROXY_SERVER || '';

        persistConfig.LLM_INFO.forEach((element: any) => {
            llms.push(element);
        });
    }
}

export async function getTour() {
    const bridge = useMessageBridge();
    const { code, msg } = await bridge.commandRequest('setting/get-tour');
    
    if (code === 200) {
        pinkLog('获取引导状态成功 ' + msg.userHasReadGuide);
        userHasReadGuide.value = msg.userHasReadGuide || false;
    }
}

export async function setTour() {
    const bridge = useMessageBridge();
    const { code, msg } = await bridge.commandRequest('setting/set-tour', {
        userHasReadGuide: userHasReadGuide.value
    });
}

export function saveSetting(saveHandler?: () => void) {
    const bridge = useMessageBridge();

    // 过滤掉临时配置，只保存永久配置
    const permanentLlms = llms.filter(llm => !llm._isTemporary);
    
    const saveConfig = {
        MODEL_INDEX: llmManager.currentModelIndex,
        LLM_INFO: JSON.parse(JSON.stringify(permanentLlms)),
        LANG: I18n.global.locale.value,
        MCP_TIMEOUT_SEC: mcpSetting.timeout,
        PROXY_SERVER: mcpSetting.proxyServer
    };
    
    console.log(`[DEBUG] 保存设置: 总配置 ${llms.length} 个，永久配置 ${permanentLlms.length} 个`);

    bridge.addCommandListener('setting/save', data => {
        const saveStatusCode = data.code;
        pinkLog('配置保存状态：' + saveStatusCode);

        if (saveHandler) {
            saveHandler();
        }
    }, { once: true });

    bridge.postMessage({
        command: 'setting/save',
        data: saveConfig
    });
}