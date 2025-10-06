import { requestHandlerStorage } from "./index.js";
import type { PostMessageble } from "../hook/adapter.js";
import { LlmController } from "../llm/llm.controller.js";
import { ClientController } from "../mcp/client.controller.js";
import { ConnectController } from "../mcp/connect.controller.js";
import { OcrController } from "../mcp/ocr.controller.js";
import { PanelController } from "../panel/panel.controller.js";
import { SettingController } from "../setting/setting.controller.js";
export { disconnectService } from "../mcp/connect.service.js";

export const ModuleControllers = [
    ConnectController,
    ClientController,
    LlmController,
    PanelController,
    SettingController,
    OcrController
];

export async function routeMessage(command: string, data: any, webview: PostMessageble) {
    const handlerStore = requestHandlerStorage.get(command);
    if (handlerStore) {
        const { handler, option = {} } = handlerStore;

        try {
            const res = await handler(data, webview);

            // res.code = -1 代表当前请求不需要返回发送
            if (res.code >= 0) {
                const payload = {
                    _id: data._id,
                    ...res
                }
                webview.postMessage({
                    command, data: payload
                });
                return payload;
            }
        } catch (error) {
            // console.error(error);
            const payload = {
                _id: data._id,
                code: 500,
                msg: (error as any).toString()
            }
            webview.postMessage({
                command, data: payload
            });

            return payload;
        }
    }
    return
}