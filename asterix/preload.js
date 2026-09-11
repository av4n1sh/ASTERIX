const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("asterix", {
    sendMessage: (message) => ipcRenderer.invoke("send-message", message)
});