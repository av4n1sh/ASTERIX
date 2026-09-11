const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let pythonProcess;
let pythonBuffer = "";

function createWindow() {
    const window = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 1000,
        minHeight: 650,
        backgroundColor: "#08080b",
        title: "Asterix",

        webPreferences: {
            contextIsolation: true,
            nodeIntegration: false,
            preload: path.join(__dirname, "preload.js")
        }
    });

    window.loadFile("index.html");
}

function startPython() {
    const pythonPath = path.join(
        __dirname,
        "..",
        "bridge.py"
    );

    pythonProcess = spawn(
        "python",
        [pythonPath],
        {
            cwd: path.join(__dirname, ".."),
            stdio: ["pipe", "pipe", "pipe"]
        }
    );

    pythonProcess.stdout.on("data", (data) => {
        pythonBuffer += data.toString();
        console.log("Python:", data.toString().trim());
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(
            "Python error:",
            data.toString()
        );
    });

    pythonProcess.on("error", (error) => {
        console.error(
            "Failed to start Python:",
            error
        );
    });

    pythonProcess.on("close", (code) => {
        console.log(
            `Python process exited with code ${code}`
        );
        pythonProcess = null;
    });
}

ipcMain.handle(
    "send-message",
    async (event, message) => {
        if (!pythonProcess) {
            return {
                error: "Python backend is not running."
            };
        }

        return new Promise((resolve) => {
            pythonBuffer = "";

            const checkForResponse = () => {
                const newlineIndex =
                    pythonBuffer.indexOf("\n");

                if (newlineIndex === -1) {
                    setTimeout(
                        checkForResponse,
                        10
                    );
                    return;
                }

                const line =
                    pythonBuffer
                        .slice(0, newlineIndex)
                        .trim();

                pythonBuffer =
                    pythonBuffer.slice(
                        newlineIndex + 1
                    );

                if (!line) {
                    checkForResponse();
                    return;
                }

                try {
                    const response =
                        JSON.parse(line);

                    resolve(response);
                }

                catch (error) {
                    console.error(
                        "Invalid JSON from Python:",
                        line
                    );

                    resolve({
                        error:
                            "Python returned an invalid response."
                    });
                }
            };

            pythonProcess.stdin.write(
                JSON.stringify({
                    message: message
                }) + "\n"
            );

            checkForResponse();
        });
    }
);

app.whenReady().then(() => {
    startPython();
    createWindow();

    app.on("activate", () => {
        if (
            BrowserWindow
                .getAllWindows()
                .length === 0
        ) {
            createWindow();
        }
    });
});

app.on("window-all-closed", () => {
    if (pythonProcess) {
        pythonProcess.kill();
        pythonProcess = null;
    }

    if (process.platform !== "darwin") {
        app.quit();
    }
});