const oldExecCmd = document.execCommand.bind(document);
export const patchEditors = new Set<any>();

export function patchPasteCommand() {    
    document.execCommand = (cmd, ...args) => {
        const el = document.activeElement;

        console.log(patchEditors);
        console.log(el);
                
        if (el && patchEditors.has(el)) {
            console.log('enter');

            if (cmd == "paste") {
                navigator.clipboard.readText().then(txt => {
                    const dt = new DataTransfer();
                    dt.setData("text/plain", txt);
                    el.dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt }));
                }).catch(console.error);

                return true;
            } else if (cmd == "cut" || cmd == "copy") {
                const dt = new DataTransfer();
                el.dispatchEvent(new ClipboardEvent(cmd, { clipboardData: dt }));
                void navigator.clipboard.writeText(dt.getData("text/plain"));

                return true;
            }
        }

        return oldExecCmd(cmd, ...args);
    };
}
